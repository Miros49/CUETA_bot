from database.db_models import Base, User, Event, Registration, FundRaiser, Transaction
from database.database import DataBase

from core import DATABASE_URL

db: DataBase = DataBase(DATABASE_URL)
