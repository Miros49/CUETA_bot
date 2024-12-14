import asyncpg
import psycopg2

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from sqlalchemy.sql import or_, and_
from sqlalchemy import Column, MetaData, select, BigInteger, String, DECIMAL, SmallInteger, create_engine, func
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

from . import Admin, User

Base = declarative_base()


class DataBase:
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.engine = create_async_engine(self.database_url, echo=False)
        self.async_session = async_sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)

    async def create_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def get_admins_ids(self):
        async with self.async_session() as session:
            async with session.begin():
                query = select(Admin)
                result = await session.execute(query)
                admin_ids = [admin.id for admin in result.scalars().all()]
                return admin_ids

    async def get_admin(self, admin_id: int):
        async with self.async_session() as session:
            async with session.begin():
                query = select(Admin).filter(Admin.id == admin_id)
                result = await session.execute(query)
                admin = result.scalars().first()
                return admin

    async def add_admin(self, admin_id: int):
        async with self.async_session() as session:
            async with session.begin():
                admin = User(id=admin_id)
                session.add(admin)
                return await session.commit()

    async def get_admins(self):
        async with self.async_session() as session:
            async with session.begin():
                query = select(Admin)
                result = await session.execute(query)
                admins = result.scalars().all()
                return admins

    async def delete_admin(self, admin_id: int):
        async with self.async_session() as session:
            async with session.begin():
                query = select(Admin).filter(Admin.id == admin_id)
                result = await session.execute(query)
                admin = result.scalars().first()
                if admin:
                    await session.delete(admin)
                    await session.commit()
                    return True

    async def get_admins_usernames(self):
        async with self.async_session() as session:
            async with session.begin():
                query = select(User)
                result = await session.execute(query)
                user_ids = [user.id for user in result.scalars().all()]
                return user_ids

    async def set_user(self, user_id: int, username: str, lolz_profile: str | None = None,
                       ref_id: str | int | None = None):
        async with self.async_session() as session:
            async with session.begin():
                user = User(id=user_id, username=username, lolz_profile=lolz_profile, balance=0.00,
                            your_ref=int(ref_id) if ref_id else 0)
                session.add(user)
                await session.commit()
                return user.id

    async def get_user(self, user_id: int):
        async with self.async_session() as session:
            async with session.begin():
                query = select(User).filter(User.id == user_id)
                result = await session.execute(query)
                user = result.scalars().first()
                return user

    async def get_user_by_username(self, username: str):
        async with self.async_session() as session:
            async with session.begin():
                query = select(User).filter(User.username == username)
                result = await session.execute(query)
                user = result.scalars().first()
                return user

    async def user_exists(self, user_id: int):
        async with self.async_session() as session:
            async with session.begin():
                query = select(User).filter(User.id == user_id)
                result = await session.execute(query)
                user = result.scalars().first()
                if user:
                    return True
                else:
                    return False

    async def get_all_users(self):
        async with self.async_session() as session:
            async with session.begin():
                query = select(User)
                result = await session.execute(query)
                user_ids = [user.id for user in result.scalars().all()]
                return user_ids

    async def set_lolz_profile(self, user_id: int, lolz_profile):
        async with self.async_session() as session:
            async with session.begin():
                query = select(User).filter(User.id == user_id)
                result = await session.execute(query)
                user = result.scalars().first()
                if user.lolz_profile == " " or user.lolz_profile is None or user.lolz_profile == "":
                    lolz_profile = lolz_profile
                else:
                    lolz_profile = str(user.lolz_profile)
                user.lolz_profile = lolz_profile
                await session.commit()

    async def set_nickname(self, user_id: int, nickname: str):
        async with self.async_session() as session:
            async with session.begin():
                query = select(User).filter(User.id == user_id)
                result = await session.execute(query)
                user = result.scalars().first()
                user.nickname = nickname
                await session.commit()

    async def set_status(self, user_id: int, status: str):
        async with self.async_session() as session:
            async with session.begin():
                query = select(User).filter(User.id == user_id)
                result = await session.execute(query)
                user = result.scalars().first()
                user.status = status
                await session.commit()

    async def edit_balance(self, user_id: int, amount: float):
        async with self.async_session() as session:
            async with session.begin():
                query = select(User).filter(User.id == user_id)
                result = await session.execute(query)
                user = result.scalars().first()
                balance = round(float(user.balance) + amount, 2)
                user.balance = balance
                await session.commit()

    async def ban_user(self, user_id: int | None = None, username: str | None = None, ban: bool = True):
        async with self.async_session() as session:
            async with session.begin():
                if user_id:
                    query = select(User).filter(User.id == user_id)
                elif username:
                    query = select(User).filter(User.username == username)
                result = await session.execute(query)
                user = result.scalars().first()
                if ban:
                    user.banned = 1
                else:
                    user.banned = 0
                await session.commit()

    async def add_ref(self, user_id: int | str):
        async with self.async_session() as session:
            async with session.begin():
                query = select(User).filter(User.id == int(user_id))
                result = await session.execute(query)
                user = result.scalars().first()
                user.ref_num = user.ref_num + 1
                await session.commit()

    async def get_total_turnover_by_referrer(self, user_id: int | str):
        async with self.async_session() as session:
            async with session.begin():
                query = select(func.sum(User.total_turnover)).filter(User.your_ref == int(user_id))
                result = await session.execute(query)
                total_turnover = result.scalar()
                return total_turnover if total_turnover is not None else 0.00
