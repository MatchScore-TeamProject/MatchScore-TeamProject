from pydantic import BaseModel
from models.player_profile import PlayerProfile
from datetime import datetime


class Match(BaseModel):
    id: int | None = None
    timestamp: datetime
    duration: int
    participants: list[PlayerProfile] = []  # FIX THIS IN DB player_profile
    # time_limit, score_limit, score ???

    @classmethod
    def from_query_result(cls, id, timestamp, duration, participants):
        
        return cls(
            id=id,
            timestamp=timestamp,
            duration=duration,
            participants=participants,
        )
    