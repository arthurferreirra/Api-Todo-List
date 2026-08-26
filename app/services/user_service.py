from sqlalchemy.orm import Session
from app.models.user import UserModel
from app.schemas.user import UserCreate
from app.core.security import get_password_hash
from app.core.exceptions import ConflictException
from app.core.security import verify_password
from app.core.exceptions import NotFoundException

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(UserModel).filter(UserModel.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user



def create_user(db: Session, user_data: UserCreate):
    existing_user = db.query(UserModel).filter(UserModel.email == user_data.email).first()
    if existing_user:
        raise ConflictException(detail="User with this email already exists.")

    hashed_password = get_password_hash(user_data.password)

    db_user = UserModel(
        email=user_data.email,
        hashed_password=hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user