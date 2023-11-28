from database.database_connection import read_query, insert_query, update_query
from models.match import Match
from services.utilities import find_player_id_by_nickname


def all(search: str = None):
    if search is None:
        data = read_query('''SELECT id, date, format, tournament_id, player_profile_id1, player_profile_id2, score_1, score_2, winner, stage
                             FROM matches''')
    else:
        data = read_query('''SELECT id, date, format, tournament_id, player_profile_id1, player_profile_id2, score_1, score_2, winner, stage
                             FROM matches
                             WHERE date LIKE ?''', (f"%{search}",))

    return (Match.from_query_result(*row) for row in data)


def get_by_id(id: int):
    data = read_query('''SELECT id, date, format, tournament_id, player_profile_id1, player_profile_id2, score_1, score_2, winner, stage,order_num
                         FROM matches
                         WHERE id = ?''', (id,))

    return next((Match.from_query_result(*row) for row in data), None)


def update_by_id(old: Match, new: Match):
    merged = Match(id=old.id,
                   date=new.date or old.date,
                   format=new.format or old.format,
                   tournament_id=new.tournament_id or old.tournament_id,
                   player_profile_id1=new.player_profile_id1 or old.player_profile_id1,
                   player_profile_id2=new.player_profile_id2 or old.player_profile_id2,
                   score_1=new.score_1 or old.score_1,
                   score_2=new.score_2 or old.score_2
                   )

    update_query('''UPDATE matches SET 
                    date = ?, 
                    format = ?, 
                    tournament_id = ?, 
                    player_profile_id1 = ?,
                    player_profile_id2 = ?,
                    score_1 = ?,
                    score_2 = ?
                    WHERE id = ?''',

                 (merged.date,
                  merged.format,
                  merged.tournament_id,
                  merged.player_profile_id1,
                  merged.player_profile_id2,
                  merged.score_1,
                  merged.score_2,
                  merged.id))

    return merged


def exist(id: int):
    return any(read_query('''SELECT * FROM matches WHERE id = ?''', (id,)))


def sort(result: list[Match], *, attribute="date", reverse=False):
    if attribute == "date":
        def sort_func(m: Match): return m.date
    else:
        def sort_func(m: Match): return m.id

    return sorted(result, key=sort_func, reverse=reverse)


def check_date_of_match(id: int):
    date_of_match = read_query('''SELECT date from matches 
                                  WHERE id = ?''', (id,))
    return date_of_match[0][0]


# def create(date, format, nickname_1, nickname_2):
#     player_profile_id_1 = find_player_id_by_nickname(nickname_1)
#     player_profile_id_2 = find_player_id_by_nickname(nickname_2)
#
#     generated_id = insert_query('''INSERT INTO matches(date, format, player_profile_id1, player_profile_id2)
#                                 VALUES(?,?,?,?)''',
#                                 (date, format, player_profile_id_1, player_profile_id_2))
#
#     complete_match = get_by_id(generated_id)
#
#     return complete_match

def create(date, format, tournament_id, nickname_1=None, nickname_2=None, stage=None, order_num=None):
    player_profile_id_1 = None
    player_profile_id_2 = None

    if nickname_1:
        player_profile_id_1 = find_player_id_by_nickname(nickname_1)
    if nickname_2:
        player_profile_id_2 = find_player_id_by_nickname(nickname_2)

    generated_id = insert_query('''INSERT INTO matches(date, format, tournament_id, player_profile_id1, player_profile_id2, stage, order_num) 
                                VALUES(?,?,?,?,?,?,?)''',
                                (date, format, tournament_id, player_profile_id_1, player_profile_id_2, stage, order_num))

    complete_match = get_by_id(generated_id)

    return complete_match


def delete(id: int):
    update_query('''DELETE FROM matches WHERE id = ?''', (id))

def update_by_id(old: Match, new: Match):
    merged = Match(id=old.id,
                    date=new.date or old.date,
                    format=new.format or old.format,
                    tournament_id=new.tournament_id or old.tournament_id,
                    player_profile_id1=new.player_profile_id1 or old.player_profile_id1,
                    player_profile_id2=new.player_profile_id2 or old.player_profile_id2,
                    score_1=new.score_1 or old.score_1,
                    score_2=new.score_2 or old.score_2
                    )

    update_query('''UPDATE matches SET 
                    date = ?, 
                    format = ?, 
                    tournament_id = ?, 
                    player_profile_id1 = ?,
                    player_profile_id2 = ?,
                    score_1 = ?,
                    score_2 = ?
                    WHERE id = ?''',

                    (merged.date,
                    merged.format,
                    merged.tournament_id,
                    merged.player_profile_id1,
                    merged.player_profile_id2,
                    merged.score_1,
                    merged.score_2,
                    merged.id))

    return merged