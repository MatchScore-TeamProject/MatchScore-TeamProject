from fastapi import APIRouter, Header, HTTPException
from authentication.auth import find_by_id, get_user_or_raise_401, create_token
from models.user import User, LoginData
from services import user_service, utilities

users_router = APIRouter(prefix='/users', tags=['Users'])


@users_router.post('/register')
def register(data: LoginData):
    ''' Used for registering new users.

    Args:
        - LoginData(username, password(str))

    Returns:
        - Registered user as customer
    '''

    user = user_service.create(data.email, data.password)

    return user or HTTPException(status_code=400, detail=f'Email {data.email} is already taken.')


@users_router.post('/login')
def login(data: LoginData):
    ''' Used for logging in.

    Args:
        - LoginData(email, password(str))

    Returns:
        - JWT token
    '''
    user = user_service.try_login(data.email, data.password)
    if user:
        token = create_token(user)
        return {'token': token}
    else:
        raise HTTPException(status_code=400, detail='Invalid login data.')


@users_router.get('/')
def all_users(x_token: str = Header(default=None)):
    ''' Used for admins to see a list with all users.

    Args:
        - JWT token

    Returns:
        - list of users(id, username, role)
    '''

    if x_token == None:
        raise HTTPException(status_code=401, detail='You must be logged in to view a list with users.')

    user = get_user_or_raise_401(x_token)

    if not user_service.is_admin(user):
        raise HTTPException(status_code=401, detail='Only admins can view a list with all users.')

    return user_service.all_users()


@users_router.get('/{id}')
def user_info(id: int, x_token: str = Header(default=None)):
    ''' Used for admins to see data information about a user.

    Args:
        - user.id: int(URL link)
        - JWT token

    Returns:
        - user(id, username, user_type)
    '''

    if x_token == None:
        raise HTTPException(status_code=401, detail='You must be logged in and be an admin to view accounts.')

    user = get_user_or_raise_401(x_token)

    if not user_service.is_admin(user):
        raise HTTPException(status_code=401, detail='Only admins can view accounts.')

    if not utilities.id_exists(id, 'users'):
        raise HTTPException(status_code=404, detail=f'User with id {id} does not exist.')

    return user_service.find_by_id_admin(id)


@users_router.put('/edit/{id}')
def edit_users_role(new_user: User, id: int, x_token: str = Header(default=None)):
    ''' Used for editing a user's role through user.id. Only admins can edit it.

    Args:
        - user.id: int(URL link)
        - JWT token

    Returns:
        - Edited user
    '''

    if x_token == None:
        raise HTTPException(status_code=401, detail='You must be logged in and be an admin to edit users roles.')

    user = get_user_or_raise_401(x_token)

    if not user_service.is_admin(user):
        raise HTTPException(status_code=401, detail='Only admins can edit roles.')

    if not utilities.id_exists(id, 'users'):
        raise HTTPException(status_code=404, detail=f'User with id {id} does not exist.')

    if new_user.user_type != 'admin' and new_user.user_type != 'user':
        raise HTTPException(status_code=404, detail='Unknown role.')

    old_user = find_by_id(id)

    return user_service.edit_user_type(old_user, new_user)


@users_router.delete('/delete/{id}')
def delete_user(id: int, x_token: str = Header(default=None)):
    ''' Used for deleting a user through user.id. Only admins can delete it.

    Args:
        - user.id: int(URL link)
        - JWT token

    Returns:
        - Deleted user
    '''

    if x_token == None:
        raise HTTPException(status_code=401, detail='You must be logged in and be an admin to delete a user.')

    user = get_user_or_raise_401(x_token)

    if not utilities.id_exists(id, 'users'):
        raise HTTPException(status_code=404, detail=f'User with id {id} does not exist.')

    if user_service.is_admin(user):
        user_service.delete_user(id)

    if not user_service.is_admin(user):
        raise HTTPException(status_code=401, detail='You must be admin to delete a user.')

    return {'User deleted.'}