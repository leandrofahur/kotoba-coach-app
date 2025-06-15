from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Agent Simulation API",
    description="This is the API for the Agent Simulation project.",
    version="1.0.0",
    contact={
        "name": "Agent Simulation API",
        "url": "https://github.com/leandrofahur/agent-playground-gui",                        
    },
    openapi_tags=swagger_metadata_config()
)

# Add the router to the app
router = APIRouter(prefix="/api/v1")

@router.get("/")
def read_root():
    return {"message": "Hello, World!"}

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