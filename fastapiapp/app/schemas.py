# Schemas will define the structure of the data you expect to receive and send.

from pydantic import BaseModel
class PhoneNumberBase(BaseModel):
    number: str

class PhoneNumberCreate(PhoneNumberBase):
    pass

class PhoneNumber(PhoneNumberBase):
    id: int

    class Config:
        orm_mode = True
