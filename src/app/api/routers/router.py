from fastapi.routing import APIRouter
from fastapi import Depends
from src.app.middleware.access_code import verify_access_code
from src.app.constants.enum import TAGS
from src.app.api.routers.attedance_report import router as base_attendance_router  

api_router = APIRouter()

# Create the protected router
protected_attendance_router = APIRouter(
    dependencies=[Depends(verify_access_code)],
    tags=[TAGS.attandance_report]
)

# Include the base routes in the protected router
protected_attendance_router.include_router(base_attendance_router)

# Include the protected router in the main api router
api_router.include_router(protected_attendance_router)