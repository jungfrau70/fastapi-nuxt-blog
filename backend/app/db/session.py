import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.settings import configs

DATABASE_USER = configs.POSTGRES_USER
DATABASE_PASSWORD = configs.POSTGRES_PASSWORD
DATABASE_HOST = configs.POSTGRES_SERVER
DATABASE_PORT = configs.POSTGRES_PORT
DATABASE_NAME = configs.POSTGRES_DATABASE

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{ DATABASE_USER }:{ DATABASE_PASSWORD }@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
# SQLALCHEMY_DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///./test.db')

# print(SQLALCHEMY_DATABASE_URL)

if SQLALCHEMY_DATABASE_URL.startswith('sqlite'):
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    # Dependency
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
