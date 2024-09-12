from functools import lru_cache
from persistence.postgre_db_context import PostgreDbContext
from persistence.sqlite_db_context import SqliteDbContext
from settings import DB_ENGINE
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@lru_cache
def get_db_engine():
    match DB_ENGINE:
        case "sqlite":
            context = SqliteDbContext()
        case "postgresql":
            context = PostgreDbContext()
        case __:
            context = SqliteDbContext()
            
    return context.engine


def get_db_session():
    try:
        session_local = sessionmaker(autocommit=False, autoflush=False, bind=get_db_engine())
        db = session_local()
        yield db
    finally:
        db.close()