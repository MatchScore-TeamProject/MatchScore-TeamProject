from database.database_connection import read_query
from services.utilities import find_player_nickname_by_id


def all_players(tournament_id: int):
    players_in_tournament = read_query(
        '''SELECT player_profile_id1, player_profile_id2 
        FROM matches 
        WHERE tournament_id = ?''', (tournament_id,))

    result = players_in_tournament
    unique_nums = set()

    for el in result:
        unique_nums.update(el)

    result_dict = {num: 0 for num in unique_nums}

    match_result = read_query('''
        SELECT score_1, score_2, player_profile_id1, player_profile_id2 
        FROM matches   
        WHERE tournament_id = ?''', (tournament_id,))

    for el in match_result:
        score_id_1 = el[0]
        score_id_2 = el[1]

        player_1 = el[2]
        player_2 = el[3]

        if score_id_1 > score_id_2:
            pts = 2

            if player_1 in result_dict:
                result_dict[player_1] += pts

        elif score_id_1 < score_id_2:
            pts = 2

            if player_2 in result_dict:
                result_dict[player_1] += pts

        else:
            pts = 1
            if player_1 and player_2 in result_dict:
                result_dict[player_1] += pts
                result_dict[player_2] += pts

    new_dict = {}

    for key, val in result_dict.items():
        new_key = find_player_nickname_by_id(key)
        value = val
        new_dict[new_key] = value

    result = [f"Player - {name}: {score} pts" for name, score in new_dict.items()]
    return result
