from typing import List
from fastapi import APIRouter, Depends, Query
from starlette import status
from sqlalchemy.orm import Session
from models.player_transfer import PlayerTransfer
from models.player import PlayerModel, PlayerViewModel, SearchPlayerModel
from dependencies import get_db_session
from services import player as PlayerService


router = APIRouter(prefix="/players", tags=["Player"])


@router.get("", status_code=status.HTTP_200_OK, response_model=List[PlayerViewModel])
async def get_players(
    player_name: str = Query(default=None),
    club_name: str = Query(default=None),
    page: int = Query(ge=1, default=1),
    size: int = Query(ge=1, le=50, default=10),
    db: Session = Depends(get_db_session)
):
    condition = SearchPlayerModel(player_name, club_name, page, size)
    result = PlayerService.get_players(db, condition)
    return result


@router.put("/{player_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_player(
    player_id: str, request: PlayerModel, db: Session = Depends(get_db_session)
):
    return PlayerService.update_player(db, player_id, request)


@router.post("", status_code=status.HTTP_201_CREATED)
async def add_new_player(request: PlayerModel, db: Session = Depends(get_db_session)):
    return PlayerService.add_new_player(db, request)


@router.patch(
    "/{player_id}/club", status_code=status.HTTP_202_ACCEPTED, response_model=PlayerViewModel
)
async def set_player_club(
    player_id: str, club_id: str, db: Session = Depends(get_db_session)
):
    return PlayerService.set_player_club(db, player_id, club_id)

@router.post("/{player_id}/transfer", status_code=status.HTTP_202_ACCEPTED)
async def transfer_player(player_id: str, request: PlayerTransfer, db: Session = Depends(get_db_session)):
    return PlayerService.transfer_player(db, player_id, request)