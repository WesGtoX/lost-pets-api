from typing import Optional
from pydantic import BaseModel


class PetOwner(BaseModel):
    id: int
    name: str
    phone: str
    address: Optional[str] = None
