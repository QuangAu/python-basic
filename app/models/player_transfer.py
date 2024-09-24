import decimal
from datetime import date

from pydantic import BaseModel


class PlayerTransfer(BaseModel):
    new_club: str
    fee: decimal.Decimal
    start_date: date
    end_date: date
    end_date: date
