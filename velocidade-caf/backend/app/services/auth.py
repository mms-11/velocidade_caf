from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.core.config import get_db
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta

class AuthService:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.secret_key = "your_secret_key"  # Replace with your actual secret key
        self.algorithm = "HS256"
        self.access_token_expires_minutes = 30

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def create_access_token(self, data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expires_minutes)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def register_user(self, user: UserCreate, db: Session):
        hashed_password = self.get_password_hash(user.password)
        db_user = User(**user.dict(), password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def authenticate_user(self, username: str, password: str, db: Session):
        user = db.query(User).filter(User.username == username).first()
        if not user or not self.verify_password(password, user.password):
            raise HTTPException(status_code=400, detail="Incorrect username or password")
        return user

def get_auth_service():
    return AuthService()