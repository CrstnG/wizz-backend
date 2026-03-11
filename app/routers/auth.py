from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.auth import SignInRequest, SignUpRequest, TokenResponse
from app.schemas.user import UserResponse
from app.services import auth_service

router = APIRouter()


@router.post("/signup/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup(data: SignUpRequest, db: Session = Depends(get_db)):
    """Registra un nuevo usuario en el sistema."""
    try:
        user = auth_service.register_user(db, data)
        return user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/signin/", response_model=TokenResponse)
def signin(data: SignInRequest, db: Session = Depends(get_db)):
    """Autentica un usuario y retorna un token JWT."""
    try:
        token = auth_service.authenticate_user(db, data.email, data.password)
        return TokenResponse(access_token=token)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
