from fastapi import APIRouter, Header, HTTPException, Query, Body
from authentication.auth import find_by_id, get_user_or_raise_401, create_token
from models.tournament import Tournament, TournamentFormat, TournamentStatus, TournamentType
from services.user_service import is_director, is_admin
from services import tournaments_service
from typing import List
from models.match import MatchResponse


tournaments_router = APIRouter(prefix='/tournaments', tags=['Tournaments'])


@tournaments_router.post('/create')
def create(
        title: str = Query(),
        date: str = Query(),
        tournament_format: str = Query(),
        match_format: str = Query(),
        prize: str = Query(),
        player_nicknames: List[str] = Body(),
        x_token: str = Header(default=None)):
    
    if x_token is None:
        raise HTTPException(status_code=401, detail='You need to log in first')

    user = get_user_or_raise_401(x_token)

    if not any([is_director(user), is_admin(user)]):
        raise HTTPException(status_code=401, detail="Only directors and admins can create tournaments")
    

    tournament_result = tournaments_service.create_tournament(
        title, date, tournament_format, match_format, prize, player_nicknames
    )

    new_tournament = tournament_result[0]  
    knockout_matches = tournament_result[1]  
    
   
    return {"Tournament": new_tournament, "Matches": knockout_matches}



@tournaments_router.get('/')
def get_all(x_token: str = Header(default=None)):
    
    if x_token is None:
        raise HTTPException(status_code=401, detail="You need to be logged in to view tournaments!")

    result = tournaments_service.all()

    if result is None:
        raise HTTPException(status_code=404, detail="No tournaments found")
    
    return result

@tournaments_router.get('/{id}')
def get_tournament_by_id(tournament_id: int, x_token: str = Header(default=None)):
    
    if x_token is None:
        raise HTTPException(status_code=401, detail="You need to be logged in to view tournaments!")

    result = tournaments_service.get_by_id(tournament_id)

    if result is None:
        raise HTTPException(status_code=404, detail="Tournament not found")

    return result


@tournaments_router.put('/edit/{id}')
def edit_tournament_by_id(tournament_id: int, x_token: str = Header(default=None)):

    if x_token is None:
        raise HTTPException(status_code=401, detail='You need to log in first')

    user = get_user_or_raise_401(x_token)

    if not any([is_director(user), is_admin(user)]):
        raise HTTPException(status_code=401, detail="Only directors and admins can edit tournaments")