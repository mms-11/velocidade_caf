"""
Script de inicialização do servidor de desenvolvimento.
"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=["app"],  # Monitora apenas a pasta app
        reload_excludes=[
            ".venv/**",
            "**/__pycache__/**",
            "**/*.pyc",
            "**/*.pyo",
            "**/alembic/**",
            "**/.git/**",
        ],
    )