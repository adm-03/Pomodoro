from fastapi import FastAPI, APIRouter
from app.settings import Settings

router = APIRouter(prefix="/ping", tags=["ping-app, ping-db"])

@router.get("/app")
async def ping(name: str):
    settings = Settings()

    return {"message": "ok"}

@router.get("/bd")
async def ping(name: str):
    return {"text": "ok"}