
import settings
from settings import DB_ENGINE


def get_connection_string():
    match DB_ENGINE:
        case "sqlite":
            return f"sqlite:///{settings.DB_NAME}"
        case "postgresql":
            return f"postgresql+asyncpg://{settings.USERNAME}:{settings.PASSWORD}@{settings.DB_HOST}/{settings.DB_NAME}"
        case _:
            return f"postgresql://{settings.USERNAME}:{settings.PASSWORD}@{settings.DB_HOST}/{settings.DB_NAME}"
