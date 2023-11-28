from fastapi import HTTPException
from database.database_connection import read_query, read_query_additional, update_query, insert_query
from models.tournament import Tournament, TournamentFormat, TournamentStatus, TournamentType
from models.player_profile import PlayerProfile
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
        raise HTTPException(status_code=400, detail="Number of players must be 4, 8, 16, 32 or 64 for a knockout tournament")

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
    matches = create_all_next_matches(tournament, len(player_nicknames)//2, player_nicknames)


    return tournament, player_nicknames


def pair_players_with_matches(players_left: List[str], tournament: Tournament, matches: List[str]):

    pairs = [(players_left[i], players_left[i + 1]) for i in range(0, len(players_left), 2)]

    
    for pair in pairs:
        created_pair = create_and_insert_match(tournament, pair[0], pair[1])

        # matches.append(MatchResponse.from_query_result(
        #     find_player_nickname_by_id(created_match.player_profile_id1),
        #     created_match.score_1,
        #     created_match.score_2,
        #     find_player_nickname_by_id(created_match.player_profile_id2)),
        #     )

    return matches 


def create_and_insert_match(tournament: Tournament, player1: str, player2: str, stage, order_num: int):

    created_match = create_match(tournament.date, tournament.match_format, tournament.id, player1, player2, stage, order_num)

    return created_match

# def populate_match(tournament: Tournament, nickname_1, nickname_2)
    
#     pair = insert_query(""")


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


def find_stage_from_players(players_left: list):
    if len(players_left)== 2:
        return "Final"
    if len(players_left)== 4:
        return "Semi Final"
    if len(players_left)== 8:
        return "Quarter Final"
    if len(players_left)== 16:
        return "Round of Sixteen"
    if len(players_left)== 32:
        return "Round of Thirty-Two"
    

# def create_match_next_round(tournament: Tournament, player_left: list):
#     # count // 4 if players are in initial matches, else count // 2 
#     while player_left >= 4:
#         count = len(player_left)
#         for _ in range(count// 4):
#             create_and_insert_match(tournament, None, None)
#             player_left //= 2

def create_all_next_matches(tournament: Tournament, matches_count: int, player_nicknames: List[str]):
    order_num = 1
    stage = 1
    matches = []
    pairs = [(player_nicknames[i], player_nicknames[i + 1]) for i in range(0, len(player_nicknames), 2)]
#[[1,2], [3,4]]    

    while matches_count >= 1:
        for _ in range(matches_count):
            if stage == 1:
                current_pair = []
                current_pair.append(pairs[0])
                pairs.pop(0)
            matches_count
            current_match = create_and_insert_match(tournament, current_pair[0], current_pair[1], stage, order_num)
            order_num += 1
            matches.append(current_match)
        matches_count //= 2
        stage += 1
    
    return matches
        


