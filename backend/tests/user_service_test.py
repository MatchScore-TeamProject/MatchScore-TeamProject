import unittest
from unittest.mock import patch

from fastapi import HTTPException

from models.options import Role, CurrentStatus, EmailType
from models.requests import LinkRequest, PromoteRequest
from models.user import User
from services.user_service import _hash_password, try_login, create, delete_user, edit_user_type, is_admin, get_by_id, \
    find_by_id_admin, is_director, create_link_request, approve_link_request, deny_link_request, \
    create_promotion_request, approve_promote_request, deny_promote_request


class UserServiceTest(unittest.TestCase):
    def test_hash_password(self):
        password = "TestPassword123"
        expected_hash = "d519397a4e89a7a66d28a266ed00a679bdee93fddec9ebba7d01ff27c39c1a99"

        result_hash = _hash_password(password)

        self.assertEqual(result_hash, expected_hash)

    @patch('services.user_service.find_by_email')
    @patch('services.user_service._hash_password')
    def test_try_login_success(self, mock_hash_password, mock_find_by_email):
        test_email = "test@example.com"
        test_password = "TestPassword123"
        hashed_password = "hashed_test_password"
        mock_user = User(email=test_email, password=hashed_password)
        mock_find_by_email.return_value = mock_user
        mock_hash_password.return_value = hashed_password

        result = try_login(test_email, test_password)

        self.assertIsNotNone(result)
        self.assertEqual(result.email, test_email)
        self.assertEqual(result.password, hashed_password)

    @patch('services.user_service.find_by_email')
    @patch('services.user_service._hash_password')
    def test_try_login_failure(self, mock_hash_password, mock_find_by_email):
        # Arrange
        test_email = "test@example.com"
        test_password = "TestPassword123"
        wrong_hashed_password = "wrong_hashed_password"
        mock_find_by_email.return_value = None
        mock_hash_password.return_value = wrong_hashed_password

        result = try_login(test_email, test_password)

        self.assertIsNone(result)

    @patch('services.user_service.insert_query')
    @patch('services.user_service._hash_password')
    def test_create_user(self, mock_hash_password, mock_insert_query):
        test_email = "test@example.com"
        test_password = "TestPassword123"
        hashed_password = "hashed_test_password"
        mock_hash_password.return_value = hashed_password
        generated_id = 1
        mock_insert_query.return_value = generated_id

        result = create(test_email, test_password)

        mock_insert_query.assert_called_once_with(
            '''INSERT INTO users(email, password, user_type) VALUES (?,?,?)''',
            (test_email, hashed_password, Role.USER.value)
        )
        self.assertIsInstance(result, User)
        self.assertEqual(result.id, generated_id)
        self.assertEqual(result.email, test_email)
        self.assertEqual(result.password, '')
        self.assertEqual(result.user_type, Role.USER.value)

    @patch('services.user_service.insert_query')
    def test_delete_user(self, mock_insert_query):
        user_id = 123

        delete_user(user_id)

        mock_insert_query.assert_called_once_with(
            '''DELETE FROM users WHERE id = ?''',
            (user_id,)
        )

    @patch('services.user_service.update_query')
    def test_edit_user_type(self, mock_update_query):
        # Arrange
        old_user = User(id=1, email="old@example.com", password="oldpassword", user_type=Role.USER.value)
        new_user = User(id=1, email="new@example.com", password="newpassword", user_type=Role.ADMIN.value)
        response = edit_user_type(old_user, new_user)

        mock_update_query.assert_called_once_with(
            '''UPDATE users SET user_type = ? WHERE id = ?''',
            (new_user.user_type, old_user.id)
        )
        self.assertEqual(response, {"User's role updated."})

    def test_is_admin_true(self):
        admin_user = User(id=1, email="admin@example.com", password="adminpassword", user_type=Role.ADMIN.value)

        result = is_admin(admin_user)

        self.assertTrue(result)

    def test_is_admin_false(self):
        non_admin_user = User(id=2, email="user@example.com", password="userpassword", user_type=Role.USER.value)

        result = is_admin(non_admin_user)

        self.assertFalse(result)

    @patch('services.user_service.read_query')
    def test_get_by_id_found(self, mock_read_query):
        # Arrange
        user_id = 1
        mock_data = [(1, 'user@example.com', 'user', None)]  # Example data returned from the database
        mock_read_query.return_value = mock_data

        # Act
        result = get_by_id(user_id)

        mock_read_query.assert_called_once_with(
            '''SELECT id, email, user_type, player_profile_id FROM users WHERE id = ?''', (user_id,))

        self.assertIsInstance(result, User)
        self.assertEqual(result.id, 1)
        self.assertEqual(result.email, 'user@example.com')
        self.assertEqual(result.user_type, 'user')
        self.assertIsNone(result.player_profile_id)

    @patch('services.user_service.read_query')
    def test_get_by_id_not_found(self, mock_read_query):
        # Arrange
        user_id = 2
        mock_read_query.return_value = []  # No data found for this user ID

        # Act
        result = get_by_id(user_id)

        # Assert
        self.assertIsNone(result)

    @patch('services.user_service.read_query')
    def test_find_by_id_admin_found(self, mock_read_query):
        # Arrange
        user_id = 1
        mock_data = [(1, 'admin@example.com', "", 'admin')]  # Example data returned from the database
        mock_read_query.return_value = mock_data

        # Act
        result = find_by_id_admin(user_id)

        # Assert
        mock_read_query.assert_called_once_with('''SELECT id, email, user_type FROM users WHERE id = ?''', (user_id,))
        self.assertIsInstance(result, User)
        self.assertEqual(result.id, 1)
        self.assertEqual(result.email, 'admin@example.com')
        self.assertEqual(result.user_type, 'admin')

    def test_is_director_true(self):
        director_user = User(id=1, email="director@example.com", password="directorpassword",
                             user_type=Role.DIRECTOR.value)

        result = is_director(director_user)

        self.assertTrue(result)

    def test_is_director_false(self):
        # Arrange
        non_director_user = User(id=2, email="user@example.com", password="userpassword", user_type=Role.USER.value)

        # Act
        result = is_director(non_director_user)

        # Assert
        self.assertFalse(result)

    @patch('services.user_service.insert_query')
    @patch('services.user_service.read_query')
    def test_create_link_request_success(self, mock_read_query, mock_insert_query):
        # Arrange
        user_id = 1
        player_profile_id = 2
        mock_read_query.return_value = [(None,)]
        link_request_id = 123
        mock_insert_query.return_value = link_request_id

        result = create_link_request(user_id, player_profile_id)

        mock_read_query.assert_called_once_with(
            '''SELECT users_id FROM player_profile WHERE id = ?''',
            (player_profile_id,)
        )
        mock_insert_query.assert_called_once_with(
            '''INSERT INTO link_requests (user_id, player_profile_id, status) VALUES (?, ?, ?)''',
            (user_id, player_profile_id, CurrentStatus.PENDING.value)
        )
        self.assertIsInstance(result, LinkRequest)
        self.assertEqual(result.id, link_request_id)
        self.assertEqual(result.user_id, user_id)
        self.assertEqual(result.player_profile_id, player_profile_id)
        self.assertEqual(result.status, CurrentStatus.PENDING.value)

    @patch('services.user_service.read_query')
    def test_create_link_request_already_linked(self, mock_read_query):
        user_id = 1
        player_profile_id = 2
        another_user_id = 3
        mock_read_query.return_value = [
            (another_user_id,)]

        with self.assertRaises(HTTPException) as context:
            create_link_request(user_id, player_profile_id)

        self.assertEqual(context.exception.status_code, 409)

    @patch('services.user_service.send_email_for_requests')
    @patch('services.user_service.get_user_email_to_send_email_to')
    @patch('services.user_service.update_query')
    @patch('services.user_service.read_query')
    def test_approve_link_request_success(self, mock_read_query, mock_update_query, mock_get_user_email,
                                          mock_send_email):
        # Arrange
        link_request_id = 1
        user_id = 2
        player_profile_id = 3
        mock_read_query.return_value = [
            (CurrentStatus.PENDING.value, user_id, player_profile_id)]  # Simulating link request data
        mock_get_user_email.return_value = 'user@example.com'

        result = approve_link_request(link_request_id)

        self.assertEqual(result, "Link request approved.")
        mock_read_query.assert_called_once_with(
            '''SELECT status, user_id, player_profile_id FROM link_requests WHERE id = ?''',
            (link_request_id,)
        )
        mock_update_query.assert_has_calls([
            unittest.mock.call("UPDATE player_profile SET users_id = ? WHERE id = ?", (user_id, player_profile_id)),
            unittest.mock.call("UPDATE link_requests SET status = ? WHERE id = ?",
                               (CurrentStatus.APPROVED.value, link_request_id))
        ])
        mock_send_email.assert_called_once_with(receiver='user@example.com', conformation=CurrentStatus.APPROVED.value,
                                                email_type=EmailType.LINK_REQUEST.value)

    @patch('services.user_service.read_query')
    def test_approve_link_request_not_found(self, mock_read_query):
        link_request_id = 1
        mock_read_query.return_value = []

        with self.assertRaises(HTTPException) as context:
            approve_link_request(link_request_id)

        self.assertEqual(context.exception.status_code, 404)

    @patch('services.user_service.read_query')
    def test_approve_link_request_denied(self, mock_read_query):
        # Arrange
        link_request_id = 1
        user_id = 2
        player_profile_id = 3
        mock_read_query.return_value = [(CurrentStatus.DENIED.value, user_id, player_profile_id)]

        with self.assertRaises(HTTPException) as context:
            approve_link_request(link_request_id)

        self.assertEqual(context.exception.status_code, 404)

    @patch('services.user_service.read_query')
    @patch('services.user_service.update_query')
    @patch('services.user_service.utilities')
    @patch('services.user_service.get_user_id_from_table')
    @patch('services.user_service.get_user_email_to_send_email_to')
    @patch('services.user_service.send_email_for_requests')
    def test_deny_existing_request(self, mock_send_email, mock_get_user_email, mock_get_user_id, mock_utilities,
                                   mock_update_query, mock_read_query):
        mock_read_query.return_value = [(CurrentStatus.PENDING.value,)]
        mock_utilities.id_exists.return_value = True

        response = deny_link_request(1)

        self.assertEqual(response, "Link request denied")
        mock_update_query.assert_called_once()
        mock_send_email.assert_called_once()

    @patch('services.user_service.read_query')
    def test_deny_approved_request(self, mock_read_query):
        mock_read_query.return_value = [(CurrentStatus.APPROVED.value,)]

        with self.assertRaises(HTTPException):
            deny_link_request(1)

    @patch('services.user_service.utilities')
    def test_deny_nonexistent_request(self, mock_utilities):
        mock_utilities.id_exists.return_value = False

        with self.assertRaises(HTTPException):
            deny_link_request(1)

    @patch('services.user_service.read_query')
    @patch('services.user_service.insert_query')
    def test_create_new_promote_request(self, mock_insert_query, mock_read_query):
        user_id = 123
        mock_read_query.return_value = []
        mock_insert_query.return_value = 1

        result = create_promotion_request(user_id)

        self.assertIsInstance(result, PromoteRequest)
        self.assertEqual(result.user_id, user_id)
        self.assertEqual(result.status, CurrentStatus.PENDING.value)
        mock_insert_query.assert_called_once_with(
            'INSERT INTO promote_requests (users_id, status) VALUES (?, ?)',
            (user_id, CurrentStatus.PENDING.value)
        )

    @patch('services.user_service.read_query')
    def test_existing_promote_request_error(self, mock_read_query):
        user_id = 123
        mock_read_query.return_value = [(1,)]

        with self.assertRaises(HTTPException) as context:
            create_promotion_request(user_id)

        self.assertEqual(context.exception.status_code, 409)
        self.assertIn("A pending promotion request already exists", str(context.exception.detail))

    @patch('services.user_service.send_email_for_requests')
    @patch('services.user_service.get_user_email_to_send_email_to')
    @patch('services.user_service.update_query')
    @patch('services.user_service.read_query')
    def test_approve_promote_request_success(self, mock_read_query, mock_update_query, mock_get_user_email,
                                             mock_send_email):
        promote_request_id = 1
        user_id = 2
        player_profile_id = 3
        mock_read_query.side_effect = [
            [(CurrentStatus.PENDING.value, user_id)],
            [(player_profile_id,)]
        ]
        mock_get_user_email.return_value = 'user@example.com'

        result = approve_promote_request(promote_request_id)

        self.assertEqual(result, "Promotion request approved.")
        mock_read_query.assert_has_calls([
            unittest.mock.call("SELECT status, users_id FROM promote_requests WHERE id = ?", (promote_request_id,)),
            unittest.mock.call("SELECT id FROM player_profile WHERE users_id=?", (user_id,))
        ])
        mock_update_query.assert_has_calls([
            unittest.mock.call("UPDATE users SET user_type = ? WHERE id = ?", (Role.DIRECTOR.value, user_id)),
            unittest.mock.call("UPDATE promote_requests SET status = ? WHERE id = ?",
                               (CurrentStatus.APPROVED.value, promote_request_id)),
            unittest.mock.call("UPDATE player_profile SET users_id = NULL WHERE id=?", (player_profile_id,))
        ])
        mock_send_email.assert_called_once_with(receiver='user@example.com', conformation=CurrentStatus.APPROVED.value,
                                                email_type=EmailType.PROMOTE_REQUEST.value)

    @patch('services.user_service.read_query')
    def test_approve_promote_request_not_found(self, mock_read_query):
        promote_request_id = 1
        mock_read_query.return_value = []

        with self.assertRaises(HTTPException) as context:
            approve_promote_request(promote_request_id)

        self.assertEqual(context.exception.status_code, 404)

    @patch('services.user_service.read_query')
    def test_approve_promote_request_already_processed(self, mock_read_query):
        promote_request_id = 1
        mock_read_query.return_value = [(CurrentStatus.APPROVED.value, 2)]

        with self.assertRaises(HTTPException) as context:
            approve_promote_request(promote_request_id)

        self.assertEqual(context.exception.status_code, 409)

    @patch('services.user_service.read_query')
    @patch('services.user_service.update_query')
    @patch('services.user_service.get_user_id_from_table')
    @patch('services.user_service.get_user_email_to_send_email_to')
    @patch('services.user_service.send_email_for_requests')
    def test_deny_existing_pending_promote_request(self, mock_send_email, mock_get_user_email, mock_get_user_id,
                                                   mock_update_query, mock_read_query):
        mock_read_query.return_value = [(CurrentStatus.PENDING.value,)]
        promote_request_id = 1

        response = deny_promote_request(promote_request_id)

        self.assertEqual(response, "Promotion request denied.")
        mock_update_query.assert_called_once()
        mock_send_email.assert_called_once()

    @patch('services.user_service.read_query')
    def test_deny_nonexistent_promote_request(self, mock_read_query):

        mock_read_query.return_value = []
        promote_request_id = 1

        # Action & Assert
        with self.assertRaises(HTTPException):
            deny_promote_request(promote_request_id)

    @patch('services.user_service.read_query')
    def test_deny_processed_request(self, mock_read_query):

        mock_read_query.return_value = [(CurrentStatus.APPROVED.value,)]
        promote_request_id = 1

        with self.assertRaises(HTTPException):
            deny_promote_request(promote_request_id)


if __name__ == '__main__':
    unittest.main()
