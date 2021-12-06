from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from app.db import Base


class LostPet(Base):

    __tablename__ = 'lost_pets'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    genre = Column(String, index=True)
    breed = Column(String, index=True)
    size = Column(String, index=True)
    color = Column(String, index=True)
    found = Column(Boolean, default=False)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship('User', back_populates='lost_pets')
