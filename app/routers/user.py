from typing import List
from fastapi import APIRouter, Depends
from starlette import status
from sqlalchemy.orm import Session
from common.exception import UnAuthorizedError
from schemas.user import User
from models.user import UpdateUserModel, UserModel, UserViewModel
from dependencies import get_db_session
from services import user as UserService
from services import authentication as AuthenticationService

router = APIRouter(prefix="/users", tags=["User"])


@router.get("", status_code=status.HTTP_200_OK, response_model=List[UserViewModel])
async def get_users(
    db: Session = Depends(get_db_session),
    user: User = Depends(AuthenticationService.token_interceptor),
):
    if not user.is_admin:
        raise UnAuthorizedError

    return UserService.get_users(db)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserViewModel)
async def add_new_user(
    request: UserModel,
    db: Session = Depends(get_db_session),
    user: User = Depends(AuthenticationService.token_interceptor),
):
    if not user.is_admin:
        raise UnAuthorizedError

    return UserService.add_new_user(db, request)


@router.patch("/change-password", status_code=status.HTTP_202_ACCEPTED)
async def change_user_password(
    old_password: str,
    new_password: str,
    db: Session = Depends(get_db_session),
    user: User = Depends(AuthenticationService.token_interceptor),
):

    UserService.change_password(db, user, old_password, new_password)


@router.put("/{user_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_user(
    user_id: str,
    request: UpdateUserModel,
    db: Session = Depends(get_db_session),
    user: User = Depends(AuthenticationService.token_interceptor),
):
    if not user.is_admin:
        raise UnAuthorizedError
    return UserService.update_user(db, user_id, request)


@router.delete("/{user_id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_user(
    user_id: str,
    db: Session = Depends(get_db_session),
    user: User = Depends(AuthenticationService.token_interceptor),
):
    if not user.is_admin:
        raise UnAuthorizedError
    return UserService.delete_user(db, user_id)
