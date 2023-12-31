from database.database_connection import read_query
from datetime import date

CURRENT_DATE = date.today()


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


def find_player_id_by_nickname(nickname: str):
    result = read_query("SELECT id FROM player_profile WHERE nickname = ?", (nickname,))

    return result[0][0] if result else None


def find_player_nickname_by_id(player_id: int):
    result = read_query("SELECT nickname FROM player_profile WHERE id = ?", (player_id,))
    return result[0][0] if result else None


def get_user_email_to_send_email_to(user_id: int):
    user_email = read_query("SELECT email FROM users WHERE id=?", (user_id,))[0][0] if user_id else None

    return user_email


def get_user_id_from_table(id: int, table_name: str):
    user_id = read_query(f"SELECT users_id FROM {table_name} WHERE id=?", (id,))[0][0] if id else None

    return user_id
