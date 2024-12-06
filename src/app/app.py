import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.app.api.routers.router import api_router
from fastapi.openapi.utils import get_openapi
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

origins = [
    "http://localhost",
    "http://localhost:8080",
    "*",
]

app = FastAPI(title="Attendance API", docs_url="/docs")

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Attendance API",
        version="1.0.0",
        description="API for attendance management",
        routes=app.routes,
    )

    if "components" not in openapi_schema:
        openapi_schema["components"] = {}
    
    if "schemas" not in openapi_schema["components"]:
        openapi_schema["components"]["schemas"] = {}

    openapi_schema["components"]["securitySchemes"] = {
        "AccessCode": {
            "type": "apiKey",
            "in": "header",
            "name": "X-Access-Code",
            "description": "Enter your access code"
        }
    }

    openapi_schema["security"] = [{"AccessCode": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=api_router, prefix="/api")