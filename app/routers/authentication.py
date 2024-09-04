from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from common.exception import UnAuthorizedError
from dependencies import db_context
from sqlalchemy.orm import Session
from services import authentication as AuthService
from models.authentication import OAuth2PasswordRequestFormNoStrict, Token
import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/token")
async def get_access_token(
    form_data: OAuth2PasswordRequestFormNoStrict = Depends(), db: Session = Depends(db_context)
):
    match form_data.grant_type:
        case "password":
            user = AuthService.authenticate_user(form_data.username, form_data.password, db)
            if not user:
                raise UnAuthorizedError
            
            return AuthService.create_access_token_by_user(user, settings.JWT_TOKEN_DURATION)
        case "client_credentials":
            client = AuthService.authenticate_client(form_data.client_id, form_data.client_secret, db)
            if not client:
                raise UnAuthorizedError
            
            return AuthService.create_access_token_by_client(client, settings.JWT_TOKEN_DURATION)
        case _:
            raise UnAuthorizedError
