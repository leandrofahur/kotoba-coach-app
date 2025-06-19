from fastapi import APIRouter
from uuid import uuid4
from datetime import datetime, timedelta

from models.session import SessionResponse
from core.session_store import SESSION_STORE, SESSION_DURATION_MINUTES

router = APIRouter(
    prefix="/system",
    tags=["System"],
)

@router.post("/session/start")
def start_session() -> SessionResponse:
    session_token = str(uuid4())
    expires_at = datetime.now() + timedelta(minutes=SESSION_DURATION_MINUTES)
    SESSION_STORE[session_token] = expires_at    
    return SessionResponse(session_token=session_token, expires_at=expires_at)

@router.get("/health")
def health_check():
    return {"status": "ok"}