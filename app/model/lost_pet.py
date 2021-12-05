from pydantic import BaseModel


class LostPet(BaseModel):
    id: int
    name: str
    genre: str
    size: str
    color: str
    description: str
