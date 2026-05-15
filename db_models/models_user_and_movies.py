from sqlalchemy import Column, String, Boolean, DateTime, Integer, Float, Enum
from sqlalchemy.orm import declarative_base
from typing import Dict, Any
from sqlalchemy.dialects.postgresql import ARRAY
from constants import Roles

Base = declarative_base()


class UserDBModel(Base):
    """Модель таблицы users"""

    __tablename__ = "users"

    id = Column(String, primary_key=True)
    email = Column(String)
    full_name = Column(String)
    password = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    verified = Column(Boolean)
    banned = Column(Boolean)
    roles = Column(ARRAY(Enum(Roles, name="Role")))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "email": self.email,
            "full_name": self.full_name,
            "password": self.password,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "verified": self.verified,
            "banned": self.banned,
            "roles": self.roles
        }

    def __repr__(self):
        return f"<User(id='{self.id}', email='{self.email}')>"


class MovieDBModel(Base):
    """Модель таблицы movies"""

    __tablename__ = "movies"

    id = Column(String, primary_key=True)
    name = Column(String)
    price = Column(Float)
    description = Column(String)
    image_url = Column(String)
    location = Column(String)
    published = Column(Boolean)
    rating = Column(Float)
    genre_id = Column(Integer)
    created_at = Column(DateTime)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "description": self.description,
            "image_url": self.image_url,
            "location": self.location,
            "published": self.published,
            "rating": self.rating,
            "genre_id": self.genre_id,
            "created_at": self.created_at
        }

    def __repr__(self):
        return f"<Movie(id='{self.id}', name='{self.name}', price={self.price})>"