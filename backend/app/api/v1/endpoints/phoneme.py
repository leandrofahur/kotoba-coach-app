from fastapi import APIRouter, File, UploadFile

router = APIRouter(
    prefix="/phoneme",
    tags=["Phoneme"],
)

@router.post("/score")
def phooneme_audio(file: UploadFile = File(...)):
    return {"filename": file.filename}