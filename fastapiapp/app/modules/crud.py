from sqlalchemy.orm import Session
from modules import models, schemas

def create_phone_number(db: Session, phone_number: schemas.PhoneNumberCreate):
    db_phone_number = models.PhoneNumber(number=phone_number.number)
    db.add(db_phone_number)
    db.commit()
    db.refresh(db_phone_number)
    return db_phone_number
