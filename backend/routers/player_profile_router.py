import re

from fastapi import APIRouter, Header, HTTPException, Body, Query
from fastapi.responses import JSONResponse
from authentication.auth import get_user_or_raise_401
from models.player_profile import PlayerProfile
from services import utilities
from services.player_profile_service import create_player_profile, delete_player_profile, edit_player_profile, \
    view_player_profile
from services.user_service import is_admin

player_profile_router = APIRouter(prefix="/players", tags=["Players"])


@player_profile_router.get("/view-player/{nickname}")
def view_player_endpoint(player_nickname: str):
    player_info = view_player_profile(player_nickname)

    output = {
        "Player Information": {
            "-Nickname": player_info[0],
            "-Name": player_info[1],
            "-Country": player_info[2],
            "-Sports Club": player_info[3]
        }
    }

    return JSONResponse(content=output)


@player_profile_router.post("/create")
def create_player_profile_endpoint(nickname: str = Query(),
                                   full_name: str = Query(description="Name should consist of: FirstName Surname FamilyName"),
                                   country: str = Query(),
                                   sports_club: str = Query(None),
                                   x_token: str = Header(default=None)):

    if x_token is None:
        raise HTTPException(status_code=401, detail='You must be logged in to create a player profile.')

    user = get_user_or_raise_401(x_token)

    if not is_admin(user):
        raise HTTPException(status_code=401, detail='Only admins can create a player profile.')

    create_player_profile(nickname, full_name, country, sports_club, users_id=None)

    return f"Profile for {full_name} was created."


@player_profile_router.put("/edit/{player_profile_id}")
def edit_player_profile_endpoint(
        player_profile_id: int,
        nickname: str = Query(default=None, description="New nickname"),
        full_name: str = Query(default=None, description="New full name"),
        country: str = Query(default=None, description="New country"),
        sports_club: str = Query(default=None, description="New sports club"),
        x_token: str = Header(default=None)
):
    """
    Endpoint to edit a player profile using query parameters.

    Args:
        player_profile_id: int - ID of the player profile to edit
        nickname: str - New nickname (optional)
        full_name: str - New full name (optional)
        country: str - New country (optional)
        sports_club: str - New sports club (optional)
        x_token: str - JWT token for authentication

    Returns:
        A message indicating the result of the operation.
    """

    if x_token is None:
        raise HTTPException(status_code=401, detail="Authentication token is missing.")

    user = get_user_or_raise_401(x_token)
    user_id = user.id
    user_type = user.user_type

    new_profile_data = PlayerProfile(
        nickname=nickname,
        full_name=full_name,
        country=country,
        sports_club=sports_club
    )
    result = edit_player_profile(player_profile_id, new_profile_data, user_id, user_type)
    return result


@player_profile_router.delete("/delete")
def delete_player_profile_endpoint(player_profile_id: int, x_token: str = Header(Default=None)):
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
