from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from api.v1.routes import system, pronunciation
from api.v1.routes import phrase

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
router.include_router(system.router)
router.include_router(pronunciation.router)
router.include_router(phrase.router)

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