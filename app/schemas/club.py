from sqlalchemy import Column, Integer, Numeric, String
from sqlalchemy.orm import relationship
from schemas.base_entity import BaseEntity, BaseAudit
from services.database import Base


class Club(Base, BaseEntity, BaseAudit):
    __tablename__ = "club"
    club_name = Column(String(50), nullable=False)
    country = Column(String(50), nullable=False)
    rank = Column(Integer)
    market_value = Column(Numeric(asdecimal=True))

    player = relationship("Player", back_populates="club")
