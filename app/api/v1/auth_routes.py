from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.models.user import UserModel
from app.schemas.user import UserResponse

from app.core.exceptions import ConflictException
from app.schemas.user import UserCreate, UserResponse
from app.services import user_service

from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.user import Token
from app.core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db, user_data)

@router.post("/login", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = user_service.authenticate_user(db, email=form_data.username, password=form_data.password)
    if not user:
        raise ConflictException("Email or password is incorrect.")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def get_logged_user_profile(current_user: UserModel = Depends(get_current_user)):
    return current_user