from fastapi import HTTPException
from database.database_connection import read_query, read_query_additional, update_query, insert_query
from models.tournament import Tournament, TournamentFormat, TournamentStatus, TournamentType
from models.player_profile import PlayerProfile
from typing import List
from services.utilities import find_player_id_by_nickname
from services.matches_service import create as create_match
import random


def create_tournament(
    title: str,
    date: str,
    tournament_format: str,
    match_format: str,
    prize: str,
    player_nicknames: List[str]
    ):
    
    valid_player_counts = {4, 8, 16, 32, 64}

    if len(player_nicknames) not in valid_player_counts:
        raise HTTPException(status_code=400, detail="Number of players must be 4, 8, 16, 32 or 64 for a knockout tournament")

    tournament = Tournament(
        title=title,
        date=date,
        tournament_format=tournament_format,
        match_format=match_format,
        prize=prize,
        player_nicknames=player_nicknames
    )

    generated_id = insert_query(
        """INSERT INTO tournaments(
            title, date, tournament_format, match_format, prize
        ) VALUES(?, ?, ?, ?, ?)""",
        (
            title,
            date,
            tournament_format,
            match_format,
            prize,
        ),
    )

    tournament.id = generated_id

    random.shuffle(player_nicknames)

    matches = create_knockout_matches(player_nicknames, tournament)

    for player_nickname in player_nicknames:
        player_id = find_player_id_by_nickname(player_nickname)
        if player_id is not None:
            insert_query(
                """INSERT INTO tournaments_has_player_profile(tournaments_id, player_profile_id) VALUES (?, ?)""",
                (tournament.id, player_id),
            )


    return tournament, player_nicknames, matches


def create_knockout_matches(player_nicknames: List[str], tournament: Tournament) :

    pairs = [(player_nicknames[i], player_nicknames[i + 1]) for i in range(len(player_nicknames)//2)]

    
    for pair in pairs:
        create_and_insert_match(tournament, pair[0], pair[1])

    return pairs


def create_and_insert_match(tournament: Tournament, player1: str, player2: str):

    player_id1 = find_player_id_by_nickname(player1)
    player_id2 = find_player_id_by_nickname(player2)

    create_match(tournament.date, tournament.match_format, player_id1, player_id2)













def all():
    data = read_query(
        '''SELECT id, title, date, tournament_format, match_format, prize
        FROM tournaments'''
    )

    if data is None:
        return None

    tournaments = []
    for row in data:
        tournament_id = row[0]
        nicknames_data = read_query(
            '''SELECT nickname
            FROM tournaments_has_player_profile
            JOIN player_profile ON tournaments_has_player_profile.player_profile_id = player_profile.id
            WHERE tournaments_id = ?''',
            (tournament_id,)
        )

        nicknames = [nickname[0] for nickname in nicknames_data]

        tournament = [Tournament.from_query_result(*row, player_nicknames=nicknames)]
        tournaments.append(tournament)

    return tournaments

def get_by_id(tournament_id: int):
    data = read_query(
        '''SELECT id, title, date, tournament_format, match_format, prize
        FROM tournaments
        WHERE id = ?''',
        (tournament_id,)
    )

    if data is None or len(data) == 0:
        return None

    row = data[0]
    nicknames_data = read_query(
        '''SELECT nickname
        FROM tournaments_has_player_profile
        JOIN player_profile ON tournaments_has_player_profile.player_profile_id = player_profile.id
        WHERE tournaments_id = ?''',
        (tournament_id,)
    )

    nicknames = [nickname[0] for nickname in nicknames_data]

    tournament = Tournament.from_query_result(*row, player_nicknames=nicknames)

    return tournament