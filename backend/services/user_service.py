# from data.models.user import User, Role
from database.database_connection import read_query, read_query_additional, update_query, insert_query
from models.user import User, LoginData, Role
from authentication.auth import find_by_email, find_by_id


def _hash_password(password: str):
    ''' Used to hash a password of a user before saving it in the database.'''
    from hashlib import sha256
    return sha256(password.encode('utf-8')).hexdigest()


def try_login(email: str, password: str) -> User | None:
    ''' Used to hash the login password and compare it with the existing password of the user in the database.'''

    user = find_by_email(email)

    password = _hash_password(password)
    return user if user and user.password == password else None


def create(email: str, password: str) -> User | None:
    ''' Used to save the already hashed password to the database.'''

    password = _hash_password(password)

    generated_id = insert_query(
        'INSERT INTO users(email, password, user_type) VALUES (?,?,?)',
        (email, password, Role.USER))

    return User(id=generated_id, email=email, password='', role=Role.USER)


def delete_user(id: int):
    ''' Used for deleting the user from the database.'''

    insert_query('''DELETE FROM users WHERE id = ?''',
                 (id,))


def edit_user_type(old_user: User, new_user: User):
    ''' Used for editing by an admin a role of a user in the database.'''

    edited_user = User(
        id=old_user.id,
        username=old_user.email,
        password=old_user.password,
        role=new_user.user_type
    )

    update_query('''UPDATE users SET role = ? WHERE id = ?''',
                 (edited_user.user_type, edited_user.id))

    return {"User's role updated."}


def is_admin(user: User):
    ''' Compares the user's role if it's an admin when a JWT token is written in the Header.
    Returns:
        - True/False
    '''
    return user.user_type == Role.ADMIN


def all_users():
    data = read_query(
        '''SELECT id, email, user_type, player_profile_id
        from users''')
    if data is None:
        return None

    return (User.from_query_result_no_password(*row) for row in data)


def get_by_id(id: int):
    data = read_query(
        '''SELECT id, email, user_type, player_profile_id
        from users
        where id = ?''', (id,))
    return next((User.from_query_result_no_password(*row) for row in data), None)


def find_by_id_admin(id: int) -> User | None:
    ''' Search through users.id the whole information about the account in the data. Only admins can search for them.

    Args:
        - id: int 

    Returns:
        - all the necessary information about the user (id, username, hashed password, role and etc.)
    '''

    data = read_query(
        'SELECT id, email, user_type, player_profile_id FROM users WHERE id = ?',
        (id,))

    return next((User.from_query_result_no_password(*row) for row in data), None)
