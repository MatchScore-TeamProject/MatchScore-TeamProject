from database.database_connection import read_query, insert_query, update_query
from models.match import Match


def all(search: str = None):
    if search is None:
        data = read_query('''SELECT id, date, format, tournament_id, player_profile_id1, player_profile_id2, score_1, score_2
                             FROM matches''')
    else:
        data = read_query('''SELECT id, date, format, tournament_id, player_profile_id1, player_profile_id2, score_1, score_2
                             FROM matches
                             WHERE date LIKE ?''', (f"%{search}",))

    return (Match.from_query_result(*row) for row in data)


def get_by_id(id: int):
    data = read_query('''SELECT id, date, format, tournament_id, player_profile_id1, player_profile_id2, score_1, score_2
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


def create(date, format, player_profile_id1, player_profile_id2):
    generated_id = insert_query('''INSERT INTO matches(date, format, player_profile_id1, player_profile_id2) 
                                VALUES(?,?,?,?)''',
                                (date, format, player_profile_id1, player_profile_id2))

    created_match = Match(id=generated_id,
                          date=date,
                          format=format,
                          player_profile_id1=player_profile_id1,
                          player_profile_id2=player_profile_id2
                          )

    return created_match


def delete(id: int):
    update_query('''DELETE FROM matches WHERE id = ?''', (id))