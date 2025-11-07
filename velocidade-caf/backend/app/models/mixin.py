from __future__ import annotations
from datetime import datetime, timezone
from sqlalchemy.orm import declarative_mixin, Mapped, mapped_column
from sqlalchemy import DateTime, func
from sqlalchemy.orm import Session
from sqlalchemy import event

@declarative_mixin
class TimestampMixin:
    # Sempre presente e não-nulo; valor padrão no servidor (Cockroach)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="Data de criação (preenchida no DB)"
    )
    # Atualizado pelo app via listener; começa como now() no servidor
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="Última atualização (preenchida pelo app)"
    )

# Listener global: antes de flush, toca o updated_at
@event.listens_for(Session, "before_flush")
def touch_updated_at(session: Session, flush_context, instances):
    now = datetime.now(timezone.utc)
    # Para objetos criados/alterados no flush atual:
    for obj in set(session.new).union(session.dirty):
        if hasattr(obj, "updated_at"):
            setattr(obj, "updated_at", now)
