from pydantic import BaseModel, Field, field_validator
from typing import List
from constants import Roles
import datetime


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    accessToken: str


class TestUser(BaseModel):
    email: str
    fullName: str
    password: str
    passwordRepeat: str

    roles: List[str] = Field(default_factory=lambda: [Roles.USER.value])
    verified: bool = False
    banned: bool = False

    @field_validator("passwordRepeat")
    @classmethod
    def check_password_repeat(cls, value: str, info):
        if "password" in info.data and value != info.data["password"]:
            raise ValueError("Пароли не совпадают")
        return value


class RegisterUserResponse(BaseModel):
    id: str
    email: str = Field(
        pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
        description="Email пользователя"
    )
    fullName: str = Field(
        min_length=1,
        max_length=100,
        description="Полное имя пользователя"
    )
    verified: bool
    banned: bool
    roles: List[Roles]
    createdAt: str = Field(
        description="Дата и время создания пользователя в формате ISO 8601"
    )

    @field_validator("createdAt")
    def validate_created_at(cls, value: str) -> str:
        try:
            datetime.datetime.fromisoformat(value)
        except ValueError:
            raise ValueError("Некорректный формат даты и времени. Ожидается ISO 8601")
        return value