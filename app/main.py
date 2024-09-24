from contextlib import asynccontextmanager

from dependencies import get_connection_string
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.authentication import router as authenticationRouter
from routers.club import router as clubRouter
from routers.player import router as playerRouter
from routers.transfer_history import router as transferHistoryRouter
from routers.user import router as userRouter
from services.database import sessionmanager
from services.oauth2_authentication import azure_scheme
from settings import APP_CLIENT_ID, OPENAPI_CLIENT_ID

if __name__ == "main":
    sessionmanager.init(get_connection_string())


@asynccontextmanager
async def lifespan(app: FastAPI):
    await azure_scheme.openid_config.load_config()
    yield
    if sessionmanager.engine is not None:
        await sessionmanager.close()

app = FastAPI(
    lifespan=lifespan,
    swagger_ui_oauth2_redirect_url="/oauth2-redirect",
    swagger_ui_init_oauth={
        "usePkceWithAuthorizationCodeGrant": True,
        "clientId": OPENAPI_CLIENT_ID,
        "scopes": f"api://{APP_CLIENT_ID}/user_impersonation"
    },)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(playerRouter)
app.include_router(clubRouter)
app.include_router(authenticationRouter)
app.include_router(userRouter)
app.include_router(transferHistoryRouter)
