import unittest
from unittest.mock import patch, MagicMock

from models.match import Match
from models.tournament import Tournament
from services.tournaments_service import create_knockout, create_and_insert_match, link_player_profile_and_tournament, all


class TournamentsServiceTest(unittest.TestCase):
    @patch('services.tournaments_service.send_emails_for_added_to_tournament')
    @patch('services.tournaments_service.populate_initial_matches_with_players')
    @patch('services.tournaments_service.create_all_next_matches')
    @patch('services.tournaments_service.link_player_profile_and_tournament')
    @patch('services.tournaments_service.insert_query')
    @patch('services.tournaments_service.create_player_profile')
    @patch('services.tournaments_service.find_non_existing_players')
    def test_create_knockout(self, mock_find_non_existing_players, mock_create_player_profile, mock_insert_query,
                             mock_link_player_profile_and_tournament, mock_create_all_next_matches,
                             mock_populate_initial_matches_with_players, mock_send_emails_for_added_to_tournament):
        title = "Tournament Title"
        date = "2021-01-01"
        tournament_format = "Knockout"
        match_format = "Best of 3"
        prize = "1000"
        player_nicknames = ["Player1", "Player2"]
        mock_find_non_existing_players.return_value = []
        generated_id = 1
        mock_insert_query.return_value = generated_id

        result = create_knockout(title, date, tournament_format, match_format, prize, player_nicknames)

        mock_find_non_existing_players.assert_called_once_with(player_nicknames)
        mock_insert_query.assert_called_once()
        mock_link_player_profile_and_tournament.assert_called_once()
        mock_create_all_next_matches.assert_called_once()
        mock_populate_initial_matches_with_players.assert_called_once()
        mock_send_emails_for_added_to_tournament.assert_called_once()
        self.assertIsInstance(result, Tournament)
        self.assertEqual(result.id, generated_id)



    @patch('services.tournaments_service.create_match')
    def test_create_and_insert_match(self, mock_create_match):
        tournament = Tournament(
            id=1,
            title='Tournament Title',
            date='2024-10-20',
            tournament_format='Knockout',
            match_format='score',
            prize=1000,
            player_nicknames=['Player1', 'Player2']
        )
        player_profile_id1 = 101
        player_profile_id2 = 102
        stage = 1
        order_num = 1
        mock_created_match = Match(
            id=1,
            date=tournament.date,
            format=tournament.match_format,
            tournament_id=tournament.id,
            player_profile_id1=player_profile_id1,
            player_profile_id2=player_profile_id2,
            stage=stage,
            order_num=order_num

        )
        mock_create_match.return_value = mock_created_match

        result = create_and_insert_match(tournament, player_profile_id1, player_profile_id2, stage, order_num)

        mock_create_match.assert_called_once_with(
            tournament.date, tournament.match_format, tournament.id, player_profile_id1, player_profile_id2, stage,
            order_num
        )
        self.assertEqual(result, mock_created_match)

    @patch('services.tournaments_service.insert_query')
    @patch('services.tournaments_service.find_player_id_by_nickname')
    def test_link_player_profile_and_tournament(self, mock_find_player_id_by_nickname, mock_insert_query):

        player_nicknames = ['Nickname1', 'Nickname2']
        tournament = MagicMock()
        tournament.id = 1
        player_ids = [101, 102]
        mock_find_player_id_by_nickname.side_effect = player_ids

        link_player_profile_and_tournament(player_nicknames, tournament)

        expected_calls = [
            unittest.mock.call(nickname) for nickname in player_nicknames
        ]
        mock_find_player_id_by_nickname.assert_has_calls(expected_calls)

        expected_insert_calls = [
            unittest.mock.call(
                """INSERT INTO tournaments_has_player_profile(tournaments_id, player_profile_id) VALUES (?, ?)""",
                (tournament.id, player_id)
            ) for player_id in player_ids
        ]
        mock_insert_query.assert_has_calls(expected_insert_calls, any_order=True)

    @patch('services.tournaments_service.get_all_matches_in_tournament_by_id')
    @patch('services.tournaments_service.read_query')
    def test_all(self, mock_read_query, mock_get_all_matches_in_tournament_by_id):

        mock_tournament_data = [
            (1, 'Tournament1', '2021-01-01', 'Knockout', 'Best of 3', 1000),
            (2, 'Tournament2', '2021-02-01', 'League', 'Best of 5', 2000)
        ]
        mock_nicknames_data = [
            [('Player1',), ('Player2',)],
            [('Player3',), ('Player4',)]
        ]
        mock_matches_data = [['Match1'], ['Match2']]
        mock_read_query.side_effect = [mock_tournament_data] + mock_nicknames_data
        mock_get_all_matches_in_tournament_by_id.side_effect = mock_matches_data

        result = all()

        self.assertEqual(len(result), len(mock_tournament_data))
        for i, tournament in enumerate(result):
            self.assertEqual(tournament['Name'], mock_tournament_data[i][1])
            self.assertEqual(tournament['Date'], mock_tournament_data[i][2])
            self.assertEqual(tournament['Tournament Format'], mock_tournament_data[i][3])
            self.assertEqual(tournament['Matches Format'], mock_tournament_data[i][4])
            self.assertEqual(tournament['Prize'], f"{mock_tournament_data[i][5]}$")
            self.assertEqual(tournament['Players\' Nicknames'], ", ".join(nick[0] for nick in mock_nicknames_data[i]))
            self.assertEqual(tournament['Matches'], mock_matches_data[i])



if __name__ == '__main__':
    unittest.main()
