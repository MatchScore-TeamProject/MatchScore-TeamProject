from database.database_connection import read_query, update_query, insert_query
from fastapi import HTTPException
from models.user import User
from authentication.auth import find_by_email
from models.options import Role, CurrentStatus, EmailType
from models.requests import LinkRequest, PromoteRequest
from services import utilities
from services.emails import send_email_for_requests
from services.utilities import get_user_email_to_send_email_to, get_user_id_from_table


def _hash_password(password: str):

    from hashlib import sha256
    return sha256(password.encode('utf-8')).hexdigest()


def try_login(email: str, password: str) -> User | None:

    user = find_by_email(email)

    password = _hash_password(password)
    return user if user and user.password == password else None


def create(email: str, password: str) -> User | None:

    password = _hash_password(password)

    generated_id = insert_query(
        '''INSERT INTO users(email, password, user_type) VALUES (?,?,?)''',
        (email, password, Role.USER.value))

    return User(id=generated_id, email=email, password='', role=Role.USER.value)


def delete_user(id: int):


    insert_query('''DELETE FROM users WHERE id = ?''',
                 (id,))


def edit_user_type(old_user: User, new_user: User):


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

    return user.user_type == Role.ADMIN


def get_by_id(id: int):
    data = read_query(
        '''SELECT id, email, user_type, player_profile_id FROM users WHERE id = ?''', (id,))
    return next((User.from_query_result_no_password(*row) for row in data), None)


def find_by_id_admin(id: int) -> User | None:


    data = read_query(
        '''SELECT id, email, user_type FROM users WHERE id = ?''',
        (id,))

    return next((User.from_query_result_no_password(*row) for row in data), None)


def is_director(user: User):

    return user.user_type == Role.DIRECTOR


def create_link_request(user_id: int, player_profile_id: int):

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

    link_request_data = read_query(
        "SELECT status FROM link_requests WHERE id = ?",
        (link_request_id,)
    )

    if not link_request_data:
        raise HTTPException(status_code=404, detail="No such requests exists.")


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
