from pydantic import BaseModel
from datetime import date
from models.options import MatchFormat
from services.utilities import find_player_nickname_by_id

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
    stage: str | None = None

    @classmethod
    def from_query_result(
        cls, id, date, format, tournament_id, player_profile_id1, player_profile_id2, score_1, score_2, winner, stage
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
            stage=stage
        )

class MatchResponse(BaseModel):
    player_1: str | None = None
    score_1: int | None = None
    score_2: int | None = None
    player_2: str | None = None

    @classmethod
    def from_query_result(cls, player_1, score_1, score_2, player_2):
        player_1 = find_player_nickname_by_id(player_1)
        player_2 = find_player_nickname_by_id(player_2)

        return cls(player_1=player_1, score_1=score_1, score_2=score_2, player_2=player_2)