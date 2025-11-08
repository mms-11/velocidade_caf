from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserBase(BaseModel):
    """Schema base do usuário."""
    email: EmailStr
    role: str = Field(..., pattern="^(atleta|treinador)$", description="Papel: 'atleta' ou 'treinador'")


class UserCreate(UserBase):
    """Schema para criação de usuário."""
    password: str = Field(..., min_length=8, description="Senha (mínimo 8 caracteres)")
    google_id: Optional[str] = None


class UserLogin(BaseModel):
    """Schema para login."""
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    """Schema para atualização de usuário."""
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8)
    is_active: Optional[bool] = None
    google_id: Optional[str] = None


class UserResponse(UserBase):
    """Schema de resposta do usuário."""
    id: str
    google_id: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_login: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    """Schema para token JWT."""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse  # Inclui dados do usuário no response


class TokenData(BaseModel):
    """Schema para dados extraídos do token."""
    user_id: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None