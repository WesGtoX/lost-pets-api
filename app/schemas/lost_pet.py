from pydantic import BaseModel


class LostPetBase(BaseModel):
    name: str
    genre: str
    breed: str
    size: str
    color: str
    description: str


class LostPetCreate(LostPetBase):
    pass


class LostPetUpdate(LostPetBase):
    pass


class LostPet(LostPetBase):
    id: int
    found: bool
    owner_id: int

    class Config:
        orm_mode = True
