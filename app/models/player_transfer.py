from datetime import date
import decimal
from uuid import UUID

from pydantic import BaseModel
from schemas.club import Club
from schemas.player import Player


class PlayerTransfer(BaseModel):
    new_club: str
    fee: decimal.Decimal
    start_date: date
    end_date: date