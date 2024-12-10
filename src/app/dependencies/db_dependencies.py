from contextlib import asynccontextmanager
from src.app.db.postgres import PostgresManager

@asynccontextmanager
async def get_postgres_manager():
    postgres_manager = PostgresManager()
    session = postgres_manager.Session()
    try:
        yield session
    finally:
        session.close()
