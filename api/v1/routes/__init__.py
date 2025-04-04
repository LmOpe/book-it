"""API v1 routes module."""

from fastapi import APIRouter

from api.v1.routes.users import auth

api_version_one = APIRouter(prefix="/api/v1")

api_version_one.include_router(auth)
