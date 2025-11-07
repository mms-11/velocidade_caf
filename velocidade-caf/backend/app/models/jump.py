from __future__ import annotations
import uuid
from typing import Optional

import sqlalchemy as sa
from sqlalchemy import String, Text, Float, Integer, Date, DateTime, CheckConstraint, UniqueConstraint, Index, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Jump(Base):
    """
    Registro de saltos verticais do atleta.
    Regra: um registro por atleta por dia.
    """
    __tablename__ = "jumps"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
        default=lambda: str(uuid.uuid4()),
        comment="ID único do registro"
    )

    athlete_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="ID do atleta"
    )

    # Data e medidas
    date: Mapped[sa.Date] = mapped_column(Date, nullable=False, index=True, comment="Data do treino")
    jump1: Mapped[float] = mapped_column(Float, nullable=False, comment="Primeiro salto (cm)")
    jump2: Mapped[float] = mapped_column(Float, nullable=False, comment="Segundo salto (cm)")
    jump3: Mapped[float] = mapped_column(Float, nullable=False, comment="Terceiro salto (cm)")

    # Observações
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="Observações do treino")

    # Timestamps
    #created_at: Mapped[sa.DateTime] = mapped_column(DateTime(timezone=True), server_default=sa.func.now(), nullable=False)
    #updated_at: Mapped[Optional[sa.DateTime]] = mapped_column(DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now())

    # Relationship com User (User.jumps)
    athlete: Mapped["User"] = relationship(
        "User",
        back_populates="jumps",
        foreign_keys=[athlete_id],
    )

    __table_args__ = (
        # um atleta só pode ter um registro por dia
        UniqueConstraint("athlete_id", "date", name="unique_athlete_date"),
        # índice composto comum
        Index("idx_jumps_athlete_date", "athlete_id", "date"),
        # validações
        CheckConstraint("jump1 > 0", name="check_jump1_positive"),
        CheckConstraint("jump2 > 0", name="check_jump2_positive"),
        CheckConstraint("jump3 > 0", name="check_jump3_positive"),
        CheckConstraint("jump1 <= 200", name="check_jump1_max"),
        CheckConstraint("jump2 <= 200", name="check_jump2_max"),
        CheckConstraint("jump3 <= 200", name="check_jump3_max"),
    )

    # Propriedades calculadas (não persistidas)
    @property
    def average(self) -> float:
        return round((self.jump1 + self.jump2 + self.jump3) / 3, 2)

    @property
    def max_jump(self) -> float:
        return max(self.jump1, self.jump2, self.jump3)

    @property
    def min_jump(self) -> float:
        return min(self.jump1, self.jump2, self.jump3)

    @property
    def consistency(self) -> float:
        avg = self.average
        if avg == 0:
            return 0.0
        std_dev = (((self.jump1 - avg) ** 2 + (self.jump2 - avg) ** 2 + (self.jump3 - avg) ** 2) / 3) ** 0.5
        cv = (std_dev / avg) * 100  # %
        return round(max(0, min(100, 100 - cv)), 2)

    def __repr__(self) -> str:
        return f"<Jump id={self.id} date={self.date} avg={self.average:.1f}cm max={self.max_jump:.1f}cm>"
