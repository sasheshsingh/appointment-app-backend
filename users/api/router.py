from fastapi import APIRouter, Depends, HTTPException
from users.schemas import UserBase, UserDisplay
from sqlalchemy.orm import Session
from users.db import db_user
from settings import get_db
from typing import List, Optional
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Form
from datetime import datetime, timedelta
import requests
from config import settings

router = APIRouter(prefix='/api', tags=['users'])


@router.post('/signup')
async def create_user(email: str = Form(...), password: str = Form(...), username: str = Form(...),
                      db: Session = Depends(get_db)):
    obj = db_user.get_user_by_email(email, db)
    if obj:
        raise HTTPException(status_code=422, detail='User already exists')
    user = UserBase(email=email, password=password, username=username)
    db_user.create_user(db, user)
    return db_user.create_token(user)


@router.post('/login')
async def login(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db_user.authentcate_user(db=db, email=user.username, password=user.password)
    if not user:
        raise HTTPException(status_code=401, detail='Incorrect email or password')
    return db_user.create_token(user)


@router.post('/users/me')
async def read_user_me(user: UserBase = Depends(db_user.get_current_user)):
    return user


@router.post('/microsoft_login')
async def microsoft_login(code: str, redirect_uri: str, db: Session = Depends(get_db)):
    if not code:
        raise HTTPException(status_code=400, detail="Authorization code is required")
    if not redirect_uri:
        raise HTTPException(status_code=400, detail="Redirect URI is required")

    client_id = settings.AZURE_CLIENT_ID
    client_secret = settings.AZURE_CLIENT_SECRET_VALUE
    token_url = f"https://login.microsoftonline.com/{settings.AZURE_AD_TENANT_ID}/oauth2/v2.0/token"
    print(client_secret, client_id, token_url)
    token_data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code',
    }
    token_response = requests.post(token_url, data=token_data)
    token_response_data = token_response.json()
    if 'error' in token_response_data:
        raise HTTPException(status_code=400, detail=token_response_data)

    access_token = token_response_data['access_token']
    expiry_at = token_response_data.get('expires_in')
    if expiry_at:
        expiration_time = datetime.now() + timedelta(seconds=int(expiry_at))
    else:
        expiration_time = datetime.now() + timedelta(seconds=3600)

    user_info_url = 'https://graph.microsoft.com/v1.0/me'
    headers = {'Authorization': f'Bearer {access_token}'}
    user_info_response = requests.get(user_info_url, headers=headers)
    user_info = user_info_response.json()
    email = user_info.get('mail', '')
    first_name = user_info.get('givenName', '')
    last_name = user_info.get('surname', '')
    name = user_info.get('displayName', '')
    user_name = first_name.replace(' ', '').lower() + "." + last_name.replace(' ', '').lower()

    if email:
        obj = db_user.get_user_by_email(email, db)
        if obj:
            return db_user.create_token(obj)
        user = UserBase(email=email, password="abcd1234", username="abcd1234")
        db_user.create_user(db, user)
        return db_user.create_token(user)
    else:
        raise HTTPException(status_code=400, detail={'error': 'User information not found'})
