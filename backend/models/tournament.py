from pydantic import BaseModel
from models.match import Match
from enum import Enum
from models.player_profile import PlayerProfile

class Tournament(BaseModel):
    id: int | None = None
    title: str
    date: str
    tournament_format: str # Knockout or League
    match_format: str # time or score limited
    prize: int | None = None 
    player_nicknames: list[str] = []
    
    @classmethod
    def from_query_result(
        cls, id, title, date, tournament_format, match_format, prize, player_nicknames
        ):
        
        return cls(
            id=id,
            title=title,
            date=date,
            tournament_format=tournament_format,
            match_format=match_format,
            prize=prize,
            player_nicknames=player_nicknames,
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
    

class TournamentResponse(BaseModel):
    title: str
    date: str
    tournament_format: str
    match_format: str
    prize: str
    player_nicknames: list[str] = []
    matches: list[str] =[]

    @classmethod
    def from_query_result(cls, tournament, player_nicknames, matches):
        return cls(
            title=tournament.title,
            date=tournament.date,
            tournament_format=tournament.tournament_format,
            match_format=tournament.match_format,
            prize=tournament.prize,
            player_nicknames=player_nicknames,
            matches=matches
        )