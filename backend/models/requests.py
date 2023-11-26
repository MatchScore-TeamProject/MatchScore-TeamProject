from pydantic import BaseModel
from models.options import CurrentStatus


class LinkRequest(BaseModel):
    id: int | None = None
    user_id: int
    player_profile_id: int
    status: str = CurrentStatus


class PromoteRequest(BaseModel):
    id: int | None = None
    user_id: int
    status: str = CurrentStatus
