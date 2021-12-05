from fastapi import FastAPI

from app.model.lost_pet import LostPet
from app.model.pet_owner import PetOwner

app = FastAPI()


@app.get('/hello-world')
async def hello_world():
    return {'hello_world': 'Lost Pets API'}


@app.post('/register')
async def register_lost_pet(lost_pet: LostPet, pet_owner: PetOwner):
    return {}


@app.post('/list')
async def read_lost_pets():
    return {}


@app.get('/detail/{id}')
async def read_lost_pet_by_id():
    return {}


@app.put('/update/{id}')
async def update_lost_pet_by_id():
    return {}


@app.delete('/destroy/{id}')
async def remove_lost_pet_by_id():
    return {}


@app.post('/found/{id}')
async def mark_lost_pet_found():
    return {}
