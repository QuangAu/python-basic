from sqlalchemy import Column, Date, ForeignKey, Numeric, UUID
from sqlalchemy.orm import relationship
from schemas.base_entity import BaseEntity, BaseAudit
from services.database import Base


class TransferHistory(Base, BaseEntity, BaseAudit):
    __tablename__ = "transfer_history"
    contract_start = Column(type_=Date, nullable=False)
    contract_end = Column(type_=Date, nullable=False)
    transfer_fee = Column(Numeric(asdecimal=True))

    player_id = Column(UUID(), ForeignKey("player.id"), nullable=False)
    player = relationship("Player", foreign_keys=[player_id])

    from_club_id = Column(UUID(), ForeignKey("club.id"))
    from_club = relationship("Club", foreign_keys=[from_club_id])

    to_club_id = Column(UUID(), ForeignKey("club.id"))
    to_club = relationship("Club", foreign_keys=[to_club_id])
