from pydantic import BaseModel, EmailStr
from options import Role


class User(BaseModel):
    id: int
    password: str
    email: str
    player_id: int | None = None  # Option to associate with a player profile
    user_type: Role = Role.USER  # (user, amin, director)

    @classmethod
    def frm_query_result(cls, id, password, email, user_type, player_id=None):
        return cls(id=id,
                   password=password,
                   email=email,
                   player_id=player_id,
                   user_type=user_type
                   )


class LoginData(BaseModel):  # OK
    email: EmailStr
    password: str

