from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class CoachProfileBase(BaseModel):
    """Schema base do perfil do treinador."""
    nome: Optional[str] = Field(None, max_length=255)
    especialidade: Optional[str] = Field(None, max_length=255)
    telefone: Optional[str] = Field(None, max_length=20)
    bio: Optional[str] = None
    certificacoes: Optional[str] = None
    anos_experiencia: Optional[int] = Field(None, ge=0)


class CoachProfileCreate(CoachProfileBase):
    """Schema para criação de perfil de treinador."""
    user_id: str


class CoachProfileUpdate(CoachProfileBase):
    """Schema para atualização de perfil de treinador."""
    pass


class CoachProfileResponse(CoachProfileBase):
    """Schema de resposta do perfil de treinador."""
    id: str
    user_id: str

    model_config = ConfigDict(from_attributes=True)