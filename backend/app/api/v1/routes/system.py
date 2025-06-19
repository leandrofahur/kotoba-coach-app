from fastapi import APIRouter
from uuid import uuid4
from datetime import datetime, timedelta

from models.session import SessionResponse

# Session store is a simple in-memory store for the session token and the expiration time.
SESSION_STORE = {}
SESSION_DURATION_MINUTES = 15

router = APIRouter(
    prefix="/system",
    tags=["System"],
)

@router.post("/session/start")
def start_session() -> SessionResponse:
    session_token = uuid4()
    expires_at = datetime.now() + timedelta(minutes=SESSION_DURATION_MINUTES)
    SESSION_STORE[session_token] = expires_at    
    return SessionResponse(session_token=session_token, expires_at=expires_at)

@router.post("/session/end")
def end_session():
    return {"message": "Hello from end session"}

@router.get("/health")
def health_check():
    return {"status": "ok"}