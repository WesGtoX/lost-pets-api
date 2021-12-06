from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db import Base


class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)
    phone = Column(String, index=True)
    address = Column(String, index=True)

    lost_pets = relationship('LostPet', back_populates='owner')
