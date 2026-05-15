from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from resources.db_creds import MoviesDbCreds
from typing import Generator


USERNAME = MoviesDbCreds.USERNAME
PASSWORD = MoviesDbCreds.PASSWORD
HOST = MoviesDbCreds.HOST
PORT = MoviesDbCreds.PORT
DATABASE_NAME = MoviesDbCreds.DATABASE_NAME

#  движок для подключения к базе данных
engine = create_engine(
    f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}",
    echo=False  # Установить True для отладки SQL запросов
)

#  создаем фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



def get_db_session() -> Generator[Session, None, None]:
    """
        Создает и предоставляет сессию базы данных.

        Использует генератор для автоматического закрытия
        сессии после завершения работы с БД.
        """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()