from .db_models import Base, Admin, User
from .database import DataBase

from core import config

db = DataBase(
    f"postgresql+asyncpg://{config.database.user}:{config.database.password}@{config.database.host}/{config.database.name}"
)
