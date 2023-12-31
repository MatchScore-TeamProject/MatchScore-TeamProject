from fastapi import FastAPI
from routers.matches_router import matches_router
from routers.player_profile_router import player_profile_router
from routers.users_router import users_router
from routers.tournaments_router import tournaments_router

app = FastAPI()

app.include_router(matches_router)
app.include_router(tournaments_router)
app.include_router(users_router)
app.include_router(player_profile_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run('main:app', host="127.0.0.1", port=8000, reload=True)
