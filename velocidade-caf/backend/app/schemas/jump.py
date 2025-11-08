from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class JumpBase(BaseModel):
    """Schema base de salto."""
    date: date
    jump1: float = Field(..., gt=0, description="Primeiro salto em cm")
    jump2: float = Field(..., gt=0, description="Segundo salto em cm")
    jump3: Optional[float] = Field(None, gt=0, description="Terceiro salto em cm")
    observacoes: Optional[str] = None


class JumpCreate(JumpBase):
    """Schema para criação de registro de salto."""
    athlete_id: str


class JumpUpdate(BaseModel):
    """Schema para atualização de salto."""
    jump1: Optional[float] = Field(None, gt=0)
    jump2: Optional[float] = Field(None, gt=0)
    jump3: Optional[float] = Field(None, gt=0)
    observacoes: Optional[str] = None


class JumpResponse(JumpBase):
    """Schema de resposta de salto."""
    id: str
    athlete_id: str
    melhor_salto: Optional[float] = None
    media: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)