from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class MarkBase(BaseModel):
    """Schema base de marca."""
    evento: str = Field(..., max_length=100, description="Evento (100m, 200m, 400m, etc.)")
    resultado: float = Field(..., gt=0, description="Tempo em segundos")
    vento: Optional[float] = Field(None, description="Vento em m/s")
    data: date
    local: Optional[str] = Field(None, max_length=255)
    tipo: str = Field(..., pattern="^(competicao|teste)$", description="Tipo: 'competicao' ou 'teste'")
    observacoes: Optional[str] = None


class MarkCreate(MarkBase):
    """Schema para criação de marca."""
    athlete_id: str


class MarkUpdate(BaseModel):
    """Schema para atualização de marca."""
    evento: Optional[str] = Field(None, max_length=100)
    resultado: Optional[float] = Field(None, gt=0)
    vento: Optional[float] = None
    data: Optional[date] = None
    local: Optional[str] = Field(None, max_length=255)
    tipo: Optional[str] = Field(None, pattern="^(competicao|teste)$")
    observacoes: Optional[str] = None


class MarkResponse(MarkBase):
    """Schema de resposta de marca."""
    id: str
    athlete_id: str

    model_config = ConfigDict(from_attributes=True)