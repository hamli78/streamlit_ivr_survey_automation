from pydantic import BaseModel
class PhoneNumberBase(BaseModel):
    number: str

class PhoneNumberCreate(PhoneNumberBase):
    pass

class PhoneNumber(PhoneNumberBase):
    id: int

    class Config:
        orm_mode = True

























# models.py
# # models if got database
# from sqlalchemy import Column, Integer, String
# from modules.database import Base
# class PhoneNumber(Base):
#     __tablename__ = "phonenumbers"

#     id = Column(Integer, primary_key=True, index=True)
#     number = Column(String, unique=True, index=True)



# database.py
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# import os

# DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()
