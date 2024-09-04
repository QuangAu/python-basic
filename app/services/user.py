from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session
from common.exception import InvalidOperationError, ResourceNotFoundError
from common import utils
from schemas.user import User
from models.user import UpdateUserModel, UserModel


def get_users(db_context: Session):
    result = db_context.scalars(select(User).order_by(User.name)).all()

    return result


def add_new_user(db_context: Session, data: UserModel):
    user = User(**data.model_dump())

    user.password = utils.hash_text(user.password)
    db_context.add(user)
    db_context.commit()
    db_context.refresh(user)

    return user


def change_password(
    db_context: Session, user: User, old_passowrd: str, new_password: str
):
    user_data = db_context.scalars(
        select(User).filter(User.login_id == user.login_id)
    ).first()
    if user_data is None:
        raise ResourceNotFoundError
    if not utils.compare_hashed_text(old_passowrd, user_data.password):
        raise InvalidOperationError

    user_data.password = utils.hash_text(new_password)

    db_context.commit()


def update_user(db_context: Session, user_id: UUID, data: UpdateUserModel):
    user = db_context.scalars(select(User).filter(User.id == UUID(user_id))).first()
    if user is None:
        raise ResourceNotFoundError

    user.name = data.name
    user.is_active = data.is_active
    user.is_admin = data.is_admin

    db_context.commit()


def delete_user(db_context: Session, user_id: UUID):
    user = db_context.scalars(select(User).filter(User.id == UUID(user_id))).first()
    if user is None:
        raise ResourceNotFoundError

    # Soft delte by deactivating user
    user.is_active = False

    db_context.commit()
