import uuid
import random
import string
import datetime
from constants import Roles


class DataGenerator:
    """Генерация тестовых данных."""

    @staticmethod
    def movie():
        return {
            "name": f"Test Movie {uuid.uuid4()}",
            "price": 100,
            "description": "Test",
            "location": "MSK",
            "published": True,
            "genreId": 1
        }

    @staticmethod
    def generate_random_email():
        return f"test_{uuid.uuid4().hex[:8]}@mail.com"

    @staticmethod
    def generate_random_name():
        return f"User_{uuid.uuid4().hex[:6]}"

    @staticmethod
    def generate_random_password(length=12):
        if length < 8:
            length = 8

        letters = string.ascii_letters
        digits = string.digits

        password = [
            random.choice(letters),
            random.choice(digits)
        ]

        all_chars = letters + digits
        password += random.choices(all_chars, k=length - 2)

        random.shuffle(password)
        return ''.join(password)

    @staticmethod
    def generate_user_data() -> dict:
        """Генерирует данные для тестового пользователя"""
        return {
            "id": str(uuid.uuid4()),
            "email": DataGenerator.generate_random_email(),
            "full_name": DataGenerator.generate_random_name(),
            "password": DataGenerator.generate_random_password(),
            "created_at": datetime.datetime.now().isoformat(),
            "updated_at": datetime.datetime.now().isoformat(),
            "verified": False,
            "banned": False,
            "roles": [Roles.USER.value]
        }

    @staticmethod
    def generate_random_int(max_value: int = 1000):
        return random.randint(1, max_value)