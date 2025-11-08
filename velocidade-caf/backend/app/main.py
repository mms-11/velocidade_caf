from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.api.v1 import users

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])


@app.get("/")
def root():
    """Health check."""
    return {
        "message": "Velocidade CAF API",
        "version": settings.VERSION,
        "status": "online"
    }


@app.get("/health")
def health():
    """Health check detalhado."""
    return {"status": "healthy"}