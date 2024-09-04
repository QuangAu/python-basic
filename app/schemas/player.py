from sqlalchemy import UUID, Column, Enum, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship
from schemas.base_entity import BaseAudit, BaseEntity, Base_Migration
from schemas.enum.player_position import PlayerPosition


class Player(Base_Migration, BaseEntity, BaseAudit):
    __tablename__ = "player"
    player_name = Column(String(50), nullable=False)
    age = Column(Integer)
    nationality = Column(String(50), nullable=False)
    position = Column(Enum(PlayerPosition), nullable=False)
    market_value = Column(Numeric(asdecimal=True))

    club_id = Column(UUID(), ForeignKey("club.id"))
    club = relationship("Club", back_populates="player")
