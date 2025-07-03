from fastapi import APIRouter, Depends, Form, File, UploadFile, HTTPException
from utils.session import validate_session_token

from services.phrase_service import get_phrase_by_id
from services.audio_service import prepare_audio
from services.whisper_service import transcribe_audio
from services.feedback_service import analyze_comprehensive_pronunciation
from services.morae_service import extract_morae 
from services.pitch_service import extract_pitch_librosa

router = APIRouter(prefix="/pronunciation", 
                   tags=["Pronunciation"],
                #    dependencies=[Depends(validate_session_token)]     
)

@router.post("/evaluate")
async def evaluate_pronunciation(phrase_id: str =Form(...), audio_file: UploadFile = File(...)):
    # get the phrase by id:
    phrase = get_phrase_by_id(phrase_id)

    if not phrase:
        raise HTTPException(status_code=404, detail="Page Not Found")
    
    #  process the audio file:
    audio_path = await prepare_audio(audio_file)
    transcription = transcribe_audio(audio_path)

    # extract the pitch data:
    pitch_contour = extract_pitch_librosa(audio_path)

    # Comprehensive pronunciation analysis
    analysis = analyze_comprehensive_pronunciation(
        expected_phrase=phrase.text,
        transcription=transcription,
        pitch_values=pitch_contour
    )

    # return the comprehensive analysis:
    return {
        "phrase": phrase,
        **analysis  # Include all analysis results
    }