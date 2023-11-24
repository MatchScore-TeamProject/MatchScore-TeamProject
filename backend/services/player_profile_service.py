from fastapi import HTTPException

from database.database_connection import read_query, read_query_additional, update_query, insert_query
from models.player_profile import PlayerProfile


def create_player_profile(nickname, full_name, country, sports_club, users_id):
    generated_id = insert_query(
        """INSERT INTO player_profile(nickname, full_name, country, sports_club, users_id) VALUES (?,?,?,?,?)""",
        (nickname, full_name, country, sports_club, users_id))

    return PlayerProfile(id=generated_id, nickname=nickname, full_name=full_name, country=country, sports_club=sports_club, user_id=users_id)


def delete_player_profile(player_profile_id):
    insert_query('''DELETE FROM player_profile WHERE id = ?''',
                 (player_profile_id,))


def edit_player_profile(player_profile_id: int, new_data: PlayerProfile, user_id, user_type):
    current_profile_data = read_query(
        "SELECT nickname, full_name, country, sports_club, users_id FROM player_profile WHERE id = ?",
        (player_profile_id,)
    )

    if not current_profile_data:
        raise HTTPException(status_code=404, detail=f"No player profile with ID: {player_profile_id} exists.")

    current_profile = current_profile_data[0]

    _, _, _, _, linked_user_id = current_profile_data[0]

    if linked_user_id:
        if linked_user_id != user_id:
            raise HTTPException(status_code=403, detail="You do not have permission to edit this player profile.")
    else:
        if user_type != "director":
            raise HTTPException(status_code=403, detail="Only a director can edit an unlinked player profile.")

    update_fields = {
        'nickname': new_data.nickname if new_data.nickname is not None else current_profile[0],
        'full_name': new_data.full_name if new_data.full_name is not None else current_profile[1],
        'country': new_data.country if new_data.country is not None else current_profile[2],
        'sports_club': new_data.sports_club if new_data.sports_club is not None else current_profile[3]
    }

    update_set_parts = [f"{key} = ?" for key in update_fields]
    update_query_str = "UPDATE player_profile SET " + ", ".join(update_set_parts) + " WHERE id = ?"
    update_params = list(update_fields.values()) + [player_profile_id]

    update_query(update_query_str, update_params)

    return "Player profile updated successfully."
