from pydantic import BaseModel
from models.match import Match
from enum import Enum
from models.player_profile import PlayerProfile

class Tournament(BaseModel):
    id: int | None = None
    title: str
    tournament_format: str # Knockout or League
    match_format: str # time or score limited
    prize: int | None = None 
    participants: list[PlayerProfile] = []
    matches: list[Match] = []
    
    @classmethod
    def from_query_result(
        cls, id, title, tournament_format, match_format, prize, participants, matches
        ):
        
        return cls(
            id=id,
            title=title,
            tournament_format=tournament_format,
            match_format=match_format,
            prize=prize
        )

class TournamentStatus(Enum):
    OPEN = "open"
    CLOSED = "closed"


class TournamentFormat(Enum):
    KNOCKOUT = "knockout"
    LEAGUE = "league"


class TournamentType(BaseModel):
    id: int | None
    type: str

    def is_league(self):
        return self.type == TournamentFormat.LEAGUE

    def is_knockout(self):
        return self.type == TournamentFormat.KNOCKOUT