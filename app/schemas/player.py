from schemas.base_entity import BaseAudit, BaseEntity
from schemas.enum.player_position import PlayerPosition
from services.database import Base
from sqlalchemy import UUID, Column, Enum, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship


class Player(Base, BaseEntity, BaseAudit):
    __tablename__ = "player"
    player_name = Column(String(50), nullable=False)
    age = Column(Integer)
    nationality = Column(String(50), nullable=False)
    position = Column(Enum(PlayerPosition), nullable=False)
    market_value = Column(Numeric(asdecimal=True))

    club_id = Column(UUID(), ForeignKey("club.id"))
    club = relationship("Club", back_populates="player")
