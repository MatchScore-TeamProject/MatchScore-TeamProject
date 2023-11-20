from database.database_connection import read_query, insert_query
from models.match import Match


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
