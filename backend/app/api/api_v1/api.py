from fastapi import APIRouter
from app.api.api_v1.endpoints import auth, evaluate, ingest, memory, retrieve, agent

api_router = APIRouter()
api_router.include_router(auth.router, tags=["login"])
api_router.include_router(ingest.router, tags=["ingest"])
api_router.include_router(retrieve.router, tags=["retrieve"])
api_router.include_router(memory.router, tags=["memory"])
api_router.include_router(evaluate.router, tags=["evaluate"])
api_router.include_router(agent.router, tags=["agent"])

