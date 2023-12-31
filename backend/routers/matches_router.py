from datetime import datetime

from fastapi import APIRouter, HTTPException, Header, Query
from models.match import Match
from services.matches_service import check_date_of_match
from services.user_service import is_admin, is_director
from services import matches_service
from authentication.auth import get_user_or_raise_401
from services import utilities
from models.options import CurrDateTime

matches_router = APIRouter(prefix='/matches', tags=['Matches'])


@matches_router.get('/', description="Show all matches.")
def get_matches(
        sort: str = Query(None, description="Sort matches by asc|desc."),
        get_by_date: str = Query(None, description="Sort matches by a specific date."),
        search: str = Query(None, description="Search a specific match by its id.")):
    result = matches_service.all(search, get_by_date)

    if not result:
        raise HTTPException(status_code=404, detail="No matches found.")

    if sort == 'date':
        result = [{**match, 'date': datetime.strptime(match['date'], '%Y-%m-%d')} for match in result]
        sorted_matches = sorted(result, key=lambda m: m['date'])
    elif sort == 'asc':
        sorted_matches = sorted(result, key=lambda m: m['id'])
    elif sort == 'desc':
        sorted_matches = sorted(result, key=lambda m: m['id'], reverse=True)
    else:
        sorted_matches = result

    formatted_matches = []
    for match in sorted_matches:
        try:
            formatted_match = f"MatchID: {match['id']} | Date: {match['date'] if isinstance(match['date'], str) else match['date'].strftime('%Y-%m-%d')} | {match.get('details')} | Winner: {match.get('winner_nickname', 'N/A')} | Tournament: {match.get('name')}"
            formatted_matches.append(formatted_match)
        except KeyError as e:
            print(f"KeyError: Missing key {e} in match data")

    return formatted_matches


@matches_router.put('/update/{id}')
def update_match_date_by_id(id: int, new_date: str, x_token: str):

    user = get_user_or_raise_401(x_token)

    if x_token is None:
        raise HTTPException(status_code=401, detail="You need to be logged in to update match!")

    if not (is_admin(user) or is_director(user)):
        raise HTTPException(status_code=401, detail="Unauthorized user to change match date.")

    if not matches_service.exist(id):
        raise HTTPException(status_code=204, detail=f"Match with id:{id} doesn't exist!")

    check_date = check_date_of_match(id)
    if check_date < CurrDateTime.CURRENT_DATE:
        raise HTTPException(status_code=205, detail=f"The match with date:{check_date} has expired!")

    existing_match = matches_service.get_by_id(id)

    matches_service.update_by_id(existing_match, new_date)

    return f"The date for the match was moved for {new_date}"


@matches_router.post('/')
def create_match(date: str = Query(description="To create a match, enter a date in the format: yyyy-mm-dd"),
                 format: str = Query("time or score"),
                 tournament_id: int = Query(default=None),
                 nickname_1: str = Query(),
                 nickname_2: str = Query(),
                 x_token: str = Header(default=None)):
    user = get_user_or_raise_401(x_token)

    if x_token is None:
        raise HTTPException(status_code=401, detail="You need to be logged in to create a match!")

    if not (is_admin(user) or is_director(user)):
        raise HTTPException(status_code=401, detail="Unauthorized user to create match.")

    if date < CurrDateTime.CURRENT_DATE:
        return HTTPException(status_code=205, detail=f"You cannot create a match with a past date!")

    match = matches_service.create(date=date, format=format, tournament_id=tournament_id, nickname_1=nickname_1,
                                   nickname_2=nickname_2)
    return match


@matches_router.delete('/delete/{id}')
def delete_match(id: int, x_token: str = Header(default=None)):
    user = get_user_or_raise_401(x_token)

    if x_token is None:
        raise HTTPException(status_code=401, detail="You need to be logged in to update match date!")

    if not is_admin(user):
        raise HTTPException(status_code=401, detail="Unauthorized user to change match date.")

    match = matches_service.get_by_id(id)
    if match is None:
        return HTTPException(status_code=404, detail=f"No match found with id:{id}!")

    matches_service.delete(id)
