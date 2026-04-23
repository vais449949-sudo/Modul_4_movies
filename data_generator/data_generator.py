import uuid


class DataGenerator:
    """Генерация данных для нового фильма."""

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