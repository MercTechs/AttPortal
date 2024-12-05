from typing import List
import sqlalchemy
from sqlalchemy import (
    create_engine,
    Table,
    Column,
    MetaData,
    text,
)
from sqlalchemy.orm import sessionmaker


from src.app.core.config import settings
from src.app.repositories.base_repository import ITableRepository
from src.app.models.entities.orm import Base

class PostgresManager(ITableRepository):
    def __init__(self) -> None:
        try:
            self.engine = create_engine(settings.POSTGRES_URL)
            self.engine.connect()
            # Create all tables defined in models
            Base.metadata.create_all(self.engine)  
        except Exception as e:
            print(str(e))
            self.engine = create_engine(settings.POSTGRES_URL + '/postgres')
            self.create_database(settings.POSTGRES_DB)
        finally:
            try:
                self.engine = create_engine(settings.POSTGRES_URL)
                self.metadata = MetaData()
                self.Session = sessionmaker(bind=self.engine)
                # Create all tables after database is created
                Base.metadata.create_all(self.engine)  
            except Exception as e:
                print(f"Failed to initialize PostgresManager: {e}")

    def create_database(self, database_name: str) -> None:
        try:
            conn = self.engine.connect()
            conn.execute(sqlalchemy.sql.text("commit"))
            conn.execute(sqlalchemy.sql.text(f"create database {database_name}"))
            conn.close()
        except Exception as e:
            print(f"Failed to create database: {e}")

    def create_table(self, table_name: str, columns: List[Column] = []) -> None:
        try:
            if not self.has_table(table_name=table_name):
                table = Table(table_name, self.metadata, *columns)
                table.create(self.engine)
                return
            raise ValueError(f"Table {table_name} already exists")
        except Exception as e:
            print(f"Failed to create table {table_name}: {e}")

    def table_metadata(self, table_name: str) -> dict:
        try:
            if self.has_table(table_name=table_name):
                table = Table(
                    table_name, self.metadata, autoload=True, autoload_with=self.engine
                )
                return {
                    "name": table.name,
                    "columns": [column.name for column in table.columns],
                }
            raise TableNotFoundException(table_name)
        except Exception as e:
            print(f"Failed to get table metadata for {table_name}: {e}")
            return {}

    def has_table(self, table_name: str) -> bool:
        try:
            inspector = sqlalchemy.inspect(self.engine)
            return table_name in inspector.get_table_names()
        except Exception as e:
                print(f"Failed to check if table exists {table_name}: {e}")
                return False

    def delete_table(self, table_name: str) -> None:
        try:
            if self.has_table(table_name=table_name):
                table = Table(table_name, self.metadata)
                table.drop(self.engine)
                return
            raise TableNotFoundException(table_name)
        except Exception as e:
            print(f"Failed to delete table {table_name}: {e}")

    def update_table(self, old_name: str, new_name: str) -> Table:
        try:
            if self.has_table(table_name=old_name):
                with self.Session() as session:
                    session.execute(
                        text(f"ALTER TABLE {old_name} RENAME TO {new_name}")
                    )
                    session.commit()
                return self.get_table(new_name)
            raise TableNotFoundException(old_name)
        except Exception as e:
            print(f"Failed to update table from {old_name} to {new_name}: {e}")
            raise TableNotFoundException(old_name)

    def list_tables(self) -> List[str]:
        try:
            with self.Session() as session:
                tables = session.execute(
                    text(
                        "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
                    )
                )
                return [row[0] for row in tables]
        except Exception as e:
            print(f"Failed to list tables: {e}")
            return []

    def get_table(self, table_name: str) -> Table:
        try:
            with self.Session() as session:
                table = session.execute(
                    sqlalchemy.sql.text(
                        f"SELECT * FROM information_schema.tables WHERE table_schema = 'public' AND table_name = '{table_name}'"
                    )
                )
                res = []
                for row in table:
                    temp = []
                    for i in row:
                        temp.append(i)
                    res.append(temp)
                return res # type: ignore
        except Exception as e:
            print(f"Failed to get table {table_name}: {e}")
            raise TableNotFoundException(table_name)
        

class TableNotFoundException(Exception):
    def __init__(self, table_name: str):
        super().__init__(f"Table {table_name} not found")