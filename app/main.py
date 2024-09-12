from fastapi import FastAPI

from routers.player import router as playerRouter
from routers.club import router as clubRouter
from routers.authentication import router as authenticationRouter
from routers.user import router as userRouter
from routers.transfer_history import router as transferHistoryRouter


app = FastAPI()


app.include_router(playerRouter)
app.include_router(clubRouter)
app.include_router(authenticationRouter)
app.include_router(userRouter)
app.include_router(transferHistoryRouter)
