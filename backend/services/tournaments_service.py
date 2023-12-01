from fastapi import HTTPException
from database.database_connection import read_query, read_query_additional, update_query, insert_query
from models.tournament import Tournament, TournamentFormat, TournamentStatus, TournamentType
from models.match import MatchResponse, Match
from typing import List
from services.utilities import find_player_id_by_nickname, find_player_nickname_by_id
from services.matches_service import create as create_match
from services.player_profile_service import find_non_existing_players, create_player_profile
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
        raise HTTPException(status_code=400,
                            detail="Number of players must be 4, 8, 16, 32 or 64 for a knockout tournament")

    players_to_create = find_non_existing_players(player_nicknames)
    if players_to_create:
        for player in players_to_create:
            create_player_profile(player, None, None, None, None)

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
    link_player_profile_and_tournament(player_nicknames, tournament)

    # matches = pair_knockout_matches(player_nicknames, tournament)
    matches = create_all_next_matches(tournament, len(player_nicknames) // 2, player_nicknames)

    initial_games = populate_initial_matches_with_players(tournament, player_nicknames)

    return tournament, player_nicknames


def create_and_insert_match(tournament: Tournament, player1: str, player2: str, stage, order_num: int):
    created_match = create_match(tournament.date, tournament.match_format, tournament.id, player1, player2, stage, order_num)
    return created_match


def link_player_profile_and_tournament(player_nicknames, tournament):
    for player_nickname in player_nicknames:
            player_id = find_player_id_by_nickname(player_nickname)
            if player_id is not None:
                insert_query(
                    """INSERT INTO tournaments_has_player_profile(tournaments_id, player_profile_id) VALUES (?, ?)""",
                    (tournament.id, player_id),
                )


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


def create_all_next_matches(tournament: Tournament, matches_count: int, player_nicknames: List[str]):
    order_num = 1
    stage = 1
    matches = []

    while matches_count >= 1:
        for _ in range(matches_count):
            current_match = create_and_insert_match(tournament, None, None, stage, order_num)
            order_num += 1
            matches.append(current_match)
        matches_count //= 2
        stage += 1

    return matches


def populate_initial_matches_with_players(tournament: Tournament, participants_left: List[str]):
    pairs = [(participants_left[i], participants_left[i + 1]) for i in range(0, len(participants_left), 2)]
    stage = 1
    order_num = 1
    for current_pair in pairs:
        player1_id = find_player_id_by_nickname(current_pair[0])
        player2_id = find_player_id_by_nickname(current_pair[1])

        update_query(
            """UPDATE matches
               SET player_profile_id1 = ?,
                   player_profile_id2 = ?
               WHERE tournament_id = ? AND stage = ? AND order_num = ?""",
            (player1_id, player2_id, tournament.id, stage, order_num)
        )
        order_num += 1


def get_all_matches_in_tournament_by_id(tournament_id: int):
    data = read_query(
        '''SELECT id, date, tournament_id, score_1, score_2, player_profile_id1, player_profile_id2, winner, stage
        FROM matches
        WHERE tournament_id = ?''',
        (tournament_id,))

    return data


"""It is about to be used in league functionality"""
# def find_stage_from_players(players_left: list):
#     if len(players_left)== 2:
#         return "Final"
#     if len(players_left)== 4:
#         return "Semi Final"
#     if len(players_left)== 8:
#         return "Quarter Final"
#     if len(players_left)== 16:
#         return "Round of Sixteen"
#     if len(players_left)== 32:
#         return "Round of Thirty-Two"
