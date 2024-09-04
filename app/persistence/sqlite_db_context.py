import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from settings import DB_NAME
from persistence.Abstraction.database import database
from sqlalchemy.ext.declarative import declarative_base


class SqliteDbContext(database):
    Base = declarative_base()
    
    def __init__(self) -> None:
        super().__init__()
        connection_string = self.get_connection_string()
        self.engine = create_engine(connection_string)
        

    def get_connection_string(self, async_mode=False):
        """Get the connection string for the database

        Returns:
            string: The connection string
        """
        return f"sqlite:///{DB_NAME}"

    def get_db_context(self):
        try:
            session_local = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            db = session_local()
            yield db
        finally:
            db.close()
