from fastapi import FastAPI

from routers import club, player, authentication, user, transfer_history


app = FastAPI()


app.include_router(player.router)
app.include_router(club.router)
app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(transfer_history.router)
