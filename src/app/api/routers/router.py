from fastapi.routing import APIRouter


from src.app.constants.enum import TAGS
from src.app.api.routers.attedance_report import router as attendance_router

api_router = APIRouter()


api_router.include_router(attendance_router, tags=[TAGS.attandance_report])
