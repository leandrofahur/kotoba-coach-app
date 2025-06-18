from fastapi import FastAPI, APIRouter, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from utils.audio import process_audio_in_memory, load_reference_audio, calculate_similarity_score

app = FastAPI(
    title="KotobaCoach API",
    description="This is the API for the japanese speaking audio score assistant.",
    version="1.0.0",
    contact={
        "name": "KotobaCoach API",
        "url": "https://github.com/leandrofahur/kotoba-coach-app",                        
    },
    # openapi_tags=swagger_metadata_config()
)

# Add the router to the app
router = APIRouter(prefix="/api/v1")

@router.get("/")
def read_root():    
    return {"message": "Hello, World!"}

# TODO: Add a function to save the uploaded audio files for a tracking system:
# @router.post("/upload_audio")
# def upload_audio_file(uploaded_file: UploadFile = File(...)):
#     fp = save_uploaded_audio(uploaded_file)
#     return {"status": "success", "file": fp}
    

@router.post("/score")
def score_audio(file: UploadFile = File(...)):
    # Validate file
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    # Read file content into memory
    try:
        audio_content = file.file.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to read uploaded file")
    
    # Process audio in memory
    user_audio_result = process_audio_in_memory(audio_content)
    if not user_audio_result:
        raise HTTPException(status_code=400, detail="Invalid audio file")
    
    user_audio, user_sr = user_audio_result
    
    # Load reference audio
    reference_audio, ref_sr = load_reference_audio()
    
    # Calculate score using MFCC
    score = calculate_similarity_score(user_audio, user_sr, reference_audio, ref_sr)
    
    return {
        "filename": file.filename,
        "score": score,  # Now guaranteed to be Python float
        "message": "Audio processed successfully using MFCC analysis",
        "audio_duration_user": round(float(len(user_audio) / user_sr), 2),  # Convert to Python float
        "audio_duration_reference": round(float(len(reference_audio) / ref_sr), 2)  # Convert to Python float
    }

@router.get("/health")
def health_check():
    return {"status": "ok"}

# Add the router to the app
app.include_router(router)

# Enable communication between frontend and backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)