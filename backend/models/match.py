from pydantic import BaseModel
from datetime import date
from models.options import MatchFormat


class Match(BaseModel):
    id: int | None = None
    date: str  # date
    format: MatchFormat
    tournament_id: int | None = None
    score_1: int | None = None
    score_2: int | None = None
    player_profile_id1: int | None = None
    player_profile_id2: int | None = None
    winner: str | None = None
    stage: int | None = None
    order_num: int | None = None

    @classmethod
    def from_query_result(
        cls, id, date, format, tournament_id, player_profile_id1, player_profile_id2, score_1, score_2, winner, stage, order_num
        ):
        return cls(
            id=id,
            date=date,
            format=format,
            tournament_id=tournament_id,
            score_1=score_1,
            score_2=score_2,
            player_profile_id1=player_profile_id1,
            player_profile_id2=player_profile_id2,
            winner=winner,
            stage=stage,
            order_num=order_num
        )


class MatchResponse(BaseModel):
    nickname_1: str | None = None  
    score_1: int | None = None
    score_2: int | None = None
    nickname_2: str | None = None

    @classmethod
    def from_query_result(cls, nickname_1, score_1, score_2, nickname_2):
        return cls(
            nickname_1=nickname_1,
            score_1=score_1,
            score_2=score_2,
            nickname_2=nickname_2
                    )