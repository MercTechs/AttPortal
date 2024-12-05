import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.app.api.routers.router import api_router
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

origins = [
    "http://localhost",
    "http://localhost:8080",
    "*",
]


app = FastAPI(title="Attendance API", docs_url="/docs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=api_router, prefix="/api")
