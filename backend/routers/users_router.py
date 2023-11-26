from fastapi import APIRouter, Header, HTTPException, Query
from authentication.auth import find_by_id, get_user_or_raise_401, create_token
from models.user import User, LoginData
from services import user_service, utilities
from models.options import Role
from pydantic import EmailStr


users_router = APIRouter(prefix='/users', tags=['Users'])


@users_router.post('/register')
def register(email: EmailStr = Query(),
             password: str = Query()):
    """ Used for registering new users.

    Args:
        - LoginData(email, password(str))

    Returns:
        - Registered user
    """

    user = user_service.create(email, password)

    return user or HTTPException(status_code=400, detail=f'Email {email} is already taken.')


@users_router.post('/login')
def login(email: EmailStr = Query(),
          password: str = Query()):
    """ Used for logging in.

    Args:
        - LoginData(email, password(str))

    Returns:
        - JWT token
    """
    user = user_service.try_login(email, password)
    if user:
        token = create_token(user)
        return {'token': token}
    else:
        raise HTTPException(status_code=400, detail="Invalid login data.")

#  ............There is no need for this functionality at this time............
# @users_router.get('/')
# def all_users(x_token: str = Header(default=None)):
#     """ Used for admins to see a list with all users.
#
#     Args:
#         - JWT token
#
#     Returns:
#         - list of users(id, username, role)
#     """
#
#     if x_token is None:
#         raise HTTPException(status_code=401, detail="You must be logged in to view a list with users.")
#
#     user = get_user_or_raise_401(x_token)
#
#     if not user_service.is_admin(user):
#         raise HTTPException(status_code=401, detail="Only admins can view a list with all users.")
#
#     return user_service.all_users()


@users_router.get('/{id}')
def user_info(id: int, x_token: str = Header(default=None)):
    """ Used for admins to see data information about a user.

    Args:
        - user.id: int(URL link)
        - JWT token

    Returns:
        - user(id, username, user_type)
    """

    if x_token is None:
        raise HTTPException(status_code=401, detail="You must be logged in and be an admin to view accounts.")

    user = get_user_or_raise_401(x_token)

    if not user_service.is_admin(user):
        raise HTTPException(status_code=401, detail="Only admins can view accounts.")

    if not utilities.id_exists(id, 'users'):
        raise HTTPException(status_code=404, detail=f"User with id {id} does not exist.")

    return user_service.find_by_id_admin(id)


@users_router.put('/edit/{id}')
def edit_users_role(new_user: User, id: int, x_token: str = Header(default=None)):
    """ Used for editing a user's role through user.id. Only admins can edit it.

    Args:
        - user.id: int(URL link)
        - JWT token

    Returns:
        - Edited user
    """

    if x_token is None:
        raise HTTPException(status_code=401, detail="You must be logged in and be an admin to edit users roles.")

    user = get_user_or_raise_401(x_token)

    if not user_service.is_admin(user):
        raise HTTPException(status_code=401, detail="Only admins can edit roles.")

    if not utilities.id_exists(id, 'users'):
        raise HTTPException(status_code=404, detail=f"User with id {id} does not exist.")

    if new_user.user_type != Role.ADMIN and new_user.user_type != Role.USER:
        raise HTTPException(status_code=404, detail="Unknown role.")

    old_user = find_by_id(id)

    return user_service.edit_user_type(old_user, new_user)


@users_router.delete('/delete/{id}')
def delete_user(id: int, x_token: str = Header(default=None)):
    """ Used for deleting a user through user.id. Only admins can delete it.

    Args:
        - user.id: int(URL link)
        - JWT token

    Returns:
        - Deleted user
    """

    if x_token is None:
        raise HTTPException(status_code=401, detail="You must be logged in and be an admin to delete a user.")

    user = get_user_or_raise_401(x_token)

    if not utilities.id_exists(id, 'users'):
        raise HTTPException(status_code=404, detail=f"User with id {id} does not exist.")

    if user_service.is_admin(user):
        user_service.delete_user(id)

    if not user_service.is_admin(user):
        raise HTTPException(status_code=401, detail="You must be admin to delete a user.")

    return {'User deleted.'}


@users_router.post("/link-request")
def send_link_request(user_id: int, player_profile_id: int, x_token: str = Header(default=None)):
    """ Creates a link request. Only admins can approve or deny requests.

    Args:
        user_id: int
        player_profile_id: int
        x_token: JTW token

    Returns:
        A message about the sending of the request.

    """

    if x_token is None:
        raise HTTPException(status_code=401, detail="You must be logged in to send a request.")

    if user_id != get_user_or_raise_401(x_token).id:
        raise HTTPException(status_code=401, detail="Can't send request for another user.")

    if not utilities.id_exists(user_id, 'users'):
        raise HTTPException(status_code=404, detail=f"User with id {user_id} does not exist.")

    user_service.create_link_request(user_id, player_profile_id)

    return "Request was sent for an admin to approve or deny."


@users_router.put("/link-request/approve/{link_request_id}")
def approve_link_request(link_request_id, x_token: str = Header(default=None)):
    user = get_user_or_raise_401(x_token)

    if x_token is None:
        raise HTTPException(status_code=401, detail="You must be logged in to approve a request.")

    if not user_service.is_admin(user):
        raise HTTPException(status_code=401, detail="You must be admin to approve a request.")

    user_service.approve_link_request(link_request_id)

    return f"Request with ID: {link_request_id} was approved."


@users_router.put("/link-request/deny/{link_request_id}")
def deny_link_request(link_request_id, x_token: str = Header(default=None)):
    user = get_user_or_raise_401(x_token)

    if x_token is None:
        raise HTTPException(status_code=401, detail="You must be logged in to deny a request.")

    if not user_service.is_admin(user):
        raise HTTPException(status_code=401, detail="You must be admin to deny a request.")

    user_service.deny_link_request(link_request_id)

    return f"Request with ID: {link_request_id} was denied."


@users_router.post("/promote-request")
def send_promotion_request(user_id: int, x_token: str = Header(default=None)):
    """
    Creates a promotion to director request.

    Args:
        user_id: int
        x_token: JWT token

    Returns:
        A message about the sending of the promotion request.
    """

    if x_token is None:
        raise HTTPException(status_code=401, detail="You must be logged in to send a request.")

    if user_id != get_user_or_raise_401(x_token).id:
        raise HTTPException(status_code=401, detail="Unauthorized: You can only create requests for your own account.")

    if not utilities.id_exists(user_id, 'users'):
        raise HTTPException(status_code=404, detail=f'User with id {user_id} does not exist.')

    user_service.create_promotion_request(user_id)

    return "Promotion request was sent for an admin to review."


@users_router.put("/promote-request/approve/{promote_request_id}")
def approve_promotion_request_endpoint(promote_request_id: int, x_token: str = Header(default=None)):
    """
    Endpoint to approve a promotion request. Only admins can approve requests.

    Args:
        promote_request_id: int
        x_token: JWT token

    Returns:
        A message indicating the result of the operation.
    """
    if x_token is None:
        raise HTTPException(status_code=401, detail="You must be logged in to approve a request.")

    user = get_user_or_raise_401(x_token)

    # Assuming there's a function to check if the user is an admin
    if not user_service.is_admin(user):
        raise HTTPException(status_code=403, detail="Only admins can approve promotion requests.")

    return user_service.approve_promote_request(promote_request_id)


@users_router.put("/promote-request/deny/{promote_request_id}")
def deny_promotion_request_endpoint(promote_request_id: int, x_token: str = Header(default=None)):
    """
    Endpoint to deny a promotion request. Only admins can deny requests.

    Args:
        promote_request_id: int
        x_token: JWT token

    Returns:
        A message indicating the result of the operation.
    """

    if x_token is None:
        raise HTTPException(status_code=401, detail="You must be logged in to deny a request.")

    user = get_user_or_raise_401(x_token)

    if not user_service.is_admin(user):
        raise HTTPException(status_code=403, detail="Only admins can deny promotion requests.")

    return user_service.deny_promote_request(promote_request_id)
