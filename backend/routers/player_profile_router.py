from fastapi import APIRouter, Header, HTTPException

from authentication.auth import get_user_or_raise_401
from services import utilities
from services.player_profile_service import create_player_profile, delete_player_profile
from services.user_service import is_admin

player_profile_router = APIRouter(prefix="/players", tags=["Players"])


@player_profile_router.post("/create")
def create_player_profile_endpoint(player_fullname: str,
                                   country: str,
                                   sports_club: str,
                                   x_token: str = Header(default=None)):
    if x_token is None:
        raise HTTPException(status_code=401, detail='You must be logged in to create a player profile.')

    user = get_user_or_raise_401(x_token)

    if not is_admin(user):
        raise HTTPException(status_code=401, detail='Only admins can create a player profile.')

    create_player_profile(player_fullname, country, sports_club, users_id=None)

    return f"Profile for {player_fullname} was created."


@player_profile_router.delete("/delete")
def delete_player_profile_endpoint(player_profile_id, x_token: str = Header(Default=None)):

    if x_token is None:
        raise HTTPException(status_code=401, detail='You must be logged in to delete a player profile.')

    user = get_user_or_raise_401(x_token)

    if not utilities.id_exists(player_profile_id, 'player_profile'):
        raise HTTPException(status_code=404, detail=f'User with id {player_profile_id} does not exist.')

    if is_admin(user):
        delete_player_profile(player_profile_id)

    if not is_admin(user):
        raise HTTPException(status_code=401, detail='You must be admin to delete a user.')

    return f"Profile with ID: {player_profile_id} was deleted."

