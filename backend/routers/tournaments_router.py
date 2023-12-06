from fastapi import APIRouter, Header, HTTPException, Query, Body
from authentication.auth import find_by_id, get_user_or_raise_401, create_token
from models.options import CurrDateTime
from models.tournament import Tournament, TournamentFormat, TournamentStatus, TournamentType, TournamentResponse
from services.matches_service import update_result_by_nicknames
from services.tournaments_service import delete_tournament, get_tournament_id_by_name, get_standings_by_league_name
from services.user_service import is_director, is_admin
from services import tournaments_service
from typing import List

tournaments_router = APIRouter(prefix='/tournaments', tags=['Tournaments'])


@tournaments_router.get('/')
def get_all():
    result = tournaments_service.all()

    if result is None:
        raise HTTPException(status_code=404, detail="No tournaments found")

    return result


@tournaments_router.get('/{tournament_name}')
def get_tournament(tournament_name: str):

    tournament_id = get_tournament_id_by_name(tournament_name)

    result = tournaments_service.get_by_id(tournament_id)

    if result is None:
        raise HTTPException(status_code=404, detail="Tournament not found")

    return result


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
        raise HTTPException(status_code=401, detail="You need to log in first.")

    user = get_user_or_raise_401(x_token)

    if not any([is_director(user), is_admin(user)]):
        raise HTTPException(status_code=401, detail="Only directors and admins can create tournaments.")

    if date < CurrDateTime.CURRENT_DATE:
        return HTTPException(status_code=205, detail=f"You cannot create a tournament with a past date!")

    valid_player_counts = {4, 8, 16, 32, 64}

    if len(player_nicknames) not in valid_player_counts:
        raise HTTPException(status_code=400,
                            detail="Number of players must be 4, 8, 16, 32 or 64 for a tournament!")

    if tournament_format == TournamentFormat.LEAGUE.value:
        new_tournament = tournaments_service.create_league(
            title, date, tournament_format, match_format, prize, player_nicknames)
        return {"Tournament": new_tournament}

    elif tournament_format == TournamentFormat.KNOCKOUT.value:
        new_tournament = tournaments_service.create_knockout(
            title, date, tournament_format, match_format, prize, player_nicknames)
        return {"Tournament": new_tournament}

    else:
        return HTTPException(status_code=400, detail=f"The format of the tournament should be: "
                                                     f"'{TournamentFormat.KNOCKOUT.value}' or '{TournamentFormat.LEAGUE.value}'")


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


@tournaments_router.delete("/delete/{tournament_id}")
def delete_tournament_endpoint(tournament_id: int, x_token: str = Header(default=None)):
    if x_token is None:
        raise HTTPException(status_code=401, detail="You need to log in first")

    user = get_user_or_raise_401(x_token)

    if not is_admin(user):
        raise HTTPException(status_code=401, detail="You need to be an admin to delete an")

    delete_tournament(tournament_id)

    return "Tournament deleted successfully!"


@tournaments_router.get('/standings/{league_name}')
def get_league_standings(league_name: str):

    result = get_standings_by_league_name(league_name)

    if result is None:
        raise HTTPException(status_code=404, detail="League not found")

    return result