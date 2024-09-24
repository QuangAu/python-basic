from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from common.exception import InvalidOperationError, ResourceNotFoundError
from common import utils
from schemas.user import User
from models.user import UpdateUserModel, UserModel


async def get_users(db_context: AsyncSession):
    result = await db_context.scalars(select(User).order_by(User.name))
    user = result.all()
    return user


async def add_new_user(db_context: AsyncSession, data: UserModel):
    user = User(**data.model_dump())

    user.password = utils.hash_text(user.password)
    await db_context.add(user)
    await db_context.commit()
    await db_context.refresh(user)

    return user


async def change_password(
    db_context: AsyncSession, user: User, old_passowrd: str, new_password: str
):
    result = await db_context.scalars(
        select(User).filter(User.login_id == user.login_id)
    )
    user_data = result.first()
    if user_data is None:
        raise ResourceNotFoundError
    if not utils.compare_hashed_text(old_passowrd, user_data.password):
        raise InvalidOperationError

    user_data.password = utils.hash_text(new_password)

    await db_context.commit()


async def update_user(db_context: AsyncSession, user_id: UUID, data: UpdateUserModel):
    result = await db_context.scalars(select(User).filter(User.id == UUID(user_id)))
    user = result.first()
    if user is None:
        raise ResourceNotFoundError

    user.name = data.name
    user.is_active = data.is_active
    user.is_admin = data.is_admin

    await db_context.commit()


def delete_user(db_context: AsyncSession, user_id: UUID):
    user = db_context.scalars(select(User).filter(User.id == UUID(user_id))).first()
    if user is None:
        raise ResourceNotFoundError

    # Soft delte by deactivating user
    user.is_active = False

    db_context.commit()
