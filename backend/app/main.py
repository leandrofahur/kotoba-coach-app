from fastapi import FastAPI, APIRouter, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import tempfile
from utils.audio import score_user_audio

# Import the audio utils
from utils.audio import AUDIO_PATH

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
    print(AUDIO_PATH)
    return {"message": "Hello, World!"}

@router.post("/score")
async def get_score(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_path = temp_audio.name
        content = await file.read()
        temp_audio.write(content)

    score = score_user_audio(temp_path)
    return {"score": score}


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