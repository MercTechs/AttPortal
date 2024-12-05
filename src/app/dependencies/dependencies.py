
from src.app.db.postgres import PostgresManager
from src.app.services.attendance_service import AttendanceService

def get_postgres_manager():
    postgres_manager = PostgresManager()
    session = postgres_manager.Session()
    try:
        yield session
    finally:
        session.close()

def get_attendance_service() -> AttendanceService:
    return AttendanceService()