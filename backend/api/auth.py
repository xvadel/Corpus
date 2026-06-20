"""
Auth Routes (Phase 2)
=====================
Endpoints:
  POST /api/auth/register   → Create a new user account
  POST /api/auth/login      → Log in and receive a JWT access token
  GET  /api/auth/me         → Get the current user's profile (requires Bearer token)

All endpoints return `501 Not Implemented` until Phase 2 is built.

Phase 2 implementation checklist:
  1. Uncomment backend/models/user.py and run: alembic upgrade head
  2. Uncomment backend/auth/utils.py (hash_password, create_access_token, etc.)
  3. Replace the stub handlers below with real DB queries + JWT responses
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr, Field
from typing import Dict, Any

router = APIRouter(prefix="/auth", tags=["Authentication"])


# ── Request Schemas (ready for Phase 2) ─────────────────────────────────────

class RegisterRequest(BaseModel):
    email: EmailStr = Field(..., example="user@example.com")
    password: str = Field(..., min_length=8, example="SecurePass123!")
    full_name: str = Field(..., example="Jane Doe")


class LoginRequest(BaseModel):
    email: EmailStr = Field(..., example="user@example.com")
    password: str = Field(..., example="SecurePass123!")


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ── Route Handlers ───────────────────────────────────────────────────────────

@router.post(
    "/register",
    summary="Register a new user account",
    description=(
        "Create a new Corpus account with email and password. "
        "**Phase 2 — currently returns 501.**"
    ),
    status_code=501,
)
async def register(body: RegisterRequest) -> Dict[str, Any]:
    # TODO (Phase 2):
    #   from backend.database.session import get_db
    #   from backend.auth.utils import hash_password
    #   from backend.models.user import User
    #   db = next(get_db())
    #   user = User(email=body.email, hashed_password=hash_password(body.password), full_name=body.full_name)
    #   db.add(user); db.commit(); db.refresh(user)
    #   return {"id": user.id, "email": user.email}
    raise HTTPException(status_code=501, detail="User registration coming in Phase 2.")


@router.post(
    "/login",
    summary="Log in and get a JWT token",
    description=(
        "Authenticate with email + password. Returns a JWT Bearer token. "
        "**Phase 2 — currently returns 501.**"
    ),
    response_model=TokenResponse,
    status_code=501,
)
async def login(body: LoginRequest) -> TokenResponse:
    # TODO (Phase 2):
    #   from backend.auth.utils import verify_password, create_access_token
    #   user = db.query(User).filter(User.email == body.email).first()
    #   if not user or not verify_password(body.password, user.hashed_password):
    #       raise HTTPException(status_code=401, detail="Invalid credentials")
    #   token = create_access_token({"sub": user.email})
    #   return TokenResponse(access_token=token)
    raise HTTPException(status_code=501, detail="Authentication coming in Phase 2.")


@router.get(
    "/me",
    summary="Get current user profile",
    description=(
        "Returns the logged-in user's profile. Requires `Authorization: Bearer <token>` header. "
        "**Phase 2 — currently returns 501.**"
    ),
    status_code=501,
)
async def get_current_user() -> Dict[str, Any]:
    # TODO (Phase 2):
    #   from fastapi.security import OAuth2PasswordBearer
    #   Decode Bearer token → fetch user from DB
    raise HTTPException(status_code=501, detail="User profile coming in Phase 2.")
