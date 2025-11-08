from typing import List
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user, get_current_active_athlete
from app.schemas import MarkCreate, MarkUpdate, MarkResponse
from app.crud import mark as crud_mark, athlete as crud_athlete
from app.models.user import User

router = APIRouter()


@router.post("/", response_model=MarkResponse, status_code=status.HTTP_201_CREATED)
def create_mark(
    mark_in: MarkCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_athlete)
):
    """Cria registro de marca."""
    athlete = crud_athlete.get_athlete_by_user_id(db, current_user.id)
    if not athlete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil de atleta não encontrado"
        )
    
    # Força o athlete_id do usuário autenticado
    mark_in.athlete_id = athlete.id
    
    mark = crud_mark.create_mark(db, mark_in)
    return mark


@router.get("/me", response_model=List[MarkResponse])
def get_my_marks(
    skip: int = 0,
    limit: int = 100,
    evento: str = Query(None, description="Filtrar por evento"),
    tipo: str = Query(None, pattern="^(competicao|teste)$", description="Filtrar por tipo"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_athlete)
):
    """Lista marcas do atleta autenticado."""
    athlete = crud_athlete.get_athlete_by_user_id(db, current_user.id)
    if not athlete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil de atleta não encontrado"
        )
    
    if evento:
        marks = crud_mark.get_marks_by_event(db, athlete.id, evento)
    elif tipo:
        marks = crud_mark.get_marks_by_type(db, athlete.id, tipo)
    else:
        marks = crud_mark.get_marks_by_athlete(db, athlete.id, skip=skip, limit=limit)
    
    return marks


@router.get("/me/statistics")
def get_my_mark_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_athlete)
):
    """Retorna estatísticas das marcas do atleta autenticado."""
    athlete = crud_athlete.get_athlete_by_user_id(db, current_user.id)
    if not athlete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil de atleta não encontrado"
        )
    
    stats = crud_mark.get_mark_statistics(db, athlete.id)
    return stats


@router.get("/me/records")
def get_my_personal_records(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_athlete)
):
    """Retorna recordes pessoais do atleta autenticado."""
    athlete = crud_athlete.get_athlete_by_user_id(db, current_user.id)
    if not athlete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil de atleta não encontrado"
        )
    
    records = crud_mark.get_personal_records(db, athlete.id)
    return records


@router.get("/athlete/{athlete_id}", response_model=List[MarkResponse])
def get_athlete_marks(
    athlete_id: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lista marcas de um atleta (treinadores podem ver qualquer atleta)."""
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
            detail="Sem permissão para visualizar marcas deste atleta"
        )
    
    marks = crud_mark.get_marks_by_athlete(db, athlete_id, skip=skip, limit=limit)
    return marks


@router.get("/{mark_id}", response_model=MarkResponse)
def get_mark(
    mark_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Busca marca por ID."""
    mark = crud_mark.get_mark_by_id(db, mark_id)
    if not mark:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Marca não encontrada"
        )
    
    # Verifica permissão
    athlete = crud_athlete.get_athlete_by_id(db, mark.athlete_id)
    if current_user.role != "treinador" and athlete.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para visualizar esta marca"
        )
    
    return mark


@router.put("/{mark_id}", response_model=MarkResponse)
def update_mark(
    mark_id: str,
    mark_in: MarkUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_athlete)
):
    """Atualiza registro de marca."""
    mark = crud_mark.get_mark_by_id(db, mark_id)
    if not mark:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Marca não encontrada"
        )
    
    # Verifica se a marca pertence ao atleta
    athlete = crud_athlete.get_athlete_by_user_id(db, current_user.id)
    if not athlete or mark.athlete_id != athlete.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para editar esta marca"
        )
    
    mark = crud_mark.update_mark(db, mark, mark_in)
    return mark


@router.delete("/{mark_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_mark(
    mark_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_athlete)
):
    """Deleta registro de marca."""
    mark = crud_mark.get_mark_by_id(db, mark_id)
    if not mark:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Marca não encontrada"
        )
    
    # Verifica se a marca pertence ao atleta
    athlete = crud_athlete.get_athlete_by_user_id(db, current_user.id)
    if not athlete or mark.athlete_id != athlete.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para deletar esta marca"
        )
    
    crud_mark.delete_mark(db, mark_id)
    return None