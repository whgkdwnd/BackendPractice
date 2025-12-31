from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./app.db" #어떤 database를 사용할지 결정

engine = create_engine(# DB의 연결에 대한 모든 메타정보를 가진 객체
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # sqlite 전용
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()