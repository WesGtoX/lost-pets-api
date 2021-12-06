from typing import Dict
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas, dependencies, docs
from app.db.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get('/', responses={200: docs.RESPONSES_EXAMPLE.get('hello_world')})
def hello_world() -> Dict[str, str]:
    return {'hello_world': 'Lost Pets API'}


# User
@app.post('/users/', response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(dependencies.get_db)) -> schemas.User:
    db_user = crud.get_user_by_email(db=db, email=user.email)

    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User already registered')

    return crud.create_user(db=db, user=user)


@app.get('/users/{user_id}', response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(dependencies.get_db)) -> schemas.User:
    user = crud.get_user_by_id(db=db, user_id=user_id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

    return user


# Lost Pet
@app.post('/lost-pets/{owner_id}/', response_model=schemas.LostPet, status_code=status.HTTP_201_CREATED)
def create_lost_pet(owner_id: int, lost_pet: schemas.LostPetCreate,
                    db: Session = Depends(dependencies.get_db)) -> schemas.LostPet:
    user = crud.get_user_by_id(db=db, user_id=owner_id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

    return crud.create_lost_pet(db=db, lost_pet=lost_pet, user_id=owner_id)


@app.post('/list')
async def read_lost_pets():
    return {}


@app.get('/lost-pets/{lost_pet_id}', response_model=schemas.LostPet)
def read_lost_pet_by_id(lost_pet_id: int, db: Session = Depends(dependencies.get_db)) -> schemas.LostPet:
    lost_pet = crud.get_lost_pet_by_id(db=db, lost_pet_id=lost_pet_id)

    if not lost_pet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Lost Pet not found')

    return lost_pet


@app.put('/update/{id}')
async def update_lost_pet_by_id():
    return {}


@app.delete('/destroy/{id}')
async def remove_lost_pet_by_id():
    return {}


@app.post('/found/{id}')
async def mark_lost_pet_found():
    return {}
