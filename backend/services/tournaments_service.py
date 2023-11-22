from database.database_connection import read_query, read_query_additional, update_query, insert_query
from models.tournament import Tournament, TournamentFormat, TournamentStatus, TournamentType
from models.player_profile import PlayerProfile
from typing import List

def create_tournament(tournament: Tournament, player_ids: List[int]):
    
    valid_player_counts = {4, 8, 16, 32, 64}

    if len(player_ids) not in valid_player_counts:
        raise ValueError("Number of players must be 4, 8, 16, 32 or 64 for a knockout tournament")

    generated_id = insert_query(
        """INSERT INTO tournament(
            title,tournament_format,match_format,prize) VALUES(?,?,?,?)""",
        (
            tournament.title,
            tournament.tournament_format,
            tournament.match_format,
            tournament.prize,
        ),
    )

    tournament.id = generated_id

    for player_id in player_ids:
        insert_query(
            """INSERT INTO tournaments_has_player_profile(tournament_id, player_profile_id) VALUES (?, ?)""",
            (tournament.id, player_id),
        )

    return tournament