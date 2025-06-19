from fastapi import APIRouter
from services.phrase_service import get_all_phrases, get_phrase_by_id

router = APIRouter(prefix="/phrase", tags=["Phrase"])

@router.get("/")
def get_phrases(id: str = None):
    if not id:
        return get_all_phrases()
    else:
        return get_phrase_by_id(id)


