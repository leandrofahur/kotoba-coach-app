from typing import List
from fastapi import APIRouter

from models.phrase import Phrase
from services.phrase_service import get_all_phrases, get_phrase_by_id

router = APIRouter(prefix="/phrase", tags=["Phrase"])

@router.get("/")
def get_phrases() -> List[Phrase]:
    return get_all_phrases()
    
@router.get("/{id}")
def get_phrase(id: str) -> Phrase:
    return get_phrase_by_id(id)
