from fastapi import APIRouter, File, UploadFile

router = APIRouter(
    prefix="/evaluate",
    tags=["Evaluate"],
)

@router.post("/score")
def evaluate_audio(file: UploadFile = File(...)):
    return {"filename": file.filename}