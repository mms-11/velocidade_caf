from typing import List, Optional
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import and_, extract

from app.models.mark import Mark  # JÁ ESTÁ CORRETO
from app.schemas import MarkCreate, MarkUpdate


def get_mark_by_id(db: Session, mark_id: str) -> Optional[Mark]:
    """Busca marca por ID."""
    return db.query(Mark).filter(Mark.id == mark_id).first()


def get_marks_by_athlete(
    db: Session,
    athlete_id: str,
    skip: int = 0,
    limit: int = 100
) -> List[Mark]:
    """Lista todas as marcas de um atleta."""
    return db.query(Mark).filter(
        Mark.athlete_id == athlete_id
    ).order_by(Mark.data.desc()).offset(skip).limit(limit).all()


def get_marks_by_event(
    db: Session,
    athlete_id: str,
    evento: str
) -> List[Mark]:
    """Busca marcas de um atleta em um evento específico."""
    return db.query(Mark).filter(
        and_(
            Mark.athlete_id == athlete_id,
            Mark.evento == evento
        )
    ).order_by(Mark.data.desc()).all()


def get_marks_by_date_range(
    db: Session,
    athlete_id: str,
    start_date: date,
    end_date: date
) -> List[Mark]:
    """Busca marcas de um atleta em um período."""
    return db.query(Mark).filter(
        and_(
            Mark.athlete_id == athlete_id,
            Mark.data >= start_date,
            Mark.data <= end_date
        )
    ).order_by(Mark.data.desc()).all()


def get_marks_by_type(
    db: Session,
    athlete_id: str,
    tipo: str
) -> List[Mark]:
    """Busca marcas por tipo (competicao ou teste)."""
    return db.query(Mark).filter(
        and_(
            Mark.athlete_id == athlete_id,
            Mark.tipo == tipo
        )
    ).order_by(Mark.data.desc()).all()


def get_best_mark_by_event(
    db: Session,
    athlete_id: str,
    evento: str
) -> Optional[Mark]:
    """Retorna a melhor marca de um atleta em um evento."""
    return db.query(Mark).filter(
        and_(
            Mark.athlete_id == athlete_id,
            Mark.evento == evento
        )
    ).order_by(Mark.resultado.asc()).first()  # Menor tempo = melhor


def create_mark(db: Session, mark_in: MarkCreate) -> Mark:
    """Cria novo registro de marca."""
    mark = Mark(**mark_in.model_dump())
    db.add(mark)
    db.commit()
    db.refresh(mark)
    return mark


def update_mark(db: Session, mark: Mark, mark_in: MarkUpdate) -> Mark:
    """Atualiza registro de marca."""
    update_data = mark_in.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(mark, field, value)
    
    db.add(mark)
    db.commit()
    db.refresh(mark)
    return mark


def delete_mark(db: Session, mark_id: str) -> bool:
    """Deleta registro de marca."""
    mark = get_mark_by_id(db, mark_id)
    if mark:
        db.delete(mark)
        db.commit()
        return True
    return False


def get_mark_statistics(db: Session, athlete_id: str) -> dict:
    """Retorna estatísticas das marcas de um atleta."""
    marks = db.query(Mark).filter(Mark.athlete_id == athlete_id).all()
    
    if not marks:
        return {
            "total_registros": 0,
            "eventos_praticados": [],
            "melhores_marcas": {},
            "ultima_competicao": None
        }
    
    eventos = list(set([m.evento for m in marks]))
    
    melhores = {}
    for evento in eventos:
        melhor = get_best_mark_by_event(db, athlete_id, evento)
        if melhor:
            melhores[evento] = {
                "resultado": melhor.resultado,
                "data": melhor.data,
                "local": melhor.local
            }
    
    competicoes = [m for m in marks if m.tipo == "competicao"]
    ultima_competicao = max(competicoes, key=lambda x: x.data).data if competicoes else None
    
    return {
        "total_registros": len(marks),
        "eventos_praticados": eventos,
        "melhores_marcas": melhores,
        "ultima_competicao": ultima_competicao
    }


def get_personal_records(db: Session, athlete_id: str) -> List[dict]:
    """Retorna os recordes pessoais de um atleta por evento."""
    marks = db.query(Mark).filter(Mark.athlete_id == athlete_id).all()
    
    if not marks:
        return []
    
    eventos = list(set([m.evento for m in marks]))
    recordes = []
    
    for evento in eventos:
        melhor = get_best_mark_by_event(db, athlete_id, evento)
        if melhor:
            recordes.append({
                "evento": evento,
                "resultado": melhor.resultado,
                "data": melhor.data,
                "local": melhor.local,
                "vento": melhor.vento,
                "tipo": melhor.tipo
            })
    
    return recordes