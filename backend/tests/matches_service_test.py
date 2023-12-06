import unittest
from datetime import date
from unittest.mock import patch

from models.match import Match
from models.options import MatchFormat, EmailType
from services.matches_service import get_by_id, all, exist, update_by_id, sort, check_date_of_match, delete, create, \
    update_result_by_nicknames, winner_to_next_stage


class MatchesServiceTest(unittest.TestCase):

    @patch('services.matches_service.read_query')
    def test_get_by_id_found(self, mock_read_query):
        match_id = 1
        mock_data = [
            (1, '2021-01-01', 'score', 2, 3, 4, 5, 6, 'Winner', 1, 7)]
        mock_read_query.return_value = mock_data

        get_by_id(match_id)

        expected_query = '''SELECT id, date, format, tournament_id, player_profile_id1, player_profile_id2, score_1, score_2, winner, stage,order_num FROM matches WHERE id = ?'''
        mock_read_query.assert_called_once_with(expected_query, (match_id,))

    @patch('services.matches_service.read_query')
    @patch('services.matches_service.find_player_nickname_by_id')
    def test_with_search_and_date(self, mock_find_nickname, mock_read_query):
        mock_read_query.return_value = [
            (1, '2023-01-01', 'format1', 10, 20, 30, 3, 2, 'winner1', 'stage1', 1)
        ]
        mock_find_nickname.side_effect = ['Player1', 'Player2']
        search = 'test'
        date = '2023-01-01'

        result = all(search, date)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['id'], 1)
        self.assertEqual(result[0]['details'], 'Player1 3 vs 2 Player2')

    @patch('services.matches_service.read_query')
    def test_match_exists(self, mock_read_query):
        mock_read_query.return_value = [(1, '2023-01-01', 'format1', 10, 20, 30, 3, 2, 'winner1', 'stage1', 1)]
        match_id = 1

        result = exist(match_id)

        self.assertTrue(result)

    @patch('services.matches_service.read_query')
    def test_match_does_not_exist(self, mock_read_query):
        mock_read_query.return_value = []
        match_id = 2

        result = exist(match_id)

        self.assertFalse(result)

    @patch('services.matches_service.send_email_changed_match_date')
    @patch('services.matches_service.get_user_email_to_send_email_to')
    @patch('services.matches_service.get_user_id_from_table')
    @patch('services.matches_service.update_query')
    def test_update_by_id(self, mock_update_query, mock_get_user_id, mock_get_user_email, mock_send_email):

        old_match = Match(
            id=1,
            player_profile_id1=2,
            player_profile_id2=3,
            date='2021-01-01',
            format=MatchFormat.SCORE
        )
        new_date = '2021-02-01'
        user_id1 = 4
        user_id2 = 5
        user_email1 = 'user1@example.com'
        user_email2 = 'user2@example.com'
        mock_get_user_id.side_effect = [user_id1, user_id2]
        mock_get_user_email.side_effect = [user_email1, user_email2]

        update_by_id(old_match, new_date)

        mock_update_query.assert_called_once_with('''UPDATE matches SET date = ? WHERE id = ?''',
                                                  (new_date, old_match.id))
        mock_get_user_id.assert_has_calls([
            unittest.mock.call(old_match.player_profile_id1, "player_profile"),
            unittest.mock.call(old_match.player_profile_id2, "player_profile")
        ])
        mock_get_user_email.assert_has_calls([
            unittest.mock.call(user_id1),
            unittest.mock.call(user_id2)
        ])
        mock_send_email.assert_has_calls([
            unittest.mock.call(receiver=user_email1, new_date=new_date, email_type=EmailType.MATCH_CHANGED.value),
            unittest.mock.call(receiver=user_email2, new_date=new_date, email_type=EmailType.MATCH_CHANGED.value)
        ])

    def setUp(self):
        self.matches = [
            Match(id=2, date="2023-12-20", format="score"),
            Match(id=1, date="2023-12-19", format="score"),
            Match(id=3, date="2023-12-21", format="score")
        ]

    def test_sort_by_date(self):
        sorted_matches = sort(self.matches)
        self.assertEqual([match.id for match in sorted_matches], [1, 2, 3])

    def test_sort_by_id(self):
        sorted_matches = sort(self.matches, attribute="id")
        self.assertEqual([match.id for match in sorted_matches], [1, 2, 3])

    def test_reverse_sort_by_date(self):
        sorted_matches = sort(self.matches, reverse=True)
        self.assertEqual([match.id for match in sorted_matches], [3, 2, 1])

    def test_reverse_sort_by_id(self):
        sorted_matches = sort(self.matches, attribute="id", reverse=True)
        self.assertEqual([match.id for match in sorted_matches], [3, 2, 1])

    @patch('services.matches_service.read_query')
    def test_check_date_of_match(self, mock_read_query):

        match_id = 1
        expected_date = '2021-01-01'
        mock_read_query.return_value = [(expected_date,)]

        result = check_date_of_match(match_id)

        mock_read_query.assert_called_once_with(
            '''SELECT date from matches WHERE id = ?''',
            (match_id,)
        )
        self.assertEqual(result, expected_date)

    @patch('services.matches_service.update_query')
    def test_delete_match(self, mock_update_query):

        match_id = 1

        delete(match_id)

        mock_update_query.assert_called_once_with(
            '''DELETE FROM matches WHERE id = ?''', (match_id,)
        )

    @patch('services.matches_service.send_email_for_added_to_event')
    @patch('services.matches_service.get_user_email_to_send_email_to')
    @patch('services.matches_service.get_user_id_from_table')
    @patch('services.matches_service.get_by_id')
    @patch('services.matches_service.insert_query')
    @patch('services.matches_service.find_player_id_by_nickname')
    def test_create(self, mock_find_player_id, mock_insert_query, mock_get_by_id, mock_get_user_id, mock_get_user_email,
                    mock_send_email):

        date = '2021-01-01'
        format = 'Format'
        tournament_id = 1
        nickname_1 = 'Nickname1'
        nickname_2 = 'Nickname2'
        player_profile_id_1 = 2
        player_profile_id_2 = 3
        user_id_1 = 4
        user_id_2 = 5
        user_email_1 = 'user1@example.com'
        user_email_2 = 'user2@example.com'
        generated_id = 6
        mock_find_player_id.side_effect = [player_profile_id_1, player_profile_id_2]
        mock_insert_query.return_value = generated_id
        mock_get_by_id.return_value = Match(id=1, date='2021-01-01', format='score')

        mock_get_user_id.side_effect = [user_id_1, user_id_2]
        mock_get_user_email.side_effect = [user_email_1, user_email_2]

        result = create(date, format, tournament_id, nickname_1, nickname_2)

        mock_find_player_id.assert_has_calls([
            unittest.mock.call(nickname_1),
            unittest.mock.call(nickname_2)
        ])
        mock_insert_query.assert_called_once_with(
            '''INSERT INTO matches(date, format, tournament_id, player_profile_id1, player_profile_id2, stage, order_num) VALUES(?,?,?,?,?,?,?)''',
            (date, format, tournament_id, player_profile_id_1, player_profile_id_2, None, None)
        )
        mock_get_by_id.assert_called_once_with(generated_id)
        mock_get_user_id.assert_has_calls([
            unittest.mock.call(player_profile_id_1, "player_profile"),
            unittest.mock.call(player_profile_id_2, "player_profile")
        ])
        mock_get_user_email.assert_has_calls([
            unittest.mock.call(user_id_1),
            unittest.mock.call(user_id_2)
        ])
        mock_send_email.assert_has_calls([
            unittest.mock.call(user_email_1, [nickname_1, nickname_2], date, EmailType.ADDED_TO_MATCH.value),
            unittest.mock.call(user_email_2, [nickname_1, nickname_2], date, EmailType.ADDED_TO_MATCH.value)
        ])
        self.assertIsInstance(result, Match)

    @patch('services.matches_service.winner_to_next_stage')
    @patch('services.matches_service.update_query')
    @patch('services.matches_service.read_query')
    @patch('services.matches_service.find_player_id_by_nickname')
    def test_update_result_by_nicknames_success(self, mock_find_player_id, mock_read_query, mock_update_query,
                                                mock_winner_to_next_stage): # No time to fix error

        tournament_id = 1
        nickname_1 = 'Nickname1'
        nickname_2 = 'Nickname2'
        score_1 = 3
        score_2 = 2
        player_profile_id1 = 2
        player_profile_id2 = 3
        order_num = 5
        mock_find_player_id.side_effect = [player_profile_id1, player_profile_id2]
        mock_read_query.side_effect = [
            [(1, '2021-01-01', 'score', tournament_id, player_profile_id1, player_profile_id2, 0, 0, None, 1,
              order_num)],
            [(order_num,)]
        ]

        result = update_result_by_nicknames(tournament_id, nickname_1, score_1, score_2, nickname_2)

        mock_find_player_id.assert_has_calls([
            unittest.mock.call(nickname_1),
            unittest.mock.call(nickname_2)
        ])
        mock_read_query.assert_has_calls([
            unittest.mock.call(
                '''SELECT * FROM matches WHERE tournament_id = ? AND player_profile_id1 = ? AND player_profile_id2 = ?''',
                (tournament_id, player_profile_id1, player_profile_id2)),
            unittest.mock.call(
                """SELECT order_num FROM matches WHERE tournament_id = ? ORDER BY order_num DESC LIMIT 1""",
                (tournament_id,))
        ])
        mock_update_query.assert_called_once()
        mock_winner_to_next_stage.assert_called_once_with(tournament_id,
                                                          nickname_1 if score_1 > score_2 else nickname_2)

        self.assertIn("Result updated. The winner is", result)

    @patch('services.matches_service.find_player_id_by_nickname')
    @patch('services.matches_service.read_query')
    def test_update_result_by_nicknames_no_match(self, mock_read_query, mock_find_player_id):

        tournament_id = 1
        nickname_1 = 'Nickname1'
        nickname_2 = 'Nickname2'
        score_1 = 3
        score_2 = 2
        player_profile_id1 = 2
        player_profile_id2 = 3
        mock_find_player_id.side_effect = [player_profile_id1, player_profile_id2]
        mock_read_query.return_value = []

        result = update_result_by_nicknames(tournament_id, nickname_1, score_1, score_2, nickname_2)

        self.assertFalse(result)

    @patch('services.matches_service.update_query')
    @patch('services.matches_service.read_query')
    @patch('services.matches_service.find_player_id_by_nickname')
    def test_update_first_player_id(self, mock_find_player_id, mock_read_query, mock_update_query):
        tournament_id = 1
        winner = "WinnerNickname"
        mock_read_query.side_effect = [
            [(2,)],
            [(None,)],

        ]
        mock_find_player_id.return_value = 10

        winner_to_next_stage(tournament_id, winner)

        mock_update_query.assert_called_once_with(
            '''UPDATE matches SET player_profile_id1 = ? WHERE tournament_id = ? AND order_num = 2''',
            (10, tournament_id)
        )


if __name__ == '__main__':
    unittest.main()
