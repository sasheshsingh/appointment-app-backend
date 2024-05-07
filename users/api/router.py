from fastapi import APIRouter, Depends, HTTPException
from users.schemas import UserBase, UserDisplay
from sqlalchemy.orm import Session
from users.db import db_user
from settings import get_db
from typing import List, Optional
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


router = APIRouter(prefix='/api', tags=['users'])


@router.post('/signup', response_model=UserDisplay)
async def create_user(user: UserBase, db: Session = Depends(get_db)):
    obj = db_user.get_user_by_email(user.email, db)
    if obj:
        raise HTTPException(status_code=422, detail='User already exists')
    return db_user.create_user(db, user)


@router.post('/login')
async def login(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db_user.authentcate_user(db=db, email=user.username, password=user.password)
    if not user:
        raise HTTPException(status_code=401, detail='Incorrect email or password')
    return db_user.create_token(user)

@router.post('/users/me')
async def read_user_me(user: UserBase = Depends(db_user.get_current_user)):
    return user