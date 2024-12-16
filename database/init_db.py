import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine

from db_models import Base
from core import config, DATABASE_URL


def create_database():
    connection = psycopg2.connect(user="postgres", password=config.database.password)
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()

    try:
        cursor.execute('CREATE DATABASE cueta_database')  # Создание базы данных
        print("База данных создана.")
    except psycopg2.errors.DuplicateDatabase:
        print("База данных уже существует.")
    finally:
        cursor.close()
        connection.close()


def create_tables():
    engine = create_engine(DATABASE_URL.replace("asyncpg", "psycopg2"))
    Base.metadata.create_all(engine)
    print("Таблицы созданы.")


if __name__ == "__main__":
    create_database()
    create_tables()
