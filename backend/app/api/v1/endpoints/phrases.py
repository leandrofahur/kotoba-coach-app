from fastapi import APIRouter

router = APIRouter(
    prefix="/phrases",
    tags=["Phrases"],
)

@router.get("/phrases")
def get_phrases():    
    return {"phrases": "ok"}