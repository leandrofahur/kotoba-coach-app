from fastapi import APIRouter, Depends
from utils.session import validate_session_token

router = APIRouter(prefix="/pronunciation", 
                   tags=["Pronunciation"],
                #    dependencies=[Depends(validate_session_token)]
)

@router.post("/evaluate")
def evaluate_pronunciation():    
    return {"message": "Hello from evaluate pronunciation"}