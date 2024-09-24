from uuid import UUID

from common.exception import InvalidOperationError
from models.player_transfer import PlayerTransfer
from schemas.club import Club
from schemas.player import Player
from schemas.transfer_history import TransferHistory
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased


async def get_transfer_histories(db_context: AsyncSession):
    old_club = aliased(Club, name="old_club")
    new_club = aliased(Club, name="new_club")

    query = (
        select(
            TransferHistory.transfer_fee,
            TransferHistory.contract_start,
            TransferHistory.contract_end,
            Player.player_name,
            old_club.club_name.label('from_club'),
            new_club.club_name.label('to_club')
        )
        .join(TransferHistory.player, isouter=True)
        .join(old_club, TransferHistory.from_club_id == old_club.id, isouter=True)
        .join(new_club, TransferHistory.to_club_id == new_club.id, isouter=True)
        .order_by(TransferHistory.transfer_fee)
    )
    result = await db_context.execute(query)
    return result.all()


async def build_transfer_history(
    db_context: AsyncSession, player: Player, transfer_data: PlayerTransfer
) -> TransferHistory:
    result = await db_context.scalars(
        select(TransferHistory).filter(
            and_(
                TransferHistory.player_id == player.id,
                TransferHistory.from_club_id == player.club_id,
                TransferHistory.to_club_id == UUID(transfer_data.new_club),
                TransferHistory.contract_start == transfer_data.start_date,
                TransferHistory.contract_end == transfer_data.end_date
            )
        )
    )
    existing_transfer = result.first()
    if existing_transfer:
        raise InvalidOperationError
    history = TransferHistory()
    history.player_id = player.id
    history.from_club_id = player.club_id
    history.to_club_id = UUID(transfer_data.new_club)
    history.contract_start = transfer_data.start_date
    history.contract_end = transfer_data.end_date
    history.transfer_fee = transfer_data.fee
    return history
    history.transfer_fee = transfer_data.fee
    return history
