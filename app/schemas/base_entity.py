import uuid

from sqlalchemy import UUID, Column, DateTime, func


class BaseAudit:
    created_by = Column(type_=UUID, nullable=True, default=uuid.uuid4)
    created_at = Column(type_=DateTime, nullable=False, server_default=func.now())
    updated_by = Column(type_=UUID, nullable=True, default=uuid.uuid4)
    updated_at = Column(
        type_=DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )


class BaseEntity:
    id = Column(primary_key=True, type_=UUID, default=uuid.uuid4)
    id = Column(primary_key=True, type_=UUID, default=uuid.uuid4)
