from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.user import AthleteProfile  # MUDANÇA AQUI
from app.schemas import AthleteProfileCreate, AthleteProfileUpdate


def get_athlete_by_id(db: Session, athlete_id: str) -> Optional[AthleteProfile]:
    """Busca atleta por ID."""
    return db.query(AthleteProfile).filter(AthleteProfile.id == athlete_id).first()


def get_athlete_by_user_id(db: Session, user_id: str) -> Optional[AthleteProfile]:
    """Busca atleta por user_id."""
    return db.query(AthleteProfile).filter(AthleteProfile.user_id == user_id).first()


def get_athletes(db: Session, skip: int = 0, limit: int = 100) -> List[AthleteProfile]:
    """Lista todos os atletas."""
    return db.query(AthleteProfile).offset(skip).limit(limit).all()


def get_athletes_by_coach(db: Session, coach_id: str, skip: int = 0, limit: int = 100) -> List[AthleteProfile]:
    """Lista atletas de um treinador específico."""
    return db.query(AthleteProfile).filter(
        AthleteProfile.coach_id == coach_id
    ).offset(skip).limit(limit).all()


def create_athlete(db: Session, athlete_in: AthleteProfileCreate) -> AthleteProfile:
    """Cria novo perfil de atleta."""
    athlete = AthleteProfile(**athlete_in.model_dump())
    db.add(athlete)
    db.commit()
    db.refresh(athlete)
    return athlete


def update_athlete(db: Session, athlete: AthleteProfile, athlete_in: AthleteProfileUpdate) -> AthleteProfile:
    """Atualiza perfil de atleta."""
    update_data = athlete_in.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(athlete, field, value)
    
    db.add(athlete)
    db.commit()
    db.refresh(athlete)
    return athlete


def delete_athlete(db: Session, athlete_id: str) -> bool:
    """Deleta perfil de atleta."""
    athlete = get_athlete_by_id(db, athlete_id)
    if athlete:
        db.delete(athlete)
        db.commit()
        return True
    return False