"""
Funções de segurança e autenticação JWT.
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.config import settings

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/users/login")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Cria um token JWT.
    
    Args:
        data: Dados a serem codificados no token
        expires_delta: Tempo de expiração customizado
    
    Returns:
        Token JWT codificado
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    return encoded_jwt


def verify_token(token: str) -> dict:
    """
    Verifica e decodifica um token JWT.
    
    Args:
        token: Token JWT
    
    Returns:
        Dados decodificados do token
    
    Raises:
        HTTPException: Se o token for inválido
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )