from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, simulation

app = FastAPI(title="B-Bot API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://bbot.vercel.app", "https://b-bot-mik-version.vercel.app", "https://b-bot-mik-version-backend.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(simulation.router, prefix="/api/simulation", tags=["simulation"])


@app.get("/")
def read_root():
    return {"message": "B-Bot API is running"}
