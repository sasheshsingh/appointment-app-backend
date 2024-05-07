from fastapi import security, HTTPException, Depends

from users.db.hash import Hash
from users.schemas import UserBase, UserDisplay
from sqlalchemy.orm.session import Session
from users.models import DBUser
from settings import JWT_SECRET_KEY, ALGORITHM, get_db
from fastapi.security import OAuth2PasswordBearer

import jwt


oauth2schema = OAuth2PasswordBearer(tokenUrl="/api/login")


def create_user(db: Session, request: UserBase):
    new_user = DBUser(username=request.username,
                      email=request.email,
                      password=Hash.bcrypt(db, request.password),
                      is_active=True)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user_by_email(email: str, db: Session):
    return db.query(DBUser).filter(DBUser.email == email).first()


def update_user(db: Session, user_id: int, request: UserBase):
    user = db.query(DBUser).filter(DBUser.id == user_id).first()
    user.update({
        DBUser.password: Hash.bcrypt(db, request.password),
        DBUser.email: request.email,
        DBUser.username: request.username
    })


def authentcate_user(email: str, password: str, db: Session):
    user = get_user_by_email(db=db, email=email)
    if not user:
        return False

    if not user.verify_password(password):
        return False

    return user


def create_token(user: DBUser):
    user_obj = UserBase.from_orm(user)
    token = jwt.encode(user_obj.dict(), JWT_SECRET_KEY)
    return dict(access_token=token, token_type="jwt", user=user.id)


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2schema)):
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
    try:
        email = payload.get('email')
        if email is None:
            raise HTTPException(status_code=401, detail="Could not validate sdffcredentials")

        user = db.query(DBUser).filter(DBUser.email == email).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")

        return UserDisplay.from_orm(user)
    except:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
