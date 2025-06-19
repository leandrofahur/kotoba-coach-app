from fastapi import APIRouter

router = APIRouter(prefix="/pronunciation", tags=["Pronunciation"])

@router.post("/evaluate")
def evaluate_pronunciation():
    return {"message": "Hello from evaluate pronunciation"}