from typing import Optional, List
from pydantic import BaseModel

from app.schemas.lost_pet import LostPet


class UserBase(BaseModel):
    name: str
    phone: str
    email: str
    address: Optional[str] = None


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    items: List[LostPet] = []

    class Config:
        orm_mode = True
