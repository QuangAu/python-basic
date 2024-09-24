import asyncio
import sys
sys.path.append('app')

from httpx import AsyncClient
import pytest
import pytest_asyncio
from testcontainers.postgres import PostgresContainer
from app.routers.player import get_db_context

from app.main import app, sessionmanager



postgres = PostgresContainer("postgres:16-alpine", username="postgres", password="123123", dbname="fastapi_test", driver="asyncpg")
postgres.start()

@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
    

@pytest_asyncio.fixture(scope="session", autouse=True)
async def connection_test(request, event_loop):
    connection_str = postgres.get_connection_url()
    sessionmanager.init(connection_str)
    
    def stop_db():
        postgres.stop()

    request.addfinalizer(stop_db)
        
@pytest_asyncio.fixture(scope="session", autouse=True)
async def create_tables(connection_test):
    async with sessionmanager.get_db_connection() as connection:
        await sessionmanager.drop_all(connection)
        await sessionmanager.create_all(connection)    

@pytest_asyncio.fixture(scope="session", autouse=True)
async def session_override(connection_test):
    async def get_db_override():
        async with sessionmanager.get_db_session() as session:
            yield session

    app.dependency_overrides[get_db_context] = get_db_override

   

# @pytest.fixture(scope="session")
# async def client(request):
#     def remove_container():
#         postgres.stop()
        
#     request.addfinalizer(remove_container)
    
#     async with AsyncClient(
#         transport=ASGITransport(app=app), base_url="http://test"
#     ) as client:
#         yield client
   
# from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine, AsyncConnection, AsyncEngine
     
# @pytest.fixture(scope="module")
# def postgres_container():
#     with PostgresContainer("postgres:16-alpine", username="postgres", password="123123", dbname="fastapi_test", driver="asyncpg") as postgres:
#         yield postgres
        
@pytest_asyncio.fixture(scope="session")
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
    
