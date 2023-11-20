from fastapi import APIRouter, HTTPException, Header, Query
from models.match import Match
from services.user_service import is_admin, is_director
from services import matches_service
from authentication.auth import get_user_or_raise_401

matches_router = APIRouter(prefix='/matches', tags=['Matches'])


@matches_router.post('/')
def create_match(date: str = Query(description="Enter a date to create a match in format: yyyy-mm-dd"),
                 format: str = Query("time or score"),
                 participant_1: int = Query(),
                 participant_2: int = Query(),
                 x_token: str = Header(default=None)):
    user = get_user_or_raise_401(x_token)

    if x_token == None:
        raise HTTPException(status_code=401, detail="You need to be logged in to create a match!")

    if not (is_admin(user) or is_director(user)):
        raise HTTPException(status_code=401, detail="Unauthorized user to create match.")

    match = matches_service.create(date=date, format=format, participant_1=participant_1, participant_2=participant_2)
    return match


@matches_router.get('/', description="Get all matches.")
def get_match_by_id():
    pass


@matches_router.put('/')  # try with patch
def update_score():
    pass


@matches_router.put('/update/{id}')
def update_date(id: int, match: Match, x_token: str):
    user = get_user_or_raise_401(x_token)

    if x_token is None:
        raise HTTPException(status_code=401, detail="You need to be logged in to update match date!")

    if not (is_admin(user) or is_director(user)):
        raise HTTPException(status_code=401, detail="Unauthorized user to change match date.")

    if not matches_service.exist(id):
        return HTTPException(status_code=401, detail=f"Match with id:{id} doesn't exist!")

    # check for future date (future_date in utilities)
    # today =


@matches_router.put('/')  # try with patch
def update_players():
    pass
