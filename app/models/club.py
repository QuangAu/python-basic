import decimal
from pydantic import BaseModel, Field, field_serializer


class SearchClubModel:
    def __init__(self, club_name, page=1, size=5) -> None:
        self.club_name = club_name
        self.page = page
        self.size = size
        
class ClubViewModel(BaseModel):
    club_name: str
    country: str
    rank: int
    market_value: decimal.Decimal
    
    @field_serializer("market_value")    
    def decimal_custom_serializer(self, field_value: decimal.Decimal):
        return round(decimal.Decimal(field_value), 0)
        


class ClubModel(BaseModel):
    club_name: str = Field(max_length=50, min_length=2)
    country: str = Field(max_length=50, min_length=2)
    rank: int = Field(gt=0)
    market_value: decimal.Decimal = Field(gt=0)

    class Config:
        json_schema_extra = {
            "example": {
                "club_name": "Liverpool",
                "country": "England",
                "rank": 1,
                "market_value": 100000000,
            }
        }
