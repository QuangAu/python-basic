import uuid
from sqlalchemy import UUID, Column, String
from schemas.base_entity import Base_Migration


class Client(Base_Migration):
    __tablename__ = "client"
    client_id = Column(primary_key=True, type_=UUID, default=uuid.uuid4)
    client_secret = Column(String(50), nullable=False)
    scopes = Column(String)
