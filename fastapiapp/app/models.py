from sqlalchemy import Column, Integer, String
from .database import Base

class PhoneNumber(Base):
    __tablename__ = 'phonenumbers'
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, unique=True, index=True)
    user_key_press = Column(String)





# from sqlalchemy import Column, Integer, String, create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker, scoped_session

# Base = declarative_base()

# class PhoneNumber(Base):
#     __tablename__ = "phonenumbers"
#     id = Column(Integer, primary_key=True, index=True)
#     phone_number = Column(String, index=True)
#     user_key_press = Column(String, index=True)

