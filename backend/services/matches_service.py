from database.database_connection import read_query, insert_query
from models.match import Match
from datetime import date

CURRENT_DATE = date.today()


def create(date, format, participant_1, participant_2):
    generated_id = insert_query('''INSERT INTO matches(date, format, participant_1, participant_2) 
                                VALUES(?,?,?,?)''',
                                (date, format, participant_1, participant_2))

    created_match = Match(id=generated_id,
                          date=date,
                          format=format,
                          participant_1=participant_1,
                          participant_2=participant_2
                          )

    return created_match


def exist(id: int):
    return any(read_query('''SELECT * FROM matches WHERE id = ?''', (id,)))


def data_update(new_data):


def check_date_of_match(id: int):
    date_of_match = read_query('''SELECT date from matches WHERE id = ?''', ())
    return date_of_match


def check_for_future_date():
    pass