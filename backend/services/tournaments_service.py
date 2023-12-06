from datetime import datetime, timedelta
from itertools import combinations
from fastapi import HTTPException
from database.database_connection import read_query, read_query_additional, update_query, insert_query
from models.tournament import Tournament, TournamentFormat, TournamentStatus, TournamentType
from models.match import MatchResponse, Match
from typing import List
from services.utilities import find_player_id_by_nickname, find_player_nickname_by_id
from services.matches_service import create as create_match
from services.player_profile_service import find_non_existing_players, create_player_profile
import random


def create_knockout(
        title: str,
        date: str,
        tournament_format: str,
        match_format: str,
        prize: str,
        player_nicknames: List[str]
):

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
    create_all_next_matches(tournament, len(player_nicknames) // 2, player_nicknames)

    populate_initial_matches_with_players(tournament, player_nicknames)

    return tournament


def create_and_insert_match(tournament: Tournament, player1: str, player2: str, stage, order_num: int):
    created_match = create_match(tournament.date, tournament.match_format, tournament.id, player1, player2, stage,
                                 order_num)
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

        matches = get_all_matches_in_tournament_by_id(tournament_id)

        tournament_dict = {
            "Name": row[1],
            "Date": row[2],
            "Tournament Format": row[3],
            "Matches Format": row[4],
            "Prize": f"{row[5]}$",
            "Players' Nicknames": ", ".join(nicknames),
            "Matches": matches
        }

        tournaments.append(tournament_dict)

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

    matches = get_all_matches_in_tournament_by_id(tournament_id)

    tournament_dict = {
        "Name": row[1],
        "Date": row[2],
        "Tournament Format": row[3],
        "Match Format": row[4],
        "Prize": f"{row[5]}$",
        "Players' Nicknames": ", ".join(nicknames),
        "Matches": matches
    }

    return tournament_dict


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

    formatted_matches = []

    for match in data:
        player1_name = find_player_nickname_by_id(match[5])
        player2_name = find_player_nickname_by_id(match[6])
        score_1 = match[3]
        score_2 = match[4]

        match_string = f"{player1_name} {score_1} vs {score_2} {player2_name} | Winner: {match[7]} | Stage: {match[8]}"

        formatted_matches.append(match_string)

    return formatted_matches


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


def delete_tournament(tournament_id: int):
    insert_query("DELETE FROM tournaments_has_player_profile WHERE tournaments_id = ?", (tournament_id,))

    insert_query("DELETE FROM matches WHERE tournament_id = ?", (tournament_id,))

    insert_query("DELETE FROM tournaments WHERE id = ?", (tournament_id,))


def create_league(
        title: str,
        date: str,
        tournament_format: str,
        match_format: str,
        prize: str,
        player_nicknames: List[str]):

    participants_list = player_nicknames
    pairs = list(combinations(participants_list, 2))

    list_of_matches = []
    counter_matches = 0

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
    for pair in pairs:
        nickname_1 = pair[0]
        nickname_2 = pair[1]

        format = tournament.match_format
        tournament_id = tournament.id
        order_num = None
#  The following variables are for converting and adding the next match date to the current date!
        date_str = tournament.date
        date_object = datetime.strptime(date_str, '%Y-%m-%d')
        adding_days_to_date = date_object + timedelta(days=counter_matches)
        result_date_str = adding_days_to_date.strftime('%Y-%m-%d')

        match = create_match(
            date=result_date_str,
            format=format,
            tournament_id=tournament_id,
            nickname_1=nickname_1,
            nickname_2=nickname_2,
            stage=0,
            order_num=order_num)

        counter_matches += 1
        list_of_matches.append(match)

    return list_of_matches


def get_tournament_id_by_name(tournament_name: str):
    tournament_id = read_query('''SELECT id FROM tournaments WHERE title=?''', (tournament_name,))

    if not tournament_id:
        raise HTTPException(status_code=404, detail="Tournament not found.")

    return tournament_id[0][0]
