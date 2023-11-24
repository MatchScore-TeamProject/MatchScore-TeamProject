from fastapi import APIRouter, Header, HTTPException, Query, Body
from authentication.auth import find_by_id, get_user_or_raise_401, create_token
from models.tournament import Tournament, TournamentFormat, TournamentStatus, TournamentType
from services.user_service import is_director
from services import tournaments_service
from typing import List

tournaments_router = APIRouter(prefix='/tournaments', tags=['Tournaments'])


@tournaments_router.post('/create')
def create(
        title: str = Query(),
        date: str = Query(),
        participants: int = Query(),
        tournament_formant: str = Query(),
        match_format: str = Query(),
        prize: str = Query(),
        player_nicknames: List[str] = Body(),
        x_token: str = Header(default=None)):
    
    if x_token is None:
        raise HTTPException(status_code=401, detail='You need to log in first')

    user = get_user_or_raise_401(x_token)

    if not is_director(user):
        raise HTTPException(status_code=401, detail="Only directors can create tournaments")
    
    new_tournament, player_nicknames = tournaments_service.create_tournament(title, date, participants, tournament_formant,match_format,
        prize, player_nicknames)

    return f'Tournament created: {new_tournament}'


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

    if not is_director(user):
        raise HTTPException(status_code=401, detail="Only directors can edit tournaments")
    
    