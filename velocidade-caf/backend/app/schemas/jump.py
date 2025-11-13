from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class JumpBase(BaseModel):
    """Schema base de salto."""
    date: date
    jump1: float = Field(..., gt=0, le=200, description="Primeiro salto em cm")
    jump2: float = Field(..., gt=0, le=200, description="Segundo salto em cm")
    jump3: float = Field(..., gt=0, le=200, description="Terceiro salto em cm")
    notes: Optional[str] = Field(None, alias="observacoes")
    
    model_config = ConfigDict(populate_by_name=True)


class JumpCreate(JumpBase):
    """Schema para criação de registro de salto."""
    athlete_id: Optional[str] = None  # Opcional, será preenchido automaticamente pelo backend


class JumpUpdate(BaseModel):
    """Schema para atualização de salto."""
    jump1: Optional[float] = Field(None, gt=0, le=200)
    jump2: Optional[float] = Field(None, gt=0, le=200)
    jump3: Optional[float] = Field(None, gt=0, le=200)
    notes: Optional[str] = Field(None, alias="observacoes")
    
    model_config = ConfigDict(populate_by_name=True)


class JumpResponse(JumpBase):
    """Schema de resposta de salto."""
    id: str
    athlete_id: str
    melhor_salto: Optional[float] = Field(None, alias="max_jump")
    media: Optional[float] = Field(None, alias="average")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)