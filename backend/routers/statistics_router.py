from fastapi import APIRouter, Query, HTTPException
from services import tournaments_service, statistic_service

statistics_router = APIRouter(prefix='/statistics', tags=['Statistics'])


@statistics_router.post('/')
def all_players_in_tournament(tournament_id: int = Query(description="Enter the tournament id:")):

    check_if_tournament_id_exist = tournaments_service.get_by_id

    if check_if_tournament_id_exist is None:
        raise HTTPException(status_code=404, detail="Tournament not found")

    result = statistic_service.all_players(tournament_id)

    return result


