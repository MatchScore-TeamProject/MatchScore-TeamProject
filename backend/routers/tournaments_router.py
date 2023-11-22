from fastapi import APIRouter, Header, HTTPException
from authentication.auth import find_by_id, get_user_or_raise_401, create_token
from models.tournament import Tournament, TournamentFormat, TournamentStatus, TournamentType
from services.user_service import is_director
from services import tournaments_service
from typing import List

tournaments_router = APIRouter(prefix='/tournaments', tags=['Tournaments'])


@tournaments_router.post('/create')
def create(
        tournament: Tournament,
        player_ids: List[int],
        x_token: str = Header(default=None)):
    
    if x_token is None:
        raise HTTPException(status_code=401, detail='You need to log in first')

    user = get_user_or_raise_401(x_token)

    if not is_director(user):
        raise HTTPException(status_code=401, detail="Only directors can create tournaments")
    
    new_tournament = tournaments_service.create_tournament(tournament, player_ids)

    return new_tournament