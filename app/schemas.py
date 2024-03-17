from pydantic import BaseModel

class PhoneNumberBase(BaseModel):
    phone_number: str

class PhoneNumberCreate(PhoneNumberBase):
    user_key_press: str

class PhoneNumber(PhoneNumberBase):
    id: int

    class Config:
        orm_mode = True
