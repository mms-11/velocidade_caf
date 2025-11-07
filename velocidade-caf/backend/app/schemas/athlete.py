from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class AthleteProfileBase(BaseModel):
    """Schema base do perfil do atleta."""
    nome: Optional[str] = Field(None, max_length=255)
    data_nascimento: Optional[date] = None
    altura_cm: Optional[int] = Field(None, ge=100, le=250, description="Altura em cm (100-250)")
    peso_kg: Optional[float] = Field(None, ge=30, le=200, description="Peso em kg (30-200)")
    tamanho_pe: Optional[int] = Field(None, ge=20, le=60)
    endereco: Optional[str] = None
    telefone: Optional[str] = Field(None, max_length=20)
    prova_principal: Optional[str] = Field(None, max_length=100)
    prova_secundaria: Optional[str] = Field(None, max_length=100)
    tempo_experiencia: Optional[str] = Field(None, max_length=50)
    categoria: Optional[str] = Field(None, max_length=50)


class AthleteProfileCreate(AthleteProfileBase):
    """Schema para criação de perfil de atleta."""
    user_id: str
    coach_id: Optional[str] = None
    tipo_sanguineo: Optional[str] = Field(None, max_length=5)
    alergias: Optional[str] = None
    medicamentos: Optional[str] = None
    contato_emergencia: Optional[str] = Field(None, max_length=255)


class AthleteProfileUpdate(BaseModel):
    """Schema para atualização de perfil de atleta."""
    coach_id: Optional[str] = None
    nome: Optional[str] = Field(None, max_length=255)
    data_nascimento: Optional[date] = None
    altura_cm: Optional[int] = Field(None, ge=100, le=250)
    peso_kg: Optional[float] = Field(None, ge=30, le=200)
    tamanho_pe: Optional[int] = Field(None, ge=20, le=60)
    endereco: Optional[str] = None
    telefone: Optional[str] = Field(None, max_length=20)
    prova_principal: Optional[str] = Field(None, max_length=100)
    prova_secundaria: Optional[str] = Field(None, max_length=100)
    tempo_experiencia: Optional[str] = Field(None, max_length=50)
    categoria: Optional[str] = Field(None, max_length=50)
    tipo_sanguineo: Optional[str] = Field(None, max_length=5)
    alergias: Optional[str] = None
    medicamentos: Optional[str] = None
    contato_emergencia: Optional[str] = Field(None, max_length=255)


class AthleteProfileResponse(AthleteProfileBase):
    """Schema de resposta do perfil de atleta."""
    id: str
    user_id: str
    coach_id: Optional[str] = None
    tipo_sanguineo: Optional[str] = None
    alergias: Optional[str] = None
    medicamentos: Optional[str] = None
    contato_emergencia: Optional[str] = None
    idade: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)