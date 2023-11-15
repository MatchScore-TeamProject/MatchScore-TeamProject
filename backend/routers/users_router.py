from fastapi import APIRouter, Depends , Request, HTTPException
from authentication.jwt_bearer import JwtBearer
from services.utilities import email_exists, id_exists
from services.user_service import check_user
from models.user import User, LoginData, CreateUserModel
from services import user_service
from authentication.jwt_handler import signJWT


user_router = APIRouter(prefix='/users', tags=['Users'])


@user_router.get('/')
def get_all_users():
    result = user_service.all_users()
    if result is None:
        raise HTTPException(status_code=404, detail="No users yet.")
    return result


@user_router.get('/{id}')
def get_user_by_id(id: int):
    user = user_service.get_by_id(id)
    if user is None:
        raise HTTPException(status_code=404, detail="No user with ID:{id}")
    return user


@user_router.post('/register')
def register(user: CreateUserModel):
    if email_exists(user.email, 'users'):
        raise HTTPException(status_code=400, detail=f'User with email: {user.email} already exists.')
    created_user = user_service.create(user)

    return signJWT(created_user.email)


# @user_router.post('/register/admin')
# def register_admin(user: CreateUserModel):
#     if email_exists(user.email, 'users'):
#         raise HTTPException(status_code=400, detail=f'Admin with email: {user.email} already exists.')
#     created_user = user_service.create(user, True)

#     return signJWT(created_user.email)


@user_router.post('/login')
def login(user: LoginData):
    if not email_exists(user.email, 'users'):
        return {
            "error": "You are not registered"
        }
    if check_user(user):
        return signJWT(user.email)
    else:
        return {"error": "Invalid email or password"}



@user_router.put('/{id}', dependencies=[Depends(JwtBearer())])
def edit_user(id: int, user: User, request:Request):
    check_token(request)
    existing_user = user_service.get_by_id(id)
    if existing_user is None:
        return HTTPException(status_code=404, detail="User Not Found")
    return user_service.update(existing_user, user)


@user_router.delete('/{id}', dependencies=[Depends(JwtBearer())])
def delete_user(id:int, request: Request):
    if not id_exists(id, 'users'):
        raise HTTPException(status_code=404, detail=f'User with id: {id} does not exist.')
    if not user_service.is_admin(check_token(request)):
        raise HTTPException(status_code=403, detail='Only admins can remove users.')
    user_service.delete(id)

    return f"User with id {id} deleted"


def check_token(request: Request):
    x_token = request.headers.get("Authorization")
    if not JwtBearer.verify_jwt(x_token):
        raise HTTPException(status_code=403, detail='Invalid or expired token')
    return x_token 