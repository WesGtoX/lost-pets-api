from sqlalchemy.orm import Session

from app import models, schemas


def get_lost_pet_by_id(db: Session, lost_pet_id: int):
    return db.query(models.LostPet).filter(models.LostPet.id == lost_pet_id).first()


def get_lost_pets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.LostPet).filter(models.LostPet.found is False).offset(skip).limit(limit).all()


def create_lost_pet(db: Session, lost_pet: schemas.LostPetCreate, user_id: int):
    db_lost_pet = models.LostPet(**lost_pet.dict(), owner_id=user_id)
    db.add(db_lost_pet)
    db.commit()
    db.refresh(db_lost_pet)
    return db_lost_pet
