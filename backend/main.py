from fastapi import FastAPI
# from routers.matches_router import matches_router
# from routers.tournaments_router import tournaments_router
from routers.users_router import user_router


app = FastAPI()

# app.include_router(matches_router)
# app.include_router(tournamets_router)
app.include_router(user_router)


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run('main:app', host="127.0.0.1", port=8000, reload=True)

