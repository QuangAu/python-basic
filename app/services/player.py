from uuid import UUID, uuid4
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from models.player_transfer import PlayerTransfer
from common.exception import InvalidOperationError, ResourceNotFoundError
from models.player import PlayerModel, SearchPlayerModel
from schemas.club import Club
from schemas.player import Player
from services import transfer_history as TransferHistoryService

def get_players(db_context: Session, condition: SearchPlayerModel):
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

    return db_context.execute(query).all()


def add_new_player(db_context: Session, data: PlayerModel):
    player = Player(**data.model_dump())
    db_context.add(player)
    db_context.commit()
    db_context.refresh(player)

    return player


def update_player(db_context: Session, player_id: UUID, data: PlayerModel):
    player = db_context.scalars(
        select(Player).filter(Player.id == UUID(player_id))
    ).first()

    if player is None:
        raise ResourceNotFoundError()

    player.player_name = data.player_name
    player.age = data.age
    player.position = data.position
    player.nationality = data.nationality
    player.market_value = data.market_value

    db_context.commit()
    db_context.refresh(player)

    return player


def set_player_club(db_context: Session, player_id: uuid4, club_id: uuid4):
    player = db_context.scalars(
        select(Player).filter(Player.id == UUID(player_id))
    ).first()

    if player is None:
        raise ResourceNotFoundError()

    club = db_context.scalars(select(Club).filter(Club.id == UUID(club_id))).first()
    if club is None:
        raise ResourceNotFoundError()

    player.club_id = club.id
    db_context.commit()
    db_context.refresh(player)

    return player


def transfer_player(db_context: Session, data: PlayerTransfer):
    player = db_context.scalars(
        select(Player).filter(Player.id == UUID(data.player_id))
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
    db_context.commit()
    db_context.refresh(player)

    return player