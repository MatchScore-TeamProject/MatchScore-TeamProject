from database.database_connection import read_query, insert_query, update_query
from models.match import Match
from models.options import EmailType
from services.utilities import find_player_id_by_nickname, get_user_email_to_send_email_to, get_user_id_from_table, \
    find_player_nickname_by_id
from services.emails import send_email_changed_match_date, send_email_for_added_to_event


def all(search: str = None, date: str = None):
    if search and date:

        data = read_query('''SELECT id, date, format, tournament_id, player_profile_id1, player_profile_id2, score_1, score_2, winner, stage, order_num
                                FROM matches
                                WHERE id LIKE ? AND date = ?''', (f"%{search}%", date))
    elif date:

        data = read_query('''SELECT id, date, format, tournament_id, player_profile_id1, player_profile_id2, score_1, score_2, winner, stage, order_num
                                FROM matches
                                WHERE date = ?''', (date,))
    elif search:

        data = read_query('''SELECT id, date, format, tournament_id, player_profile_id1, player_profile_id2, score_1, score_2, winner, stage, order_num
                                FROM matches
                                WHERE id LIKE ?''', (f"%{search}%",))
    else:

        data = read_query('''SELECT id, date, format, tournament_id, player_profile_id1, player_profile_id2, score_1, score_2, winner, stage, order_num
                                FROM matches''')

    matches = []

    for row in data:
        player1_nickname = find_player_nickname_by_id(row[4])
        player2_nickname = find_player_nickname_by_id(row[5])
        winner_nickname = row[8] if row[8] else "N/A"
        tournament_name = read_query("SELECT title FROM tournaments WHERE id=?", (row[3],))
        if not tournament_name:
            tournament_name = "This match is not part of a tournament!"
        else:
            tournament_name = tournament_name[0][0]

        match = {
            "id": row[0],
            "date": row[1],
            "format": row[2],
            "details": f"{player1_nickname} {row[6]} vs {row[7]} {player2_nickname}",
            "winner": winner_nickname,
            "name": tournament_name
        }
        matches.append(match)

    return matches


def get_by_id(id: int):
    data = read_query('''SELECT id, date, format, tournament_id, player_profile_id1, player_profile_id2, score_1, score_2, winner, stage,order_num FROM matches WHERE id = ?''', (id,))

    return next((Match.from_query_result(*row) for row in data), None)


def update_by_id(old: Match, new_date):
    update_query('''UPDATE matches SET date = ? WHERE id = ?''', (new_date, old.id))

    user_id1 = get_user_id_from_table(old.player_profile_id1, "player_profile")
    user_id2 = get_user_id_from_table(old.player_profile_id2, "player_profile")

    user_email1 = get_user_email_to_send_email_to(user_id1)
    user_email2 = get_user_email_to_send_email_to(user_id2)

    send_email_changed_match_date(receiver=user_email1, new_date=new_date, email_type=EmailType.MATCH_CHANGED.value)
    send_email_changed_match_date(receiver=user_email2, new_date=new_date, email_type=EmailType.MATCH_CHANGED.value)


def exist(id: int):
    return any(read_query('''SELECT * FROM matches WHERE id = ?''', (id,)))


def sort(result: list[Match], *, attribute="date", reverse=False):
    if attribute == "date":
        def sort_func(m: Match):
            return m.date
    else:
        def sort_func(m: Match):
            return m.id

    return sorted(result, key=sort_func, reverse=reverse)


def check_date_of_match(id: int):
    date_of_match = read_query('''SELECT date from matches WHERE id = ?''', (id,))
    return date_of_match[0][0]


def create(date, format, tournament_id, nickname_1=None, nickname_2=None, stage=None, order_num=None):
    player_profile_id_1 = None
    player_profile_id_2 = None

    if nickname_1:
        player_profile_id_1 = find_player_id_by_nickname(nickname_1)
    if nickname_2:
        player_profile_id_2 = find_player_id_by_nickname(nickname_2)

    generated_id = insert_query('''INSERT INTO matches(date, format, tournament_id, player_profile_id1, player_profile_id2, stage, order_num) VALUES(?,?,?,?,?,?,?)''',
                                (date, format, tournament_id, player_profile_id_1, player_profile_id_2, stage,
                                 order_num))

    complete_match = get_by_id(generated_id)

    user_id_1 = get_user_id_from_table(player_profile_id_1, "player_profile")
    user_email_1 = get_user_email_to_send_email_to(user_id_1)

    user_id_2 = get_user_id_from_table(player_profile_id_2, "player_profile")
    user_email_2 = get_user_email_to_send_email_to(user_id_2)

    send_email_for_added_to_event(user_email_1, [nickname_1, nickname_2], date, EmailType.ADDED_TO_MATCH.value)
    send_email_for_added_to_event(user_email_2, [nickname_1, nickname_2], date, EmailType.ADDED_TO_MATCH.value)


    return complete_match


def delete(id: int):
    update_query('''DELETE FROM matches WHERE id = ?''', (id,))


def update_result_by_nicknames(tournament_id: int, nickname_1: str, score_1: int, score_2: int, nickname_2: str):
    player_profile_id1 = find_player_id_by_nickname(nickname_1)
    player_profile_id2 = find_player_id_by_nickname(nickname_2)

    correct_match = read_query('''SELECT * FROM matches WHERE tournament_id = ? AND player_profile_id1 = ? AND player_profile_id2 = ?''',
                               (tournament_id, player_profile_id1, player_profile_id2))

    if not correct_match:
        return False

    if score_1 > score_2:
        winner = nickname_1
    elif score_2 > score_1:
        winner = nickname_2
    else:
        winner = 'draw'

    update_query('''UPDATE matches SET  score_1 = ?, score_2 = ?, winner = ? WHERE tournament_id = ? AND player_profile_id1 = ? AND player_profile_id2 = ?''',

                 (
                     score_1,
                     score_2,
                     winner,
                     tournament_id,
                     player_profile_id1,
                     player_profile_id2,
                 ))

    max_order_num = read_query(
        """SELECT order_num FROM matches WHERE tournament_id = ? ORDER BY order_num DESC LIMIT 1""", (tournament_id,))

    curr_match = correct_match[0][-1]
    curr_max_order_num = max_order_num[0][0]

    # separates knockout from league (if stage = 0 is league, else knockout)
    check_stage = read_query("""SELECT stage
                                   FROM matches
                                   WHERE tournament_id = ? AND
                                    player_profile_id1 = ? AND
                                    player_profile_id2 = ?""", (tournament_id, player_profile_id1, player_profile_id2))

    if check_stage[0][0] != '0' and curr_max_order_num == curr_match:
        return f"The tournament is over! The winner is {winner}!"
    if check_stage[0][0] != '0':
        winner_to_next_stage(tournament_id, winner)

    if winner != 'draw':
        return f"Result updated. The winner is {winner}"
    else:
        return f"Result updated. The match ended in a draw"


def winner_to_next_stage(tournament_id: int, winner: str):
    first_available_match = read_query('''SELECT order_num FROM matchesWHERE tournament_id = ? AND (player_profile_id1 is NULL OR player_profile_id2 is NULL)''', (tournament_id,))

    available_match = first_available_match[0][0]

    is_id_1_null = read_query('''
               SELECT player_profile_id1
               FROM matches
               WHERE tournament_id = ?
               AND order_num = ? 
                ''', (tournament_id, available_match))

    is_id1_none = is_id_1_null[0][0] if is_id_1_null else None
    player = find_player_id_by_nickname(winner)

    if is_id1_none is None:
        update_query(f'''UPDATE matches SET player_profile_id1 = ? WHERE tournament_id = ? AND order_num = {available_match}''', (player, tournament_id))

    else:
        update_query(f'''UPDATE matches SET player_profile_id2 = ? WHERE tournament_id = ? AND order_num = {available_match}''', (player, tournament_id))
