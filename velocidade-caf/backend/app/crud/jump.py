from typing import List, Optional
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import and_, extract

from app.models.jump import Jump  # JÁ ESTÁ CORRETO
from app.schemas import JumpCreate, JumpUpdate


def get_jump_by_id(db: Session, jump_id: str) -> Optional[Jump]:
    """Busca salto por ID."""
    return db.query(Jump).filter(Jump.id == jump_id).first()


def get_jumps_by_athlete(
    db: Session,
    athlete_id: str,
    skip: int = 0,
    limit: int = 100
) -> List[Jump]:
    """Lista todos os saltos de um atleta."""
    return db.query(Jump).filter(
        Jump.athlete_id == athlete_id
    ).order_by(Jump.date.desc()).offset(skip).limit(limit).all()


def get_jumps_by_date_range(
    db: Session,
    athlete_id: str,
    start_date: date,
    end_date: date
) -> List[Jump]:
    """Busca saltos de um atleta em um período."""
    return db.query(Jump).filter(
        and_(
            Jump.athlete_id == athlete_id,
            Jump.date >= start_date,
            Jump.date <= end_date
        )
    ).order_by(Jump.date.desc()).all()


def get_jumps_by_month(
    db: Session,
    athlete_id: str,
    year: int,
    month: int
) -> List[Jump]:
    """Busca saltos de um atleta em um mês específico."""
    return db.query(Jump).filter(
        and_(
            Jump.athlete_id == athlete_id,
            extract('year', Jump.date) == year,
            extract('month', Jump.date) == month
        )
    ).order_by(Jump.date.desc()).all()


def get_best_jump(db: Session, athlete_id: str) -> Optional[Jump]:
    """Retorna o melhor salto de um atleta."""
    jumps = db.query(Jump).filter(Jump.athlete_id == athlete_id).all()
    if not jumps:
        return None
    # Usa a propriedade max_jump
    return max(jumps, key=lambda j: j.max_jump)


def create_jump(db: Session, jump_in: JumpCreate) -> Jump:
    """Cria novo registro de salto."""
    jump = Jump(**jump_in.model_dump())
    db.add(jump)
    db.commit()
    db.refresh(jump)
    return jump


def update_jump(db: Session, jump: Jump, jump_in: JumpUpdate) -> Jump:
    """Atualiza registro de salto."""
    update_data = jump_in.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(jump, field, value)
    
    db.add(jump)
    db.commit()
    db.refresh(jump)
    return jump


def delete_jump(db: Session, jump_id: str) -> bool:
    """Deleta registro de salto."""
    jump = get_jump_by_id(db, jump_id)
    if jump:
        db.delete(jump)
        db.commit()
        return True
    return False


def get_jump_statistics(db: Session, athlete_id: str) -> dict:
    """Retorna estatísticas dos saltos de um atleta."""
    jumps = db.query(Jump).filter(Jump.athlete_id == athlete_id).all()
    
    if not jumps:
        return {
            "total_registros": 0,
            "melhor_salto": None,
            "media_geral": None,
            "ultimo_registro": None
        }
    
    max_jumps = [j.max_jump for j in jumps]
    averages = [j.average for j in jumps]
    
    return {
        "total_registros": len(jumps),
        "melhor_salto": max(max_jumps),
        "media_geral": round(sum(averages) / len(averages), 2),
        "ultimo_registro": max(jumps, key=lambda x: x.date).date
    }