import os
from fastapi import FastAPI, APIRouter, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

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

@router.post("/score")
def score_audio(file: UploadFile = File(...)):
    return {"filename": file.filename}

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