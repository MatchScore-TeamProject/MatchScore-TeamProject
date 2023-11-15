# from data.models.user import User, Role
from database.database_connection import read_query, read_query_additional, update_query, insert_query
from models.user import User, LoginData, Role
from services.utilities import create_hash



def all_users():
    data = read_query(
        '''SELECT id, email, user_type, player_profile_id
        from users''')
    if data is None:
        return None

    return (User.from_query_result(*row) for row in data)


def get_by_id(id: int):
    data = read_query(
        '''SELECT id, email, user_type, player_profile_id
        from users
        where id = ?''', (id,))
    return next((User.from_query_result(*row) for row in data), None)


def create(user: User):
    hashed_password = create_hash(user.password)

    generated_id = insert_query(
        '''INSERT INTO users(email, password, user_type) VALUES(?,?,?)''',
        (user.email, hashed_password,  user.user_type))

    user.id = generated_id
    
    return user

def update(old: User, new: User):
    merged = User(
        id=old.id,
        email=new.email or old.email,
        password=new.password or old.password,
        user_type=new.user_type or old.user_type,
        player_profile_id=new.user_type or old.user_type
    )

    update_query(
        '''UPDATE users SET
            email = ?, password = ? ,user_type = ?, player_profile_id = ?
           WHERE id = ? 
        ''',
        (merged.email, merged.password, merged.user_type, merged.player_profile_id, merged.id))
    return merged

def is_director(user: User):
    ''' Compares the user's role if it's a director when a JWT token is written in the Header.
    Returns:
        - True/False
    '''
    return user.user_type == Role.DIRECTOR


def is_admin(user: User):
    ''' Compares the user's role if it's an admin when a JWT token is written in the Header.
    Returns:
        - True/False
    '''
    return user.user_type == Role.ADMIN

def check_user(data: LoginData):
    user = read_query('''Select email, password from users where email = ?''', (data.email, ))
    hashes_password = create_hash(data.password)
    if user[0][0] == data.email and user[0][1] == hashes_password:
        return True
    return False


def delete(id: int):
    insert_query('DELETE FROM users WHERE id = ?',
                 (id,))