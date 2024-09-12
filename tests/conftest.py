from fastapi.testclient import TestClient
from sqlalchemy import create_engine  
import sys
sys.path.append('app')

from schemas.base_entity import Base_Migration
import pytest
from testcontainers.postgres import PostgresContainer
import app.settings
from sqlalchemy.orm import sessionmaker
from app.routers.player import get_db_session


postgres = PostgresContainer("postgres:16-alpine", username="postgres", password="123123", dbname="fastapi_test")
postgres.start()
        
engine = create_engine(postgres.get_connection_url(), echo=True)
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base_Migration.metadata.create_all(bind=engine, checkfirst=True)

@pytest.fixture(scope="session")
def client(request):
    def remove_container():
        postgres.stop()
        
    request.addfinalizer(remove_container)
    
    def set_db_context():
        try:
            db = session_local()
            yield db
        finally:
            db.close()
    
    from app.main import app        
    app.dependency_overrides[get_db_session] = set_db_context
    
    with TestClient(app) as client:
        yield client
        
