from sqlalchemy.orm import Session
from db_models.models_user_and_movies import UserDBModel, MovieDBModel



class DBHelper:
    """Класс с методами для работы с БД в тестах"""

    def __init__(self, db_session: Session):
        self.db_session = db_session

    # -------- USER -------- #

    def create_test_user(self, user_data: dict) -> UserDBModel:
        """Создает тестового пользователя"""
        user = UserDBModel(**user_data)
        self.db_session.add(user)
        self.db_session.commit()
        self.db_session.refresh(user)
        return user

    def get_user_by_id(self, user_id: str):
        """Получает пользователя по ID"""
        return (
            self.db_session
            .query(UserDBModel)
            .filter_by(id=user_id)
            .first()
        )

    def get_user_by_email(self, email: str):
        """Получает пользователя по email"""
        return (
            self.db_session
            .query(UserDBModel)
            .filter_by(email=email)
            .first()
        )

    def user_exists_by_email(self, email: str) -> bool:
        """Проверяет существование пользователя по email"""
        return self.get_user_by_email(email) is not None

    def delete_user(self, user: UserDBModel):
        """Удаляет пользователя"""
        self.db_session.delete(user)
        self.db_session.commit()

    # -------- MOVIES -------- #

    def get_movie_by_id(self, movie_id: str):
        """Получает фильм по ID"""
        return (
            self.db_session
            .query(MovieDBModel)
            .filter_by(id=movie_id)
            .first()
        )

    def get_movie_by_name(self, name: str):
        """Получает фильм по названию"""
        return (
            self.db_session
            .query(MovieDBModel)
            .filter_by(name=name)
            .first()
        )

    def movie_exists_by_id(self, movie_id: str) -> bool:
        """Проверка существования фильма по ID"""
        return self.get_movie_by_id(movie_id) is not None

    def delete_movie(self, movie: MovieDBModel):
        """Удаление фильма"""
        self.db_session.delete(movie)
        self.db_session.commit()

    def delete_movie_by_id(self, movie_id: str):
        """Удаление фильма по ID"""
        movie = self.get_movie_by_id(movie_id)
        if movie:
            self.db_session.delete(movie)
            self.db_session.commit()

    def refresh(self):
        """Сбрасывает кеш SQLAlchemy сессии и принудительно перечитывает данные из БД.

            Используется в тестах после API-операций (CREATE / UPDATE / DELETE),
            чтобы гарантировать, что последующие DB-запросы возвращают актуальные данные,
            а не закешированные объекты из session.
            """
        self.db_session.expire_all()

    # -------- CLEANUP -------- #

    def cleanup_test_data(self, objects_to_delete: list):
        """Очищает тестовые данные"""
        for obj in objects_to_delete:
            if obj:
                self.db_session.delete(obj)
        self.db_session.commit()