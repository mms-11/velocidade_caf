from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user, get_current_active_athlete
from app.schemas import (
    AthleteProfileCreate,
    AthleteProfileUpdate,
    AthleteProfileResponse
)
from app.crud import athlete as crud_athlete
from app.models.user import User

router = APIRouter()


@router.post("/", response_model=AthleteProfileResponse, status_code=status.HTTP_201_CREATED)
def create_athlete_profile(
    athlete_in: AthleteProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_athlete)
):
    """Cria perfil de atleta (apenas atletas podem criar seu próprio perfil)."""
    # Verifica se já existe perfil
    existing = crud_athlete.get_athlete_by_user_id(db, current_user.id)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Perfil de atleta já existe"
        )
    
    # Força o user_id do usuário autenticado
    athlete_in.user_id = current_user.id
    
    athlete = crud_athlete.create_athlete(db, athlete_in)
    return athlete


@router.get("/me", response_model=AthleteProfileResponse)
def get_my_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_athlete)
):
    """Retorna perfil do atleta autenticado."""
    athlete = crud_athlete.get_athlete_by_user_id(db, current_user.id)
    if not athlete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil de atleta não encontrado"
        )
    return athlete


@router.put("/me", response_model=AthleteProfileResponse)
def update_my_profile(
    athlete_in: AthleteProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_athlete)
):
    """Atualiza perfil do atleta autenticado."""
    athlete = crud_athlete.get_athlete_by_user_id(db, current_user.id)
    if not athlete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil de atleta não encontrado"
        )
    
    athlete = crud_athlete.update_athlete(db, athlete, athlete_in)
    return athlete


@router.get("/{athlete_id}", response_model=AthleteProfileResponse)
def get_athlete(
    athlete_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Busca atleta por ID (treinadores podem ver qualquer atleta)."""
    athlete = crud_athlete.get_athlete_by_id(db, athlete_id)
    if not athlete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Atleta não encontrado"
        )
    
    # Apenas treinador ou o próprio atleta podem ver
    if current_user.role != "treinador" and athlete.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para visualizar este atleta"
        )
    
    return athlete


@router.get("/", response_model=List[AthleteProfileResponse])
def list_athletes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lista atletas (apenas treinadores)."""
    if current_user.role != "treinador":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas treinadores podem listar atletas"
        )
    
    athletes = crud_athlete.get_athletes(db, skip=skip, limit=limit)
    return athletes