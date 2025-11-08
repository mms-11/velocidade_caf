from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user, get_current_active_coach
from app.schemas import (
    CoachProfileCreate,
    CoachProfileUpdate,
    CoachProfileResponse,
    AthleteProfileResponse
)
from app.crud import coach as crud_coach, athlete as crud_athlete
from app.models.user import User

router = APIRouter()


@router.post("/", response_model=CoachProfileResponse, status_code=status.HTTP_201_CREATED)
def create_coach_profile(
    coach_in: CoachProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_coach)
):
    """Cria perfil de treinador."""
    # Verifica se já existe perfil
    existing = crud_coach.get_coach_by_user_id(db, current_user.id)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Perfil de treinador já existe"
        )
    
    # Força o user_id do usuário autenticado
    coach_in.user_id = current_user.id
    
    coach = crud_coach.create_coach(db, coach_in)
    return coach


@router.get("/me", response_model=CoachProfileResponse)
def get_my_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_coach)
):
    """Retorna perfil do treinador autenticado."""
    coach = crud_coach.get_coach_by_user_id(db, current_user.id)
    if not coach:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil de treinador não encontrado"
        )
    return coach


@router.put("/me", response_model=CoachProfileResponse)
def update_my_profile(
    coach_in: CoachProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_coach)
):
    """Atualiza perfil do treinador autenticado."""
    coach = crud_coach.get_coach_by_user_id(db, current_user.id)
    if not coach:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil de treinador não encontrado"
        )
    
    coach = crud_coach.update_coach(db, coach, coach_in)
    return coach


@router.get("/me/athletes", response_model=List[AthleteProfileResponse])
def get_my_athletes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_coach)
):
    """Lista atletas do treinador autenticado."""
    coach = crud_coach.get_coach_by_user_id(db, current_user.id)
    if not coach:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil de treinador não encontrado"
        )
    
    athletes = crud_athlete.get_athletes_by_coach(db, coach.id, skip=skip, limit=limit)
    return athletes


@router.get("/{coach_id}", response_model=CoachProfileResponse)
def get_coach(
    coach_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Busca treinador por ID."""
    coach = crud_coach.get_coach_by_id(db, coach_id)
    if not coach:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Treinador não encontrado"
        )
    return coach


@router.get("/", response_model=List[CoachProfileResponse])
def list_coaches(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lista todos os treinadores."""
    coaches = crud_coach.get_coaches(db, skip=skip, limit=limit)
    return coaches