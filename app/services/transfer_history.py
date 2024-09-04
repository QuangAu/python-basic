from uuid import UUID
from sqlalchemy import select, and_
from sqlalchemy.orm import Session, aliased
from common.exception import InvalidOperationError
from models.player_transfer import PlayerTransfer
from schemas.transfer_history import TransferHistory
from schemas.club import Club
from schemas.player import Player

def get_transfer_histories(db_context: Session):
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

    return db_context.execute(query).all()


def build_transfer_history(
    db_context: Session, player: Player, transfer_data: PlayerTransfer
) -> TransferHistory:
    existing_transfer = db_context.scalars(
        select(TransferHistory).filter(
            and_(
                TransferHistory.player_id == player.id,
                TransferHistory.from_club_id == player.club_id,
                TransferHistory.to_club_id == UUID(transfer_data.new_club),
                TransferHistory.contract_start == transfer_data.start_date,
                TransferHistory.contract_end == transfer_data.end_date
            )
        )
    ).first()
    
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
