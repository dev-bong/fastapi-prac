from datetime import timedelta, datetime
import secrets

from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.User import user_crud, user_schema
from domain.User.user_crud import pwd_context
from env_inform import SIGN_UP_CODE
from models import User

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 토큰 유효시간 (분 단위)
SECRET_KEY = secrets.token_hex(32)  # 암호화시 사용하는 64자리 랜덤 문자열
ALGORITHM = "HS256"  # 토큰 생성시 사용하는 알고리즘
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login")

router = APIRouter(
    prefix="/api/user",
)


@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def user_create(_user_create: user_schema.UserCreate, db: Session = Depends(get_db)):
    user = user_crud.get_existing_user(db, user_create=_user_create)
    if SIGN_UP_CODE:
        if _user_create.sign_up_code != SIGN_UP_CODE:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="가입 코드가 잘못되었습니다."
            )
    else:  # ? SIGN_UP_CODE가 존재하지 않는 상태.. 회원가입 받지 않는다
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="현재 회원가입이 불가합니다."
        )

    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="이미 존재하는 사용자입니다."
        )
    user_crud.create_user(db=db, user_create=_user_create)


@router.post("/login", response_model=user_schema.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    print(SECRET_KEY)
    # check user and password
    user = user_crud.get_user(db, form_data.username)
    if not user or not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # make access token
    data = {
        "sub": user.username,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username,
    }


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    else:
        user = user_crud.get_user(db, username=username)
        if user is None:
            raise credentials_exception
        return user


@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
def user_update(
    # * 운영자용 유저 수정 API (지금은 icon만 수정 가능, 나중에 비번 수정까지?)
    _user_update: user_schema.UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_user = user_crud.get_user(db, username=_user_update.username)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="데이터를 찾을수 없습니다."  # ? 404?
        )
    if current_user.username != "master-bong":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="수정 권한이 없습니다."  # ? 403?
        )
    user_crud.update_user(db=db, db_user=db_user, user_update=_user_update)
