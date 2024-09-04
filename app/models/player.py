import decimal
from pydantic import BaseModel, Field, field_serializer
from schemas.enum.player_position import PlayerPosition


class SearchPlayerModel:
    def __init__(self, player_name, club_name, page=1, size=5) -> None:
        self.player_name = player_name
        self.club_name = club_name
        self.page = page
        self.size = size


class PlayerModel(BaseModel):
    player_name: str = Field(max_length=50, min_length=5)
    age: int = Field(ge=16, le=60)
    nationality: str = Field(max_length=50, min_length=2)
    position: PlayerPosition = Field()
    market_value: decimal.Decimal = Field(gt=0)

    class Config:
        json_schema_extra = {
            "example": {
                "player_name": "John Doe",
                "age": 20,
                "nationality": "English",
                "position": PlayerPosition.to_string(),
                "market_value": 10000000,
            }
        }


class PlayerViewModel(BaseModel):
    player_name: str
    age: int
    nationality: str
    position: PlayerPosition
    market_value: decimal.Decimal
    club_name: str | None = None

    @field_serializer("market_value")
    def decimal_custom_serializer(self, field_value: decimal.Decimal):
        return round(decimal.Decimal(field_value), 0)
