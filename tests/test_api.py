
import sys  
sys.path.append('app')
from app.models.player import SearchPlayerModel
from app.services import player as PlayerService
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def test_get_player():
    USERNAME = "postgres"
    PASSWORD = "123123"
    DB_HOST = "localhost"
    DB_NAME = "fastapi"
    engine = create_engine(f"postgresql://{USERNAME}:{PASSWORD}@{DB_HOST}/{DB_NAME}")
    session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = session_local()
    condition = SearchPlayerModel("John", None)
    result = PlayerService.get_players(db, condition)
    assert not result