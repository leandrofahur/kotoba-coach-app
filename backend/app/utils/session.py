from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime
from core.session_store import SESSION_STORE

security = HTTPBearer()

def validate_session_token(credentials: HTTPAuthorizationCredentials = Depends(security)):            
    token = credentials.credentials
    session = SESSION_STORE.get(token)

    if not session:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session token")

    if datetime.now() > session["expires_at"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session expired")

    return {"token": token, "session": SESSION_STORE}