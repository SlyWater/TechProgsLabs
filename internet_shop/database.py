from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from internet_shop.settings import get_settings

DATABASE_URL = get_settings().database_url
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
Base = declarative_base()
