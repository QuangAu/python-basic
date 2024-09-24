from uuid import UUID, uuid4

from common.exception import InvalidOperationError, ResourceNotFoundError
from models.player import PlayerModel, SearchPlayerModel
from models.player_transfer import PlayerTransfer
from schemas.club import Club
from schemas.player import Player
from services import transfer_history as TransferHistoryService
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_players(db_context: AsyncSession, condition: SearchPlayerModel):
    query = (
        select(
            Player.player_name,
            Player.age,
            Player.nationality,
            Player.market_value,
            Player.position,
            Club.club_name,
        )
        .join(Player.club, isouter=True)
        .order_by(Player.player_name)
    )
    if condition.player_name is not None:
        query = query.filter(Player.player_name.like(f"%{condition.player_name}%"))

    if condition.club_name is not None:
        query = query.filter(
            func.lower(Club.club_name) == condition.club_name.casefold()
        )

    query = query.offset((condition.page - 1) * condition.size).limit(condition.size)

    result = await db_context.execute(query)
    return result.all()


async def add_new_player(db_context: AsyncSession, data: PlayerModel):
    player = Player(**data.model_dump())
    db_context.add(player)
    await db_context.commit()
    await db_context.refresh(player)

    return player


async def update_player(db_context: AsyncSession, player_id: UUID, data: PlayerModel):
    result = await db_context.scalars(
        select(Player).filter(Player.id == UUID(player_id))
    )
    player = result.first()
    if player is None:
        raise ResourceNotFoundError()

    player.player_name = data.player_name
    player.age = data.age
    player.position = data.position
    player.nationality = data.nationality
    player.market_value = data.market_value

    await db_context.commit()
    await db_context.refresh(player)

    return player


async def set_player_club(db_context: AsyncSession, player_id: uuid4, club_id: uuid4):
    player = db_context.scalars(
        select(Player).filter(Player.id == UUID(player_id))
    ).first()

    if player is None:
        raise ResourceNotFoundError()

    club = db_context.scalars(select(Club).filter(Club.id == UUID(club_id))).first()
    if club is None:
        raise ResourceNotFoundError()

    player.club_id = club.id
    await db_context.commit()
    await db_context.refresh(player)

    return player


async def transfer_player(db_context: AsyncSession, player_id: str, data: PlayerTransfer):
    player = db_context.scalars(
        select(Player).filter(Player.id == UUID(player_id))
    ).first()

    if player is None:
        raise ResourceNotFoundError()

    club = db_context.scalars(select(Club).filter(Club.id == UUID(data.new_club))).first()
    if club is None:
        raise ResourceNotFoundError()

    # create transfer history
    history = TransferHistoryService.build_transfer_history(db_context, player, data)
    if history is None:
        raise InvalidOperationError

    # set to new club
    player.club_id = club.id

    db_context.add(history)
    await db_context.commit()
    await db_context.refresh(player)

    return player
