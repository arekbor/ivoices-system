from typing import Annotated
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import CreateUser, Token
from fastapi.security import OAuth2PasswordRequestForm
import bcrypt
from datetime import timedelta, datetime, timezone
import jwt
from app.core.settings import get_settings
from fastapi import Depends, HTTPException, status
from app.core.dependencies import oauth2_scheme, get_db

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid credentials",
    headers={"WWW-Authenticate": "Bearer"}
)

def register_user(data: CreateUser, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, data.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="User already exists"
        )
    hashed_password = hash_password(data.password)
    new_user = User(username=data.username, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def login_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    db_user = get_user_by_username(db, form_data.username)
    if not db_user or not verify_password(form_data.password, db_user.password):
        raise credentials_exception

    access_token = get_access_token(
        data={"sub":str(db_user.id), "name":db_user.username}
    )
    return Token(access_token=access_token, token_type="bearer")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, get_settings().JWT_SECRET_KEY, algorithms=[get_settings().JWT_ALGORITHM])
        sub = payload.get("sub")
        if sub is None:
            raise credentials_exception
        db_user = db.query(User).filter(User.id == sub).first()
        if db_user is None:
            raise credentials_exception
        return db_user
    except:
        raise credentials_exception
    
def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()
    
def get_access_token(data: dict, expires: timedelta | None = None):
    data_to_encode = data.copy()
    if expires:
        token_expire = datetime.now(timezone.utc) + expires
    else:
        token_expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    data_to_encode.update({"exp": token_expire})
    return jwt.encode(data_to_encode, key=get_settings().JWT_SECRET_KEY, algorithm=get_settings().JWT_ALGORITHM)
    
def hash_password(password: str):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed_password: str):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))