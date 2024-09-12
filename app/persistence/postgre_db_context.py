import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from persistence.Abstraction.database import database
import settings


class PostgreDbContext(database):
    
    def __init__(self, connection_string: str=None) -> None:
        super().__init__(connection_string)
        self.engine = create_engine(self._connection_string)

    def get_connection_string(self, async_mode=False):
        """Get the connection string for the database

        Returns:
            string: The connection string
        """
        return f"postgresql://{settings.USERNAME}:{settings.PASSWORD}@{settings.DB_HOST}/{settings.DB_NAME}"

    
    def get_db_context(self):
        try:
            session_local = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            db = session_local()
            yield db
        finally:
            db.close()

    
    