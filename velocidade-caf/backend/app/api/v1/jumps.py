from typing import List
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user, get_current_active_athlete
from app.schemas import JumpCreate, JumpUpdate, JumpResponse
from app.crud import jump as crud_jump, athlete as crud_athlete
from app.models.user import User

router = APIRouter()


@router.post("/", response_model=JumpResponse, status_code=status.HTTP_201_CREATED)
def create_jump(
    jump_in: JumpCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_athlete)
):
    """Cria registro de salto."""
    # Verifica se o atleta existe e pertence ao usuário
    athlete = crud_athlete.get_athlete_by_user_id(db, current_user.id)
    if not athlete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil de atleta não encontrado"
        )
    
    # Força o athlete_id do usuário autenticado
    jump_in.athlete_id = athlete.id
    
    jump = crud_jump.create_jump(db, jump_in)
    return jump


@router.get("/me", response_model=List[JumpResponse])
def get_my_jumps(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_athlete)
):
    """Lista saltos do atleta autenticado."""
    athlete = crud_athlete.get_athlete_by_user_id(db, current_user.id)
    if not athlete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil de atleta não encontrado"
        )
    
    jumps = crud_jump.get_jumps_by_athlete(db, athlete.id, skip=skip, limit=limit)
    return jumps


@router.get("/me/statistics")
def get_my_jump_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_athlete)
):
    """Retorna estatísticas dos saltos do atleta autenticado."""
    athlete = crud_athlete.get_athlete_by_user_id(db, current_user.id)
    if not athlete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil de atleta não encontrado"
        )
    
    stats = crud_jump.get_jump_statistics(db, athlete.id)
    return stats


@router.get("/me/best", response_model=JumpResponse)
def get_my_best_jump(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_athlete)
):
    """Retorna o melhor salto do atleta autenticado."""
    athlete = crud_athlete.get_athlete_by_user_id(db, current_user.id)
    if not athlete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil de atleta não encontrado"
        )
    
    best_jump = crud_jump.get_best_jump(db, athlete.id)
    if not best_jump:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhum salto encontrado"
        )
    
    return best_jump


@router.get("/athlete/{athlete_id}", response_model=List[JumpResponse])
def get_athlete_jumps(
    athlete_id: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lista saltos de um atleta (treinadores podem ver qualquer atleta)."""
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
            detail="Sem permissão para visualizar saltos deste atleta"
        )
    
    jumps = crud_jump.get_jumps_by_athlete(db, athlete_id, skip=skip, limit=limit)
    return jumps


@router.get("/{jump_id}", response_model=JumpResponse)
def get_jump(
    jump_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Busca salto por ID."""
    jump = crud_jump.get_jump_by_id(db, jump_id)
    if not jump:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Salto não encontrado"
        )
    
    # Verifica permissão
    athlete = crud_athlete.get_athlete_by_id(db, jump.athlete_id)
    if current_user.role != "treinador" and athlete.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para visualizar este salto"
        )
    
    return jump


@router.put("/{jump_id}", response_model=JumpResponse)
def update_jump(
    jump_id: str,
    jump_in: JumpUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_athlete)
):
    """Atualiza registro de salto."""
    jump = crud_jump.get_jump_by_id(db, jump_id)
    if not jump:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Salto não encontrado"
        )
    
    # Verifica se o salto pertence ao atleta
    athlete = crud_athlete.get_athlete_by_user_id(db, current_user.id)
    if not athlete or jump.athlete_id != athlete.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para editar este salto"
        )
    
    jump = crud_jump.update_jump(db, jump, jump_in)
    return jump


@router.delete("/{jump_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_jump(
    jump_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_athlete)
):
    """Deleta registro de salto."""
    jump = crud_jump.get_jump_by_id(db, jump_id)
    if not jump:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Salto não encontrado"
        )
    
    # Verifica se o salto pertence ao atleta
    athlete = crud_athlete.get_athlete_by_user_id(db, current_user.id)
    if not athlete or jump.athlete_id != athlete.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para deletar este salto"
        )
    
    crud_jump.delete_jump(db, jump_id)
    return None