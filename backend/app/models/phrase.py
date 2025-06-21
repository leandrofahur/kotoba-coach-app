from pydantic import BaseModel
from enum import Enum

class PhraseStatus(str, Enum):
    NOT_STARTED = "not-started"
    IN_PROGRESS = "in-progress"
    COMPLETED = "completed"

class Phrase(BaseModel):
    id: str
    text: str
    romaji: str
    translation: str
    audio_url: str
    status: PhraseStatus
    