from pydantic import BaseModel

class Phrase(BaseModel):
    id: str
    text: str
    romaji: str
    translation: str
    audio_url: str
    