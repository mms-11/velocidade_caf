from __future__ import annotations
import uuid
from typing import Optional

import sqlalchemy as sa
from sqlalchemy import String, Text, Float, Integer, Date, DateTime, CheckConstraint, UniqueConstraint, Index, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Mark(Base):
    """
    Marcas de competição e testes.
    Registra tempos, vento, data, local e tipo ('competicao' ou 'teste').
    """
    __tablename__ = "marks"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
        default=lambda: str(uuid.uuid4()),
        comment="ID único da marca"
    )

    athlete_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="ID do atleta"
    )

    # Dados da prova
    evento: Mapped[str] = mapped_column(String(100), nullable=False, comment="Evento (100m, 200m, 400m, etc.)")
    resultado: Mapped[float] = mapped_column(Float, nullable=False, comment="Tempo em segundos")
    vento: Mapped[Optional[float]] = mapped_column(Float, nullable=True, comment="Vento em m/s")
    data: Mapped[sa.Date] = mapped_column(Date, nullable=False, index=True, comment="Data da prova")
    local: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment="Local da prova")
    tipo: Mapped[str] = mapped_column(String(50), nullable=False, comment="Tipo: 'competicao' ou 'teste'")

    # Metadados
    observacoes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[sa.DateTime] = mapped_column(DateTime(timezone=True), server_default=sa.func.now(), nullable=False)
    updated_at: Mapped[Optional[sa.DateTime]] = mapped_column(DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now())

    # Relationship com User (User.marks)
    athlete: Mapped["User"] = relationship(
        "User",
        back_populates="marks",
        foreign_keys=[athlete_id],
    )

    __table_args__ = (
        # Índices úteis
        Index("idx_marks_athlete_date", "athlete_id", "data"),
        Index("idx_marks_athlete_evento", "athlete_id", "evento"),
        Index("idx_marks_evento", "evento"),
        Index("idx_marks_tipo", "tipo"),
        # Validações
        CheckConstraint("resultado > 0", name="check_resultado_positive"),
        CheckConstraint("vento IS NULL OR (vento >= -5 AND vento <= 5)", name="check_vento_range"),
        CheckConstraint("tipo IN ('competicao','teste')", name="check_tipo_valid"),
    )

    # Propriedades derivadas
    @property
    def is_valid_wind(self) -> bool:
        # até 2.0 m/s é válido em provas oficiais
        if self.vento is None:
            return True
        return self.vento <= 2.0

    @property
    def wind_status(self) -> str:
        if self.vento is None:
            return "nao_informado"
        return "valido" if self.is_valid_wind else "invalido"

    @property
    def pace_per_100m(self) -> float:
        # extrai número do evento (ex.: "200m" -> 200)
        try:
            distance = int("".join(filter(str.isdigit, self.evento)))
            if distance > 0:
                return round((self.resultado / distance) * 100, 2)
        except (ValueError, ZeroDivisionError):
            pass
        return self.resultado

    @property
    def is_personal_best(self) -> bool:
        # placeholder — calcular por query no repositório/serviço
        return False

    def __repr__(self) -> str:
        vento_str = f", vento={self.vento}" if self.vento is not None else ""
        return f"<Mark id={self.id} evento={self.evento} resultado={self.resultado}s{vento_str} tipo={self.tipo}>"
