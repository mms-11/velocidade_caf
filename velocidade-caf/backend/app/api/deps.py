"""
Dependências para rotas da API.
"""
from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.core.security import oauth2_scheme, verify_token
from app.crud import user as crud_user
from app.models.user import User


def get_db() -> Generator:
    """Dependência para obter sessão do banco."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    """
    Obtém o usuário atual autenticado.
    
    Args:
        db: Sessão do banco
        token: Token JWT do header Authorization
    
    Returns:
        Usuário autenticado
    
    Raises:
        HTTPException: Se o token for inválido ou usuário não existir
    """
    payload = verify_token(token)
    user_id: Optional[str] = payload.get("sub")
    
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = crud_user.get_user_by_id(db, user_id=user_id)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário inativo"
        )
    
    return user


def get_current_active_athlete(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Verifica se o usuário atual é um atleta ativo.
    
    Args:
        current_user: Usuário autenticado
    
    Returns:
        Usuário atleta
    
    Raises:
        HTTPException: Se não for um atleta
    """
    if current_user.role != "atleta":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso permitido apenas para atletas"
        )
    return current_user


def get_current_active_coach(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Verifica se o usuário atual é um treinador ativo.
    
    Args:
        current_user: Usuário autenticado
    
    Returns:
        Usuário treinador
    
    Raises:
        HTTPException: Se não for um treinador
    """
    if current_user.role != "treinador":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso permitido apenas para treinadores"
        )
    return current_user