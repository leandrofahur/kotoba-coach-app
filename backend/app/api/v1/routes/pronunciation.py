from fastapi import APIRouter, Depends, Form, File, UploadFile, HTTPException
from utils.session import validate_session_token

from services.phrase_service import get_phrase_by_id
from services.audio_service import prepare_audio
from services.whisper_service import transcribe_audio
from services.feedback_service import calculate_similarity, label_from_score
from services.morae_service import extract_morae 
from services.pitch_service import extract_pitch_librosa

router = APIRouter(prefix="/pronunciation", 
                   tags=["Pronunciation"],
                #    dependencies=[Depends(validate_session_token)]     # TODO: Uncomment this for production
)

@router.post("/evaluate")
async def evaluate_pronunciation(phrase_id: str =Form(...), audio_file: UploadFile = File(...)):
    # get the phare by id:
    phrase = get_phrase_by_id(phrase_id)

    if not phrase:
        raise HTTPException(status_code=404, detail="Page Not Found")
    
    #  process the audio file:
    audio_path = await prepare_audio(audio_file)
    transcription = transcribe_audio(audio_path)

    # calculate the similarity score:
    similarity_score = calculate_similarity(transcription, phrase.text)
    label = label_from_score(similarity_score)

    # extract the morae:
    morae = extract_morae(phrase.text)    

    # extract the pitch data:
    pitch_contour = extract_pitch_librosa(audio_path)

    # return the phrase:
    return {        
        "phrase": phrase,
        "transcription": transcription,        
        "score": similarity_score,
        "label": label,
        "expected_morae": morae,
        "actual_pitch_contour": pitch_contour
    }