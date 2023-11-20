from database.database_connection import read_query, read_query_additional, update_query, insert_query
from models.player_profile import PlayerProfile


def create_player_profile(fullname, country, sports_club, users_id):
    generated_id = insert_query(
        """INSERT INTO player_profile(full_name, country, sports_club, users_id) VALUES (?,?,?,?)""",
        (fullname, country, sports_club, users_id))

    return PlayerProfile(id=generated_id, full_name=fullname, country=country, sports_club=sports_club, user_id=users_id)


def delete_player_profile(player_profile_id):
    insert_query('''DELETE FROM player_profile WHERE id = ?''',
                 (player_profile_id,))


