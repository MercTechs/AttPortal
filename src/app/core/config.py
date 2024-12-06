from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='.env', override=True)  # Load the .env file

class Settings(BaseSettings):

    # App configuration
    DEBUG: bool = False
    POSTGRES_USER: str = os.getenv('POSTGRES_USER', "")
    POSTGRES_PASSWORD: str = os.getenv('POSTGRES_PASSWORD', "")
    POSTGRES_PORT: int = int(os.getenv('POSTGRES_PORT', 5432))
    POSTGRES_SERVER: str = os.getenv('POSTGRES_SERVER', 'localhost')
    POSTGRES_DB: str = os.getenv('POSTGRES_DB', "attendance_db")
    POSTGRES_URL: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

    # External API configuration
    EXTERNAL_API_URL: str = os.getenv('EXTERNAL_API_URL', "http://192.168.2.120:6900/api/hpa/Paradise")
    EXTERNAL_API_USER: str = os.getenv('EXTERNAL_API_USER', "admin")
    EXTERNAL_API_PASSWORD: str = os.getenv('EXTERNAL_API_PASSWORD', "1234")
    ACCESS_CODE: str = os.getenv('ACCESS_CODE', "X7#mK9pL$fR2")

settings = Settings()