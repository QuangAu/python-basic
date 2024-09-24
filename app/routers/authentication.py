import settings
from common.exception import UnAuthorizedError
from fastapi import APIRouter, Depends
from models.authentication import OAuth2PasswordRequestFormNoStrict
from services import authentication as AuthService
from services.database import get_db_context
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/token")
async def get_access_token(
    form_data: OAuth2PasswordRequestFormNoStrict = Depends(), db: AsyncSession = Depends(get_db_context)
):
    match form_data.grant_type:
        case "password":
            user = await AuthService.authenticate_user(form_data.username, form_data.password, db)
            if not user:
                raise UnAuthorizedError

            return AuthService.create_access_token_by_user(user, settings.JWT_TOKEN_DURATION)
        case "client_credentials":
            client = await AuthService.authenticate_client(form_data.client_id, form_data.client_secret, db)
            if not client:
                raise UnAuthorizedError

            return await AuthService.create_access_token_by_client(client, settings.JWT_TOKEN_DURATION)
        case _:
            raise UnAuthorizedError
