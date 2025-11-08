"""
Schemas Pydantic para validação e serialização de dados.
"""
from app.schemas.user import (
    UserBase,
    UserCreate,
    UserUpdate,
    UserResponse,
    UserLogin,
    Token,
)
from app.schemas.athlete import (
    AthleteProfileBase,
    AthleteProfileCreate,
    AthleteProfileUpdate,
    AthleteProfileResponse,
)
from app.schemas.coach import (
    CoachProfileBase,
    CoachProfileCreate,
    CoachProfileUpdate,
    CoachProfileResponse,
)
from app.schemas.jump import (
    JumpBase,
    JumpCreate,
    JumpUpdate,
    JumpResponse,
)
from app.schemas.mark import (
    MarkBase,
    MarkCreate,
    MarkUpdate,
    MarkResponse,
)

__all__ = [
    # User
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserLogin",
    "Token",
    # Athlete
    "AthleteProfileBase",
    "AthleteProfileCreate",
    "AthleteProfileUpdate",
    "AthleteProfileResponse",
    # Coach
    "CoachProfileBase",
    "CoachProfileCreate",
    "CoachProfileUpdate",
    "CoachProfileResponse",
    # Jump
    "JumpBase",
    "JumpCreate",
    "JumpUpdate",
    "JumpResponse",
    # Mark
    "MarkBase",
    "MarkCreate",
    "MarkUpdate",
    "MarkResponse",
]