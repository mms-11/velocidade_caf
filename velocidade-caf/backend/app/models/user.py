from __future__ import annotations
import uuid
from datetime import date
from typing import Optional, List

import sqlalchemy as sa
from sqlalchemy import String, Text, Boolean, Integer, Float, Date, DateTime, CheckConstraint, Index, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
import app.models.user
import app.models.jump 
import app.models.mark

from app.db.session import Base  



# USER MODEL

class User(Base):
    """
    Modelo principal de usuário.
    Pode ser atleta ou treinador (role).
    """
    __tablename__ = "users"

    # CockroachDB tem gen_random_uuid(); se não existir, usamos default no app.
    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
        default=lambda: str(uuid.uuid4()),  # fallback se n tiver UUID
        comment="ID único do usuário"
    )

    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True, comment="Email único")
    password_hash: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment="Hash da senha (ou OAuth)")
    role: Mapped[str] = mapped_column(String(50), nullable=False, comment="Papel: 'atleta' ou 'treinador'")

    # OAuth Google
    google_id: Mapped[Optional[str]] = mapped_column(String(255), unique=True, nullable=True, index=True, comment="ID Google OAuth")

    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=sa.text("true"), comment="Ativo/Inativo")

    # Timestamps (TIMESTAMPTZ)
    created_at: Mapped[date] = mapped_column(DateTime(timezone=True), server_default=sa.func.now(), nullable=False, comment="Criação")
    updated_at: Mapped[Optional[date]] = mapped_column(DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), comment="Última atualização")
    last_login: Mapped[Optional[date]] = mapped_column(DateTime(timezone=True), nullable=True, comment="Último login")

    # Relationships 1–1 com perfis
    athlete_profile: Mapped[Optional["AthleteProfile"]] = relationship(
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
        foreign_keys="AthleteProfile.user_id",
    )

    coach_profile: Mapped[Optional["CoachProfile"]] = relationship(
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
        foreign_keys="CoachProfile.user_id",
    )

    # Exemplos de relacionamentos 1–N (ajuste se tiver modelos Jump/Mark)
    jumps: Mapped[List["Jump"]] = relationship(
        back_populates="athlete",
        cascade="all, delete-orphan",
        foreign_keys="Jump.athlete_id",
        lazy="selectin",
    )

    marks: Mapped[List["Mark"]] = relationship(
        back_populates="athlete",
        cascade="all, delete-orphan",
        foreign_keys="Mark.athlete_id",
        lazy="selectin",
    )

    __table_args__ = (
        Index("idx_user_email", "email"),
        Index("idx_user_role", "role"),
        Index("idx_user_active", "is_active"),
        Index("idx_user_google_id", "google_id"),
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email} role={self.role}>"



# ATHLETE 

class AthleteProfile(Base):
    """Perfil completo do atleta (1–1 com User)."""
    __tablename__ = "athlete_profiles"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
        default=lambda: str(uuid.uuid4()),
    )

    user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
        comment="ID do usuário (único)",
    )

    coach_id: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        comment="ID do treinador responsável",
    )

    # Dados pessoais
    nome: Mapped[Optional[str]] = mapped_column(String(255))
    data_nascimento: Mapped[Optional[date]] = mapped_column(Date)
    altura_cm: Mapped[Optional[int]] = mapped_column(Integer)
    peso_kg: Mapped[Optional[float]] = mapped_column(Float)
    tamanho_pe: Mapped[Optional[int]] = mapped_column(Integer)
    endereco: Mapped[Optional[str]] = mapped_column(Text)
    telefone: Mapped[Optional[str]] = mapped_column(String(20))

    # Dados esportivos
    prova_principal: Mapped[Optional[str]] = mapped_column(String(100))
    prova_secundaria: Mapped[Optional[str]] = mapped_column(String(100))
    tempo_experiencia: Mapped[Optional[str]] = mapped_column(String(50))
    categoria: Mapped[Optional[str]] = mapped_column(String(50))

    # Médicas (opcional)
    tipo_sanguineo: Mapped[Optional[str]] = mapped_column(String(5))
    alergias: Mapped[Optional[str]] = mapped_column(Text)
    medicamentos: Mapped[Optional[str]] = mapped_column(Text)
    contato_emergencia: Mapped[Optional[str]] = mapped_column(String(255))

    # Timestamps
    created_at: Mapped[Optional[date]] = mapped_column(DateTime(timezone=True), server_default=sa.func.now())
    updated_at: Mapped[Optional[date]] = mapped_column(DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now())

    # Relationships
    user: Mapped["User"] = relationship(
        "User",
        back_populates="athlete_profile",
        foreign_keys=[user_id],
    )
    coach: Mapped[Optional["User"]] = relationship(
        "User",
        foreign_keys=[coach_id],
    )

    __table_args__ = (
        Index("idx_athlete_user_id", "user_id"),
        Index("idx_athlete_coach_id", "coach_id"),
        CheckConstraint("altura_cm IS NULL OR (altura_cm >= 100 AND altura_cm <= 250)", name="check_altura"),
        CheckConstraint("peso_kg IS NULL OR (peso_kg >= 30 AND peso_kg <= 200)", name="check_peso"),
    )

    @property
    def idade(self) -> Optional[int]:
        if not self.data_nascimento:
            return None
        today = date.today()
        return today.year - self.data_nascimento.year - (
            (today.month, today.day) < (self.data_nascimento.month, self.data_nascimento.day)
        )

    def __repr__(self) -> str:
        return f"<AthleteProfile nome={self.nome} user_id={self.user_id}>"



# COACH 

class CoachProfile(Base):
    """Perfil do treinador (1–1 com User)."""
    __tablename__ = "coach_profiles"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
        default=lambda: str(uuid.uuid4()),
    )

    user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
        comment="ID do usuário (único)",
    )

 
    nome: Mapped[Optional[str]] = mapped_column(String(255))
    especialidade: Mapped[Optional[str]] = mapped_column(String(255))
    telefone: Mapped[Optional[str]] = mapped_column(String(20))
    bio: Mapped[Optional[str]] = mapped_column(Text)
    certificacoes: Mapped[Optional[str]] = mapped_column(Text)
    anos_experiencia: Mapped[Optional[int]] = mapped_column(Integer)

    # Timestamps
    created_at: Mapped[Optional[date]] = mapped_column(DateTime(timezone=True), server_default=sa.func.now())
    updated_at: Mapped[Optional[date]] = mapped_column(DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now())

    # Relationship 1–1 com User
    user: Mapped["User"] = relationship(
        "User",
        back_populates="coach_profile",
        foreign_keys=[user_id],
    )

    __table_args__ = (
        Index("idx_coach_user_id", "user_id"),
    )

    def __repr__(self) -> str:
        return f"<CoachProfile nome={self.nome} user_id={self.user_id}>"
