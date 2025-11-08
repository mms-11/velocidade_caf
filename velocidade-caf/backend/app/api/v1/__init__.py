"""
API v1 endpoints.
"""

from fastapi import APIRouter

from app.api.v1 import users, athletes, coaches, jumps, marks

api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(athletes.router, prefix="/athletes", tags=["athletes"])
api_router.include_router(coaches.router, prefix="/coaches", tags=["coaches"])
api_router.include_router(jumps.router, prefix="/jumps", tags=["jumps"])
api_router.include_router(marks.router, prefix="/marks", tags=["marks"])