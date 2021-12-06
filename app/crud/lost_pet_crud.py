from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import models, schemas


def get_lost_pet_by_id(db: Session, lost_pet_id: int):
    return db.query(models.LostPet).filter(models.LostPet.id == lost_pet_id).first()


def get_lost_pets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.LostPet).filter(models.LostPet.found == False).offset(skip).limit(limit).all()  # noqa


def create_lost_pet(db: Session, lost_pet: schemas.LostPetCreate, user_id: int):
    db_lost_pet = models.LostPet(**lost_pet.dict(), owner_id=user_id)
    db.add(db_lost_pet)
    db.commit()
    db.refresh(db_lost_pet)
    return db_lost_pet


def update_lost_pet(db: Session, db_lost_pet: models.LostPet, lost_pet_in: schemas.LostPetUpdate):
    lost_pet_data = jsonable_encoder(db_lost_pet)

    if isinstance(lost_pet_in, dict):
        update_data = lost_pet_in
    else:
        update_data = lost_pet_in.dict(exclude_unset=True)

    for field in lost_pet_data:
        if field in update_data:
            setattr(db_lost_pet, field, update_data.get(field))

    db.add(db_lost_pet)
    db.commit()
    db.refresh(db_lost_pet)
    return db_lost_pet


def mark_lost_pet_as_found(db: Session, db_lost_pet: models.LostPet):
    setattr(db_lost_pet, 'found', True)
    db.add(db_lost_pet)
    db.commit()
    db.refresh(db_lost_pet)
    return db_lost_pet


def remove_lost_pet(db: Session, lost_pet_id: int):
    db_lost_pet = db.query(models.LostPet).get(lost_pet_id)
    db.delete(db_lost_pet)
    db.commit()
