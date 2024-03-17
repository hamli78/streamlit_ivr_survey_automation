from pydantic import BaseModel

class PhoneNumberBase(BaseModel):
    number: str

class PhoneNumberCreate(PhoneNumberBase):
    pass

class PhoneNumber(PhoneNumberBase):
    id: int

    class Config:
        orm_mode = True
