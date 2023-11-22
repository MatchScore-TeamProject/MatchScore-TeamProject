from pydantic import BaseModel


class LinkRequest(BaseModel):
    id: int | None = None
    user_id: int
    player_profile_id: int
    status: str = "pending"


class PromoteRequest(BaseModel):
    id: int | None = None
    user_id: int
    status: str = "pending"
