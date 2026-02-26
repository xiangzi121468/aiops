from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.api_v1.api import api_router
from app.core.config import settings
from app.db.session import Base, engine
from app.db import models  # noqa: F401

app = FastAPI(
    title="AIOps Evolution Platform",
    description="The Brain -> The Nervous System",
    version="0.1.0"
)

# CORS Configuration
origins = [
    "http://localhost:5173",  # Vite Frontend
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup() -> None:
    # Temporary init for dev; replace with Alembic migrations later.
    Base.metadata.create_all(bind=engine)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "0.1.0"}

@app.get("/")
async def root():
    return {"message": "Welcome to AIOps Brain API"}

