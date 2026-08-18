from sqlalchemy.orm import Session
from app.models.user import UserModel
from app.schemas.user import UserCreate
from app.core.security import get_password_hash
from app.core.exceptions import ConflictException

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