import os

from dotenv import load_dotenv
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    artikul = Column(String, index=True)
    price = Column(Float)
    rating = Column(Float)
    total_quantity = Column(Integer)
    is_trackable = Column(Boolean, default=False)

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def create_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

