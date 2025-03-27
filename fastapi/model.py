from sqlalchemy import String, Column, Integer, ForeignKey, Float, Index
from sqlalchemy.orm import relationship, backref

from config.db import Base
from custom_types import EmailType, SlugType, TONWalletType


class Spice(Base):
    __tablename__ = "spices"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), index=True)
    image = Column(String(255))


class Animal(Base):
    __tablename__ = "animals"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), index=True)
    slug_id = Column(SlugType, unique=True, index=True)


class User(Base):
    __tablename__ = "users"
    uid = Column(String(255), primary_key=True, index=True)
    username = Column(String(255), index=True)
    mail = Column(EmailType, unique=True, index=True)
    wallet_address = Column(TONWalletType, unique=True, index=True)
    coins = Column(Float, default=0.0, index=True)
    mixed_list = relationship("Mixed", back_populates="user")


class Mixed(Base):
    __tablename__ = "mixeds"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), index=True)
    image = Column(String(255))
    points = Column(Float, default=0.0, index=True)
    
    spice_id = Column(Integer, ForeignKey('spices.id'), index=True)
    animal_slug_id = Column(SlugType, ForeignKey('animals.slug_id'), index=True)
    user_id = Column(String(255), ForeignKey('users.uid'), index=True)
    
    spice = relationship("Spice", backref=backref("mixed", uselist=False))
    animal = relationship("Animal", backref=backref("mixed", uselist=False))
    user = relationship("User", back_populates="mixed_list")

