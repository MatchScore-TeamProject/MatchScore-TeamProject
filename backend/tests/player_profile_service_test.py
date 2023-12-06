import unittest
from unittest.mock import patch

from fastapi import HTTPException

from models.player_profile import PlayerProfile
from services.player_profile_service import create_player_profile, delete_player_profile, edit_player_profile, \
    find_non_existing_players, view_player_profile, validate_name

profile_data = PlayerProfile.from_query_result(
    id=1,
    nickname="CurrentNickname",
    full_name="Current Full Name",
    country="Current Country",
    sports_club="Current Sports Club",
    user_id=100
)

new_profile_data = PlayerProfile(
    id=1,
    nickname="NewNickname",
    full_name="New Full Name",
    country="New Country",
    sports_club="New Sports Club",
    user_id=100
)


class PlayerProfileTest(unittest.TestCase):

    @patch('services.player_profile_service.validate_name')
    @patch('services.player_profile_service.insert_query')
    def test_create_player_profile(self, mock_insert_query, mock_validate_name):

        nickname = 'unique_test_nickname'
        full_name = 'Test Full Name'
        country = 'Test Country'
        sports_club = 'Test Club'
        user_id = 1
        mock_insert_query.return_value = 456

        result = create_player_profile(nickname, full_name, country, sports_club, user_id)

        mock_validate_name.assert_called_once_with(full_name)
        mock_insert_query.assert_called_once_with(
            """INSERT INTO player_profile(nickname, full_name, country, sports_club, users_id) VALUES (?,?,?,?,?)""",
            (nickname, full_name, country, sports_club, user_id)
        )
        self.assertIsInstance(result, PlayerProfile)
        self.assertEqual(result.id, 456)
        self.assertEqual(result.nickname, nickname)
        self.assertEqual(result.full_name, full_name)
        self.assertEqual(result.country, country)
        self.assertEqual(result.sports_club, sports_club)
        self.assertEqual(result.user_id, user_id)

    @patch('services.player_profile_service.insert_query')
    def test_delete_player_profile(self, mock_insert_query):

        player_profile_id = 123

        delete_player_profile(player_profile_id)

        mock_insert_query.assert_called_once_with(
            '''DELETE FROM player_profile WHERE id = ?''',
            (player_profile_id,)
        )

    @patch('services.player_profile_service.read_query')
    def test_edit_player_profile_success(self, mock_read_query):

        player_profile_id = 1
        new_data = new_profile_data
        user_id = 100
        user_type = 'director'
        mock_read_query.return_value = [(
            profile_data.nickname,
            profile_data.full_name,
            profile_data.country,
            profile_data.sports_club,
            profile_data.user_id
        )]

        try:
            edit_player_profile(player_profile_id, new_data, user_id, user_type)
        except HTTPException:
            self.fail("HTTPException was raised")

    @patch('services.player_profile_service.read_query')
    def test_edit_player_profile_not_found(self, mock_read_query):
        mock_read_query.return_value = []

        with self.assertRaises(HTTPException) as context:
            edit_player_profile(123, new_profile_data, 456, 'director')

        self.assertEqual(context.exception.status_code, 404)

    @patch('services.player_profile_service.read_query')
    def test_edit_player_profile_no_permission(self, mock_read_query):
        mock_read_query.return_value = [
            (
                profile_data.nickname,
                profile_data.full_name,
                profile_data.country,
                profile_data.sports_club,
                profile_data.user_id
            )
        ]
        user_id = 789

        with self.assertRaises(HTTPException) as context:
            edit_player_profile(123, new_profile_data, user_id, 'some_type')

        self.assertEqual(context.exception.status_code, 403)

    @patch('services.player_profile_service.read_query')
    def test_find_non_existing_players(self, mock_read_query):
        mock_read_query.return_value = [('Player1',), ('Player2',), ('Player3',)]

        player_profiles = ['Player2', 'Player4', 'Player5']

        expected_non_existing_players = ['Player4', 'Player5']

        non_existing_players = find_non_existing_players(player_profiles)

        self.assertEqual(non_existing_players, expected_non_existing_players)

    @patch('services.player_profile_service.read_query')
    def test_all_players_exist(self, mock_read_query):

        mock_read_query.return_value = [('Player1',), ('Player2',), ('Player3',)]

        player_profiles = ['Player1', 'Player2', 'Player3']

        non_existing_players = find_non_existing_players(player_profiles)

        self.assertIsNone(non_existing_players)

    @patch('services.player_profile_service.read_query')
    def test_view_player_profile_found(self, mock_read_query):
        mock_read_query.return_value = [('Nickname', 'Full Name Name', 'Country', 'Sports Club')]
        player_data = 'Nickname'

        result = view_player_profile(player_data)

        self.assertEqual(result, ('Nickname', 'Full Name Name', 'Country', 'Sports Club'))

    @patch('services.player_profile_service.read_query')
    def test_view_player_profile_not_found(self, mock_read_query):

        mock_read_query.return_value = []
        player_data = 'NonexistentNickname'

        with self.assertRaises(HTTPException) as context:
            view_player_profile(player_data)

        self.assertEqual(context.exception.status_code, 404)

    def test_validate_name_valid(self):
        valid_names = ['John Doe Smith', 'Alice Bob Carol']

        for name in valid_names:
            try:
                validate_name(name)
            except HTTPException:
                self.fail(f"HTTPException was raised for valid name: {name}")

    def test_validate_name_invalid(self):
        invalid_names = ['John', 'John123 Doe', 'John_Doe_Smith', ' ']

        for name in invalid_names:
            with self.assertRaises(HTTPException) as context:
                validate_name(name)
            self.assertEqual(context.exception.status_code, 422)


if __name__ == '__main__':
    unittest.main()
