from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.schemas import UserCreate, UserResponse, UserLogin, Token
from app.crud import user as crud_user
from app.core.security import create_access_token
from app.models.user import User

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    """Registra novo usuário."""
    # Verifica se email já existe
    existing_user = crud_user.get_user_by_email(db, email=user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado"
        )
    
    user = crud_user.create_user(db, user_in)
    return user


@router.post("/login", response_model=Token)
def login(user_in: UserLogin, db: Session = Depends(get_db)):
    """Login de usuário - retorna JWT token."""
    user = crud_user.authenticate_user(db, user_in.email, user_in.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário inativo"
        )
    
    # Atualiza last_login
    user.last_login = datetime.utcnow()
    db.add(user)
    db.commit()
    
    # Cria token JWT
    access_token = create_access_token(
        data={"sub": user.id, "email": user.email, "role": user.role}
    )
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        user=user
    )


@router.post("/token")
def login_oauth2(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    Login OAuth2 para Swagger UI.
    Use seu email como username.
    """
    user = crud_user.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário inativo"
        )
    
    # Atualiza last_login
    user.last_login = datetime.utcnow()
    db.add(user)
    db.commit()
    
    # Cria token JWT
    access_token = create_access_token(
        data={"sub": user.id, "email": user.email, "role": user.role}
    )
    
    # OAuth2 só retorna access_token e token_type
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Retorna informações do usuário autenticado."""
    return current_user


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Busca usuário por ID."""
    if current_user.role != "treinador" and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para visualizar este usuário"
        )
    
    user = crud_user.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    return user