from pydantic import BaseModel, EmailStr, Field, field_validator
from custom_types import EmailType, SlugType, TONWalletType
import re
from typing import Optional
from datetime import datetime


class SpiceBase(BaseModel):
    id: Optional[int] = None
    name: str
    image: str
    description: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class AnimalBase(BaseModel):
    id: Optional[int] = None
    name: str
    image: str
    description: str
    slug_id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class MixedUpdate(BaseModel):
    name: str
    image: str
    points: float
    spice_id: int
    animal_slug_id: str
    user_id: str

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class MixedBase(BaseModel):
    id: Optional[int] = None
    name: str
    image: str
    points: float
    spice_id: int
    animal_slug_id: str
    user_id: str
    wallet_address: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @field_validator('animal_slug_id')
    @classmethod
    def validate_slug(cls, v):
        if v is not None:
            # Convert to lowercase and replace spaces with hyphens
            v = v.lower().replace(' ', '-')
            # Remove any characters that aren't alphanumeric or hyphens
            v = re.sub(r'[^a-z0-9-]', '', v)
        return v

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class UserBase(BaseModel):
    uid: str
    username: str
    mail: str
    wallet_address: str
    coins: float = 0.0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

    @field_validator('mail')
    @classmethod
    def validate_email(cls, v):
        if v is not None:
            # Простая валидация email
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', v):
                raise ValueError("Invalid email format")
        return v

    @field_validator('wallet_address')
    @classmethod
    def validate_ton_wallet(cls, v):
        if v is not None:
            # TON address pattern: starts with EQ followed by base64 characters
            if not re.match(r'^EQ[a-zA-Z0-9+/]{48}$', v):
                raise ValueError("Invalid TON wallet address format")
        return v 