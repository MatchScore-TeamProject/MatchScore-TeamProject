import datetime

from database.database_connection import read_query

CURRENT_DATE_TIME = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def name_exists(name: str, table_name: str) -> bool:
    return any(
        read_query(
            f'SELECT name FROM {table_name} where name = ?',
            (name,)))


def id_exists(id: int, table_name: str) -> bool:
    return any(
        read_query(
            f'SELECT id FROM {table_name} where id = ?',
            (id,)))


def email_exists(email: str, table_name: str) -> bool:
    return any(
        read_query(
            f'SELECT email FROM {table_name} where email = ?',
            (email,)))


def users_id_exists(users_id: int, table_name: str) -> bool:
    return any(
        read_query(
            f'SELECT users_id FROM {table_name} where users_id = ?',
            (users_id,)))