from typing import List
from fastapi import APIRouter, Depends, Query
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from models.club import ClubModel, ClubViewModel, SearchClubModel
from services.database import get_db_context
from services import club as ClubService


router = APIRouter(prefix="/clubs", tags=["Club"])


@router.get("", status_code=status.HTTP_200_OK, response_model=List[ClubViewModel])
async def get_clubs(
    db: AsyncSession = Depends(get_db_context),
    club_name: str = Query(default=None),
    page: int = Query(ge=1, default=1),
    size: int = Query(ge=1, le=50, default=10),
):
    result = await ClubService.get_clubs(db, SearchClubModel(club_name, page, size))
    return result


@router.post("", status_code=status.HTTP_201_CREATED)
async def add_new_club(request: ClubModel, db: AsyncSession = Depends(get_db_context)):
    return await ClubService.add_new_club(db, request)
