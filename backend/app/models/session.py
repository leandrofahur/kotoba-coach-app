from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class SessionResponse(BaseModel):
    session_token: UUID
    expires_at: datetime