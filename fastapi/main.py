from typing import Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.models_api import router as models_router
from api.chat_gpt_api import router as chatgpt_router

app = FastAPI(
    title="Meme App API",
    description="API for managing memes, spices, animals and users",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI endpoint
    redoc_url="/redoc"  # ReDoc endpoint
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Vue.js development server
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(models_router, prefix="/api", tags=["models"])
app.include_router(chatgpt_router, prefix="/api/chatgpt", tags=["chatgpt"])

@app.get("/")
async def root():
    return {"message": "Welcome to Meme App API"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

