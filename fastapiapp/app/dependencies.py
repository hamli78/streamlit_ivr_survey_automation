from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from streamlit_ivr_survey_automation.fastapiapp.app.database import Base
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

# Assuming database.py exists and provides a DATABASE_URL or similar
from .database import engine

SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
