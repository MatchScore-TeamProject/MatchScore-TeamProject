from fastapi import APIRouter, Header, HTTPException, Query, Body
from authentication.auth import find_by_id, get_user_or_raise_401, create_token
from models.options import CurrDateTime
from models.tournament import Tournament, TournamentFormat, TournamentStatus, TournamentType, TournamentResponse
from services.matches_service import update_result_by_nicknames
from services.user_service import is_director, is_admin
from services import tournaments_service
from typing import List


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
        raise HTTPException(status_code=401, detail="You need to log in first")

    user = get_user_or_raise_401(x_token)

    if not any([is_director(user), is_admin(user)]):
        raise HTTPException(status_code=401, detail="Only directors and admins can create tournaments.")

    if date < CurrDateTime.CURRENT_DATE:
        return HTTPException(status_code=205, detail=f"You cannot create a tournament with a past date!")

    tournament_result = tournaments_service.create_tournament(
        title, date, tournament_format, match_format, prize, player_nicknames
    )

    new_tournament, player_nicknames = tournament_result
    return {"Tournament": new_tournament}


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
    

@tournaments_router.get('/{id}/matches')
def get_all_matches_by_tournament(tournament_id: int, x_token: str = Header(default=None)):
    if x_token is None:
        raise HTTPException(status_code=401, detail="You need to be logged in to view tournaments!")

    result = tournaments_service.get_all_matches_in_tournament_by_id(tournament_id)

    if result is None:
        raise HTTPException(status_code=404, detail="Tournament not found!")

    return result


@tournaments_router.put('/{tournament_id}/update_match_winner')
def update_match_winner(tournament_id: int,
                        nickname_1: str = Query(),
                        score_1: int = Query(),
                        score_2: int = Query(),
                        nickname_2: str = Query(),
                        x_token: str = Header(default=None)):
    if x_token is None:
        raise HTTPException(status_code=401, detail="You need to log in first")

    user = get_user_or_raise_401(x_token)

    if not any([is_director(user), is_admin(user)]):
        raise HTTPException(status_code=401, detail="Only directors and admins can edit matches.")

    winner = update_result_by_nicknames(tournament_id, nickname_1, score_1, score_2, nickname_2)
    if not winner:
        raise HTTPException(status_code=400, detail=f"Match between {nickname_1} and {nickname_2} does not exist.")

    return winner
