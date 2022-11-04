from env_inform import DB_LOGIN_INFORM

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine(DB_LOGIN_INFORM)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #? autocommit=False : 데이터 변경 후 commit을 해야만 데이터베이스에 적용

Base = declarative_base()