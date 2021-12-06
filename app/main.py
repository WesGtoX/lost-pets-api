from typing import Dict, List
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas, dependencies, docs
from app.db.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title='Lost Pets API',
    description='API for reporting lost pets.',
)


@app.get('/', responses={200: docs.RESPONSES_EXAMPLE.get('hello_world')}, tags=['hello_world'])
def hello_world() -> Dict[str, str]:
    return {'hello_world': 'Lost Pets API'}


# User
@app.post('/api/v1/users/', response_model=schemas.User, status_code=status.HTTP_201_CREATED, tags=['users'])
def create_user(user: schemas.UserCreate, db: Session = Depends(dependencies.get_db)) -> schemas.User:
    db_user = crud.get_user_by_email(db=db, email=user.email)

    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User already registered')

    return crud.create_user(db=db, user=user)


@app.get('/api/v1/users/{user_id}', response_model=schemas.User, tags=['users'])
def read_user(user_id: int, db: Session = Depends(dependencies.get_db)) -> schemas.User:
    user = crud.get_user_by_id(db=db, user_id=user_id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

    return user


# Lost Pet
@app.post('/api/v1/lost-pets/{owner_id}/', response_model=schemas.LostPet, status_code=status.HTTP_201_CREATED, tags=['lost_pets'])
def create_lost_pet(owner_id: int, lost_pet: schemas.LostPetCreate,
                    db: Session = Depends(dependencies.get_db)) -> schemas.LostPet:
    user = crud.get_user_by_id(db=db, user_id=owner_id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

    return crud.create_lost_pet(db=db, lost_pet=lost_pet, user_id=owner_id)


@app.get('/api/v1/lost-pets', response_model=List[schemas.LostPet], tags=['lost_pets'])
def read_lost_pets(skip: int = 0, limit: int = 100,
                   db: Session = Depends(dependencies.get_db)) -> List[schemas.LostPet]:
    return crud.get_lost_pets(db=db, skip=skip, limit=limit)


@app.get('/api/v1/lost-pets/{lost_pet_id}', response_model=schemas.LostPet, tags=['lost_pets'])
def read_lost_pet_by_id(lost_pet_id: int, db: Session = Depends(dependencies.get_db)) -> schemas.LostPet:
    lost_pet = crud.get_lost_pet_by_id(db=db, lost_pet_id=lost_pet_id)

    if not lost_pet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Lost Pet not found')

    return lost_pet


@app.put('/api/v1/lost-pets/{lost_pet_id}', response_model=schemas.LostPet, tags=['lost_pets'])
def update_lost_pet_by_id(lost_pet_id: int, lost_pet_in: schemas.LostPetUpdate,
                          db: Session = Depends(dependencies.get_db)) -> schemas.LostPet:
    db_lost_pet = crud.get_lost_pet_by_id(db=db, lost_pet_id=lost_pet_id)

    if not db_lost_pet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Lost Pet not found')

    return crud.update_lost_pet(db=db, db_lost_pet=db_lost_pet, lost_pet_in=lost_pet_in)


@app.delete('/api/v1/lost-pets/{lost_pet_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['lost_pets'])
def remove_lost_pet_by_id(lost_pet_id: int, db: Session = Depends(dependencies.get_db)) -> None:
    lost_pet = crud.get_lost_pet_by_id(db=db, lost_pet_id=lost_pet_id)

    if not lost_pet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Lost Pet not found')

    crud.remove_lost_pet(db=db, lost_pet_id=lost_pet_id)


@app.post('/api/v1/lost-pets/found/{lost_pet_id}', response_model=schemas.LostPet, tags=['lost_pets'])
def mark_lost_pet_found(lost_pet_id: int, db: Session = Depends(dependencies.get_db)) -> schemas.LostPet:
    db_lost_pet = crud.get_lost_pet_by_id(db=db, lost_pet_id=lost_pet_id)

    if not db_lost_pet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Lost Pet not found')

    return crud.mark_lost_pet_as_found(db=db, db_lost_pet=db_lost_pet)
