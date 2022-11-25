from passlib.context import CryptContext
from sqlalchemy.orm import Session
from domain.User.user_schema import UserCreate, UserUpdate
from models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(db: Session, user_create: UserCreate):
    db_user = User(
        username=user_create.username,
        password=pwd_context.hash(user_create.password1),
    )
    db.add(db_user)
    db.commit()


def get_existing_user(db: Session, user_create: UserCreate):
    return db.query(User).filter((User.username == user_create.username)).first()


def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def update_user(db: Session, db_user: User, user_update: UserUpdate):
    db_user.icon = user_update.icon

    db.add(db_user)
    db.commit()
