"""
Importa todos os modelos para que o Alembic os detecte.
"""
from app.models.user import User, AthleteProfile, CoachProfile
from app.models.jump import Jump
from app.models.mark import Mark

__all__ = [
    "User",
    "AthleteProfile", 
    "CoachProfile",
    "Jump",
    "Mark",
]