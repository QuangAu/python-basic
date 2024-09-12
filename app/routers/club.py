from typing import List
from fastapi import APIRouter, Depends, Query
from starlette import status
from sqlalchemy.orm import Session
from models.club import ClubModel, ClubViewModel, SearchClubModel
from dependencies import get_db_session
from services import club as ClubService


router = APIRouter(prefix="/clubs", tags=["Club"])


@router.get("", status_code=status.HTTP_200_OK, response_model=List[ClubViewModel])
async def get_clubs(
    db: Session = Depends(get_db_session),
    club_name: str = Query(default=None),
    page: int = Query(ge=1, default=1),
    size: int = Query(ge=1, le=50, default=10),
):
    result = ClubService.get_clubs(db, SearchClubModel(club_name, page, size))
    return result


@router.post("", status_code=status.HTTP_201_CREATED)
async def add_new_club(request: ClubModel, db: Session = Depends(get_db_session)):
    return ClubService.add_new_club(db, request)
