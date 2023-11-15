from pydantic import BaseModel, EmailStr
from models.options import Role


class User(BaseModel):
    id: int | None = None
    email: str
    password: str
    player_profile_id: int | None = None  # Option to associate with a player profile
    user_type: str | None = 'user'  # (user, admin, director)

    @classmethod
    def from_query_result(cls, id, email, password, user_type='user', player_profile_id=None):
        return cls(
                id=id,
                email=email,
                password='',
                user_type=user_type,
                player_profile_id=player_profile_id
                )


class LoginData(BaseModel): 
    email: EmailStr
    password: str


class CreateUserModel(BaseModel):
    id: int | None = None
    email: str
    password: str
    user_type: str | None = 'user'
