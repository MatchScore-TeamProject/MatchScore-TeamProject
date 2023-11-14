from pydantic import BaseModel
from models.match import Match


class Tournament(BaseModel):
    id: int | None = None
    participants: int
    title: str
    tournament_format: str
    match_format: str
    prize: int | None = None 
    matches: list[Match] = []
    
    @classmethod
    def from_query_result(
        cls, id, participants, title, tournament_format, match_format, prize
        ):
        
        return cls(
            id=id,
            participants=participants,
            title=title,
            tournament_format=tournament_format,
            match_format=match_format,
            prize=prize,
        )
