from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from config.db import get_db
from model import Spice, Animal, Mixed, User
from schemas import SpiceBase, AnimalBase, MixedBase, UserBase, MixedUpdate
from pydantic import BaseModel
from .chat_gpt_api import ChatGPTAPI
from datetime import datetime

router = APIRouter()
chat_gpt_api = ChatGPTAPI()

class ImagePrompt(BaseModel):
    prompt: str

class ImageResponse(BaseModel):
    image_url: str

# Spice endpoints
@router.get("/spices/", response_model=List[SpiceBase])
async def get_spices(db: Session = Depends(get_db)):
    return db.query(Spice).all()

@router.get("/spices/{spice_id}", response_model=SpiceBase)
async def get_spice(spice_id: int, db: Session = Depends(get_db)):
    spice = db.query(Spice).filter(Spice.id == spice_id).first()
    if not spice:
        raise HTTPException(status_code=404, detail="Spice not found")
    return spice


# Animal endpoints
@router.get("/animals/", response_model=List[AnimalBase])
async def get_animals(db: Session = Depends(get_db)):
    return db.query(Animal).all()

@router.get("/animals/{animal_id}", response_model=AnimalBase)
async def get_animal(animal_id: int, db: Session = Depends(get_db)):
    animal = db.query(Animal).filter(Animal.id == animal_id).first()
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    return animal


# Mixed endpoints
@router.get("/mixeds/", response_model=List[MixedBase])
async def get_mixeds(db: Session = Depends(get_db)):
    mixes = db.query(Mixed).all()
    for mix in mixes:
        # Добавляем wallet_address из связанного пользователя
        if mix.user:
            mix.wallet_address = mix.user.wallet_address
    return mixes

@router.post("/mixeds/", response_model=MixedBase)
async def create_mixed(mixed_data: MixedBase, db: Session = Depends(get_db)):
    db_mixed = Mixed(**mixed_data.dict())
    db.add(db_mixed)
    db.commit()
    db.refresh(db_mixed)
    return db_mixed

@router.get("/mixeds/{mixed_id}", response_model=MixedBase)
async def get_mixed(mixed_id: int, db: Session = Depends(get_db)):
    mixed = db.query(Mixed).filter(Mixed.id == mixed_id).first()
    if not mixed:
        raise HTTPException(status_code=404, detail="Mixed not found")
    return mixed

@router.delete("/mixeds/{mixed_id}")
async def delete_mixed(mixed_id: int, db: Session = Depends(get_db)):
    mixed = db.query(Mixed).filter(Mixed.id == mixed_id).first()
    if not mixed:
        raise HTTPException(status_code=404, detail="Mixed not found")
    db.delete(mixed)
    db.commit()
    return {"message": "Mixed deleted successfully"}

@router.put("/mixeds/{mixed_id}", response_model=MixedBase)
async def update_mixed(mixed_id: int, mixed_data: MixedUpdate, db: Session = Depends(get_db)):
    mixed = db.query(Mixed).filter(Mixed.id == mixed_id).first()
    if not mixed:
        raise HTTPException(status_code=404, detail="Mixed not found")
    
    # Обновляем только необходимые поля
    for key, value in mixed_data.dict().items():
        setattr(mixed, key, value)
    
    # Обновляем updated_at
    mixed.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(mixed)
    
    # Добавляем wallet_address из связанного пользователя
    if mixed.user:
        mixed.wallet_address = mixed.user.wallet_address
    
    return mixed


# User CRUD endpoints
@router.post("/users/", response_model=UserBase)
async def create_user(user_data: UserBase, db: Session = Depends(get_db)):
    db_user = User(**user_data.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/users/", response_model=List[UserBase])
async def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.get("/users/{user_id}", response_model=UserBase)
async def get_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.uid == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/users/{user_id}", response_model=UserBase)
async def update_user(user_id: str, user_data: UserBase, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.uid == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    for key, value in user_data.dict().items():
        setattr(user, key, value)
    
    db.commit()
    db.refresh(user)
    return user

@router.delete("/users/{user_id}")
async def delete_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.uid == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}

@router.post("/generate_image/", response_model=ImageResponse)
async def generate_image(prompt: ImagePrompt):
    try:
        image_url = await chat_gpt_api.generate_image(prompt.prompt)
        return {"image_url": image_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

