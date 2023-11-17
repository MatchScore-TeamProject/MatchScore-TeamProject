from pydantic import BaseModel, EmailStr
from models.options import Role


class User(BaseModel):
    id: int | None = None
    email: str
    password: str
    user_type: str | None = 'user'  # (user, admin, director)
    player_profile_id: int | None = None  # Option to associate with a player profile

    @classmethod
    def from_query_result(cls, id, email, password, user_type=None, player_profile_id=None):
        return cls(
            id=id,
            email=email,
            password=password,
            user_type=user_type or 'user',
            player_profile_id=player_profile_id
        )

    @classmethod
    def from_query_result_no_password(cls, id, email, password, user_type=None, player_profile_id=None):
        return cls(
            id=id,
            email=email,
            password='',
            user_type=user_type or 'user',
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
