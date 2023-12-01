from database.database_connection import read_query, update_query, insert_query
from fastapi import HTTPException
from models.user import User
from authentication.auth import find_by_email, get_user_or_raise_401
from models.options import Role, CurrentStatus, EmailType
from models.requests import LinkRequest, PromoteRequest
from services import utilities
from emails_logic.emails import send_email_for_requests
from services.utilities import get_user_email_to_send_email_to, get_user_id_from_table


def _hash_password(password: str):
    """ Used to hash a password of a user before saving it in the database."""
    from hashlib import sha256
    return sha256(password.encode('utf-8')).hexdigest()


def try_login(email: str, password: str) -> User | None:
    """ Used to hash the login password and compare it with the existing password of the user in the database."""

    user = find_by_email(email)

    password = _hash_password(password)
    return user if user and user.password == password else None


def create(email: str, password: str) -> User | None:
    """ Used to save the already hashed password to the database."""

    password = _hash_password(password)

    generated_id = insert_query(
        '''INSERT INTO users(email, password, user_type) VALUES (?,?,?)''',
        (email, password, Role.USER.value))

    return User(id=generated_id, email=email, password='', role=Role.USER.value)


def delete_user(id: int):
    """ Used for deleting the user from the database."""

    insert_query('''DELETE FROM users WHERE id = ?''',
                 (id,))


def edit_user_type(old_user: User, new_user: User):
    """ Used for editing by an admin a role of a user in the database."""

    edited_user = User(
        id=old_user.id,
        email=old_user.email,
        password=old_user.password,
        user_type=new_user.user_type
    )

    update_query('''UPDATE users SET user_type = ? WHERE id = ?''',
                 (edited_user.user_type, edited_user.id))

    return {"User's role updated."}


def is_admin(user: User):
    """ Compares the user's role if it's an admin when a JWT token is written in the Header.
    Returns:
        - True/False
    """
    return user.user_type == Role.ADMIN


#  ............There is no need for this functionality at this time............
# def all_users():
#     data = read_query(
#         '''SELECT id, email, user_type FROM users''')
#     if data is None:
#         return None
#
#     return (User.from_query_result_no_password(*row) for row in data)


def get_by_id(id: int):
    data = read_query(
        '''SELECT id, email, user_type, player_profile_id
        FROM users
        WHERE id = ?''', (id,))
    return next((User.from_query_result_no_password(*row) for row in data), None)


def find_by_id_admin(id: int) -> User | None:
    """ Search through users.id the whole information about the account in the data. Only admins can search for them.

    Args:
        - id: int

    Returns:
        - all the necessary information about the user (id, username, hashed password, role and etc.)
    """

    data = read_query(
        '''SELECT id, email, user_type FROM users WHERE id = ?''',
        (id,))

    return next((User.from_query_result_no_password(*row) for row in data), None)


def is_director(user: User):
    """
    Compares the user's role if it's an admin when a JWT token is written in the Header.
    Returns:
        - True/False
    """

    return user.user_type == Role.DIRECTOR


def create_link_request(user_id: int, player_profile_id: int):
    """

    Args:
        user_id:
        player_profile_id:

    Returns:
        - returns the Link

    """
    profile_link_status = read_query(
        '''SELECT users_id FROM player_profile WHERE id = ?''',
        (player_profile_id,)
    )

    if profile_link_status and profile_link_status[0][0] and profile_link_status[0][0] != user_id:
        raise HTTPException(status_code=409, detail="This profile is already linked to another user.")

    link_request_id = insert_query(
        '''INSERT INTO link_requests (user_id, player_profile_id, status) VALUES (?, ?, ?)''',
        (user_id, player_profile_id, CurrentStatus.PENDING.value))
    return LinkRequest(id=link_request_id, user_id=user_id, player_profile_id=player_profile_id,
                       status=CurrentStatus.PENDING.value)


def approve_link_request(link_request_id: int) -> str:
    """
    Approve a link request, updating both the player_profile and users tables.

    Args:
        - link_request_id: int

    Returns:
        - A message indicating success.
    """

    link_request_data = read_query(
        '''SELECT status, user_id, player_profile_id FROM link_requests WHERE id = ?''',
        (link_request_id,)
    )

    if not link_request_data:
        raise HTTPException(status_code=404, detail=f"No link request with ID: {link_request_id} exists.")

    current_status, user_id, player_profile_id = link_request_data[0]


    if current_status == CurrentStatus.DENIED.value:
        raise HTTPException(status_code=404, detail="Status cannot be changed from approved to denied and vice versa.")

    update_query(
        "UPDATE player_profile SET users_id = ? WHERE id = ?",
        (user_id, player_profile_id)
    )

    update_query(
        "UPDATE link_requests SET status = ? WHERE id = ?",
        (CurrentStatus.APPROVED.value, link_request_id,)
    )

    user_email = get_user_email_to_send_email_to(user_id)

    send_email_for_requests(receiver=user_email, conformation=CurrentStatus.APPROVED.value,
                            email_type=EmailType.LINK_REQUEST.value)

    return "Link request approved."


def deny_link_request(link_request_id: int) -> str:
    """
    Deny a link request, updating the status of the request.

    Args:
        - link_request_id: int

    Returns:
        - A message indicating failure.
    """
    link_request_data = read_query(
        "SELECT status FROM link_requests WHERE id = ?",
        (link_request_id,)
    )

    current_status = link_request_data[0][0]

    if current_status == CurrentStatus.APPROVED.value:
        raise HTTPException(status_code=404, detail="Status cannot be changed from denied to approved and vice versa.")

    if not utilities.id_exists(link_request_id, "link_requests"):
        raise HTTPException(status_code=404, detail=f"No link request with ID: {link_request_id} exists.")

    update_query("UPDATE link_requests SET status = ? WHERE id = ?", (CurrentStatus.DENIED.value, link_request_id))

    user_id = get_user_id_from_table(link_request_id, "link_requests")
    user_email = get_user_email_to_send_email_to(user_id)

    send_email_for_requests(receiver=user_email, conformation=CurrentStatus.DENIED.value,
                            email_type=EmailType.LINK_REQUEST.value)

    return "Link request denied"


def create_promotion_request(user_id: int):
    """
    Creates a new promotion request in the database.

    Args:
        user_id: int

    Returns:
        A message indicating the creation of the request.
    """

    existing_request = read_query(
        "SELECT id FROM promote_requests WHERE users_id = ? AND status = ?",
        (user_id, CurrentStatus.PENDING.value)
    )

    if existing_request:
        raise HTTPException(status_code=409, detail="A pending promotion request already exists for this user.")

    promotion_request_id = insert_query(
        'INSERT INTO promote_requests (users_id, status) VALUES (?, ?)',
        (user_id, CurrentStatus.PENDING.value)
    )

    return PromoteRequest(id=promotion_request_id, user_id=user_id, status=CurrentStatus.PENDING.value)


def approve_promote_request(promote_request_id: int) -> str:
    """
    Approve a promotion request, updating the status in the promotion_requests table.

    Args:
        - promote_request_id: int

    Returns:
        - A message indicating success.
    """

    promote_request_data = read_query(
        "SELECT status, users_id FROM promote_requests WHERE id = ?",
        (promote_request_id,)
    )

    if not promote_request_data:
        raise HTTPException(status_code=404, detail=f"No promote request with ID: {promote_request_id} exists.")

    current_status, user_id = promote_request_data[0]

    if current_status != CurrentStatus.PENDING.value:
        raise HTTPException(status_code=409, detail="Cannot change the status of a request that is already processed.")

    update_query(
        "UPDATE users SET user_type = ? WHERE id = ?",
        (Role.DIRECTOR.value, user_id)
    )

    update_query(
        "UPDATE promote_requests SET status = ? WHERE id = ?",
        (CurrentStatus.APPROVED.value, promote_request_id,)
    )

    player_profile_id_list = read_query("SELECT id FROM player_profile WHERE users_id=?", (user_id,))
    if player_profile_id_list:
        player_profile_id = player_profile_id_list[0][0]
        update_query("UPDATE player_profile SET users_id = NULL WHERE id=?", (player_profile_id,))

    user_email = get_user_email_to_send_email_to(user_id)

    send_email_for_requests(receiver=user_email, conformation=CurrentStatus.APPROVED.value,
                            email_type=EmailType.PROMOTE_REQUEST.value)

    return "Promotion request approved."


def deny_promote_request(promote_request_id: int) -> str:
    """
    Deny a promotion request, updating the status in the promotion_requests table.

    Args:
        - promote_request_id: int

    Returns:
        - A message indicating the request was denied.
    """

    promote_request_data = read_query(
        "SELECT status FROM promote_requests WHERE id = ?",
        (promote_request_id,)
    )

    if not promote_request_data:
        raise HTTPException(status_code=404, detail=f"No promotion request with ID: {promote_request_id} exists.")

    current_status = promote_request_data[0][0]

    if current_status != CurrentStatus.PENDING.value:
        raise HTTPException(status_code=409, detail="Cannot change the status of a request that is already processed.")

    update_query(
        "UPDATE promote_requests SET status = ? WHERE id = ?",
        (CurrentStatus.DENIED.value, promote_request_id,)
    )

    user_id = get_user_id_from_table(promote_request_id, "promote_requests")
    user_email = get_user_email_to_send_email_to(user_id)

    send_email_for_requests(receiver=user_email, conformation=CurrentStatus.DENIED.value,
                            email_type=EmailType.PROMOTE_REQUEST.value)

    return "Promotion request denied."
