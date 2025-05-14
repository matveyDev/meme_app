# === main.py ===
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from config.settings import settings
from app.routes import router as meme_router
import os

app = FastAPI(
    title="Meme App API",
    description="API for generating memes with Leonardo AI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register router
app.include_router(meme_router)

# Ensure the static directory exists
os.makedirs(settings.STATIC_FOLDER, exist_ok=True)

# Mount static files directory
app.mount("/generated", StaticFiles(directory=str(settings.STATIC_FOLDER)), name="generated")

# Root route
@app.get("/")
async def root():
    return {"message": "Welcome to Meme App API"}

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
