import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.api.v1 import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS + ["http://localhost:8000", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routes
app.include_router(api_router, prefix=settings.API_V1_STR)

# Frontend paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
STATIC_DIR = FRONTEND_DIR / "static"
TEMPLATES_DIR = FRONTEND_DIR / "templates"

# Mount static files (CSS, JS, images)
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
    print(f"✓ Servindo arquivos estáticos de: {STATIC_DIR}")
else:
    print(f"⚠ Pasta de arquivos estáticos não encontrada: {STATIC_DIR}")

# Helper function to serve HTML files
def serve_html(filename: str):
    """Serve HTML file from templates directory."""
    file_path = TEMPLATES_DIR / filename
    if file_path.exists():
        return FileResponse(file_path)
    return HTMLResponse(content="<h1>404 - Página não encontrada</h1>", status_code=404)

# Frontend routes
@app.get("/", include_in_schema=False)
async def serve_index():
    """Página inicial - login."""
    return serve_html("index.html")

@app.get("/index.html", include_in_schema=False)
async def serve_login():
    """Página de login."""
    return serve_html("index.html")

@app.get("/register.html", include_in_schema=False)
async def serve_register():
    """Página de registro."""
    return serve_html("register.html")

# Athlete routes
@app.get("/athlete-analises.html", include_in_schema=False)
async def serve_athlete_dashboard():
    """Dashboard do atleta - análises."""
    return serve_html("athlete-analises.html")

@app.get("/dashboard2.html", include_in_schema=False)
async def serve_athlete_perfil():
    """Página de perfil do atleta."""
    return serve_html("dashboard2.html")

@app.get("/dashboard3.html", include_in_schema=False)
async def serve_athlete_marks():
    """Página de marcas do atleta."""
    return serve_html("dashboard3.html")

@app.get("/dash1.html", include_in_schema=False)
async def serve_athlete_stats():
    """Página de estatísticas do atleta."""
    return serve_html("dash1.html")

# Coach routes
@app.get("/coach-dash.html", include_in_schema=False)
async def serve_coach_dashboard():
    """Dashboard do treinador."""
    return serve_html("coach-dash.html")

@app.get("/coach-analise.html", include_in_schema=False)
async def serve_coach_analise():
    """Página de análise de atletas do treinador."""
    return serve_html("coach-analise.html")

@app.get("/coach-config.html", include_in_schema=False)
async def serve_coach_config():
    """Página de configurações do treinador."""
    return serve_html("coach-config.html")

@app.get("/coach-testes.html", include_in_schema=False)
async def serve_coach_testes():
    """Página de testes do treinador."""
    return serve_html("coach-testes.html")

# API health check
@app.get("/health")
def health():
    """Health check da API."""
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "frontend": "enabled" if TEMPLATES_DIR.exists() else "disabled"
    }

# Startup event
@app.on_event("startup")
async def startup_event():
    """Log de inicialização."""
    print("\n" + "="*60)
    print(f"🚀 {settings.PROJECT_NAME} v{settings.VERSION}")
    print("="*60)
    print(f"📚 API Docs: http://localhost:8000/docs")
    print(f"🌐 Frontend: http://localhost:8000")
    print(f"📊 ReDoc: http://localhost:8000/redoc")
    print("="*60 + "\n")