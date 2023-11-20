from pydantic import BaseModel
from datetime import date
from models.options import MatchFormat


class Match(BaseModel):
    id: int | None = None
    date: str #date
    format: MatchFormat
    tournament_id: int | None = None
    participant_1: int
    participant_2: int
    score_1: int | None = None
    score_2: int | None = None

    @classmethod
    def from_query_result(cls, id, date, format, tournament_id, participant_1, participant_2, score_1, score_2):
        return cls(
            id=id,
            date=date,
            format=format,
            tournament_id=tournament_id,
            participant_1=participant_1,
            participant_2=participant_2,
            score_1=score_1,
            score_2=score_2
        )
