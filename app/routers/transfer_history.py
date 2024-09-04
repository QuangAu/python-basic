
from typing import List
from fastapi import APIRouter, Depends
from starlette import status
from sqlalchemy.orm import Session
from models.transfer_history import TransferHistoryViewModel
from dependencies import db_context
from services import transfer_history as TransferHistoryService

router = APIRouter(prefix="/transfers", tags=["Transfer History"])


@router.get("", status_code=status.HTTP_200_OK, response_model=List[TransferHistoryViewModel])
async def get_transfer_histories(
    db: Session = Depends(db_context)
):
    result = TransferHistoryService.get_transfer_histories(db)
    return result

