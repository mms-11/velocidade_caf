from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.user import CoachProfile  # MUDANÇA AQUI
from app.schemas import CoachProfileCreate, CoachProfileUpdate


def get_coach_by_id(db: Session, coach_id: str) -> Optional[CoachProfile]:
    """Busca treinador por ID."""
    return db.query(CoachProfile).filter(CoachProfile.id == coach_id).first()


def get_coach_by_user_id(db: Session, user_id: str) -> Optional[CoachProfile]:
    """Busca treinador por user_id."""
    return db.query(CoachProfile).filter(CoachProfile.user_id == user_id).first()


def get_coaches(db: Session, skip: int = 0, limit: int = 100) -> List[CoachProfile]:
    """Lista todos os treinadores."""
    return db.query(CoachProfile).offset(skip).limit(limit).all()


def create_coach(db: Session, coach_in: CoachProfileCreate) -> CoachProfile:
    """Cria novo perfil de treinador."""
    coach = CoachProfile(**coach_in.model_dump())
    db.add(coach)
    db.commit()
    db.refresh(coach)
    return coach


def update_coach(db: Session, coach: CoachProfile, coach_in: CoachProfileUpdate) -> CoachProfile:
    """Atualiza perfil de treinador."""
    update_data = coach_in.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(coach, field, value)
    
    db.add(coach)
    db.commit()
    db.refresh(coach)
    return coach


def delete_coach(db: Session, coach_id: str) -> bool:
    """Deleta perfil de treinador."""
    coach = get_coach_by_id(db, coach_id)
    if coach:
        db.delete(coach)
        db.commit()
        return True
    return False