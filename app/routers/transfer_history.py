
from typing import List

from fastapi import APIRouter, Depends
from models.transfer_history import TransferHistoryViewModel
from services import transfer_history as TransferHistoryService
from services.database import get_db_context
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

router = APIRouter(prefix="/transfers", tags=["Transfer History"])


@router.get("", status_code=status.HTTP_200_OK, response_model=List[TransferHistoryViewModel])
async def get_transfer_histories(
    db: AsyncSession = Depends(get_db_context)
):
    result = await TransferHistoryService.get_transfer_histories(db)
    return result
