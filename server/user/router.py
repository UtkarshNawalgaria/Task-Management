import jwt
from typing import List
from passlib.hash import bcrypt

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from db.config import get_db_session
from auth import oauth2_scheme
from logger import logger
from config import get_settings

from .models import User
from .schemas import UserRead, UserCreate
from .services import authenticate_user

auth_router = APIRouter(prefix="/auth")
user_router = APIRouter(prefix="/user", dependencies=[Depends(oauth2_scheme)])

settings = get_settings()


@auth_router.post("/register", response_model=UserRead)
def register_user(user: UserCreate, session: Session = Depends(get_db_session)):

    existing_users = session.exec(select(User).where(User.email == user.email)).all()

    if len(existing_users):
        raise HTTPException(status_code=400, detail="User with email already exists.")

    new_user = User(
        name="User", email=user.email, password_hash=bcrypt.hash(user.password)
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user


@auth_router.post("/login")
def user_login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_db_session),
):

    my_user = authenticate_user(form_data.username, form_data.password, session)

    if not my_user:
        logger.info(f"{form_data.username} either does not exists or passowrd is wrong")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User email or password is not correct",
        )

    token = jwt.encode(UserRead.from_orm(my_user).dict(), settings.JWT_SECRET)

    return {"access_token": token, "token_type": "bearer"}


@user_router.get("/", response_model=List[UserRead])
def get_all_users(session: Session = Depends(get_db_session)):
    users = session.exec(select(User)).all()

    return users
