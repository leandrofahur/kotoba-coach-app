from fastapi import FastAPI, APIRouter, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from api.v1.endpoints import evaluate, phoneme, system

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

router.include_router(evaluate.router)
router.include_router(phoneme.router)
router.include_router(system.router)

# @app.get("/test-phonemes")
# def get_phonemes():
#     phrase = "おはようございます"
#     phonemes = pyopenjtalk.g2p(phrase, kana=False)
#     return {"phrase": phrase, "phonemes": phonemes}

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