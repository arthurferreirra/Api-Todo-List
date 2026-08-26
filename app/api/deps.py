from app.database import sessionLocal
from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.core.security import SECRET_KEY, ALGORITHM
from app.models.user import UserModel
from app.core.exceptions import ConflictException # ou uma HTTPException 401

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login") #authentication route for obtaining a token. This is used in the get_current_user function to extract the token from the request.
def get_db(): # Dependency function to get a database session, which can be used in FastAPI routes to interact with the database.
    db = sessionLocal() 
    try:
        yield db #yielding the database session to the caller, allowing them to use it within a context manager.
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = ConflictException(
        "Could not validate credentials", # Em produção, use status_code=401
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(UserModel).filter(UserModel.email == email).first()
    if user is None:
        raise credentials_exception
    return user
