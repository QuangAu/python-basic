from sqlalchemy import Boolean, Column, String
from schemas.base_entity import BaseEntity
from services.database import Base


class User(Base, BaseEntity):
    __tablename__ = "user"
    login_id = Column(String(50), nullable=False, unique=True)
    password = Column(String, nullable=False)
    name = Column(String(50), nullable=False)
    is_admin = Column(Boolean, nullable=False, default=False)
    is_active = Column(Boolean, nullable=False, default=True)
