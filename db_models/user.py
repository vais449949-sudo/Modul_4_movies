from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base
from typing import Dict, Any
from db_requester.db_client import get_db_session
from sqlalchemy.dialects.postgresql import ARRAY

from sqlalchemy import Enum
import enum
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


# отдельный файл лучше, но если оставляешь тут:
from sqlalchemy.orm import Session


def db_session() -> Session:
    session = get_db_session()
    try:
        yield session
    finally:
        session.close()