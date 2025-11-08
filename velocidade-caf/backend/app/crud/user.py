from typing import Optional
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.models.user import User
from app.schemas import UserCreate, UserUpdate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """Gera hash da senha."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica senha."""
    return pwd_context.verify(plain_password, hashed_password)


def get_user_by_id(db: Session, user_id: str) -> Optional[User]:
    """Busca usuário por ID."""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Busca usuário por email."""
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user_in: UserCreate) -> User:
    """Cria novo usuário."""
    user = User(
        email=user_in.email,
        password_hash=get_password_hash(user_in.password),
        role=user_in.role,
        google_id=user_in.google_id,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, user: User, user_in: UserUpdate) -> User:
    """Atualiza usuário."""
    update_data = user_in.model_dump(exclude_unset=True)
    
    if "password" in update_data:
        update_data["password_hash"] = get_password_hash(update_data.pop("password"))
    
    for field, value in update_data.items():
        setattr(user, field, value)
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """Autentica usuário."""
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not user.password_hash or not verify_password(password, user.password_hash):
        return None
    return user