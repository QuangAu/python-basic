
import decimal
from datetime import date

from pydantic import BaseModel, field_serializer


class TransferHistoryViewModel(BaseModel):
    player_name: str
    transfer_fee: decimal.Decimal
    contract_start: date
    contract_end: date
    from_club: str | None = None
    to_club: str | None = None

    @field_serializer("transfer_fee")
    def decimal_custom_serializer(self, field_value: decimal.Decimal):
        return round(decimal.Decimal(field_value), 0)
