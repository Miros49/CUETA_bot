from typing import List

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from datetime import date

from . import User, Event, Registration

Base = declarative_base()


class DataBase:
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.engine = create_async_engine(self.database_url, echo=False)
        self.async_session = async_sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)

    async def create_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    # USER

    async def init_user(self, user_id: int, username: str):
        async with self.async_session() as session:
            async with session.begin():
                user = User(id=user_id, username=username)
                session.add(user)
                await session.commit()
                return user.id

    async def get_user(self, user_id: int) -> User:
        async with self.async_session() as session:
            async with session.begin():
                query = select(User).where(User.id == user_id)
                result = await session.execute(query)
                user = result.scalars().first()
                return user

    async def user_exists(self, user_id: int) -> bool:
        async with self.async_session() as session:
            async with session.begin():
                query = select(User).where(User.id == user_id)
                result = await session.execute(query)
                user = result.scalars().first()
                return True if user else False

    async def get_all_users(self) -> List[User]:
        async with self.async_session() as session:
            async with session.begin():
                query = select(User)
                result = await session.execute(query)
                return [user for user in result.scalars().all()]

    async def toggle_user_notifications(self, user_id: int, notifications: bool):
        async with self.async_session() as session:
            async with session.begin():
                query = select(User).where(User.id == user_id)
                result = await session.execute(query)
                user = result.scalars().first()

                if user:
                    user.allow_notifications = notifications
                    await session.commit()
                else:
                    raise ValueError(f"Пользователь с id {user_id} не найден")

    async def set_user(self, user_id: int, name: str, date_of_birth: date, status: str, phone_number: str):
        async with self.async_session() as session:
            async with session.begin():
                query = select(User).where(User.id == user_id)
                result = await session.execute(query)
                user = result.scalars().first()
                user.name = name
                user.date_of_birth = date_of_birth
                user.status = status
                user.phone_number = phone_number
                await session.commit()

    async def get_users_for_mailing(self):
        async with self.async_session() as session:
            async with session.begin():
                query = select(User).where(User.allow_notifications)
                result = await session.execute(query)
                user_ids = [user.id for user in result.scalars().all()]
                return user_ids

    # # ADMIN
    #
    # async def get_admins_ids(self):
    #     async with self.async_session() as session:
    #         async with session.begin():
    #             query = select(Admin)
    #             result = await session.execute(query)
    #             admin_ids = [admin.id for admin in result.scalars().all()]
    #             return admin_ids
    #
    # async def get_admin(self, admin_id: int):
    #     async with self.async_session() as session:
    #         async with session.begin():
    #             query = select(Admin).where(Admin.id == admin_id)
    #             result = await session.execute(query)
    #             admin = result.scalars().first()
    #             return admin
    #
    # async def add_admin(self, admin_id: int):
    #     async with self.async_session() as session:
    #         async with session.begin():
    #             admin = User(id=admin_id)
    #             session.add(admin)
    #             return await session.commit()
    #
    # async def get_admins(self):
    #     async with self.async_session() as session:
    #         async with session.begin():
    #             query = select(Admin)
    #             result = await session.execute(query)
    #             admins = result.scalars().all()
    #             return admins
    #
    # async def delete_admin(self, admin_id: int):
    #     async with self.async_session() as session:
    #         async with session.begin():
    #             query = select(Admin).where(Admin.id == admin_id)
    #             result = await session.execute(query)
    #             admin = result.scalars().first()
    #             if admin:
    #                 await session.delete(admin)
    #                 await session.commit()
    #                 return True

    # EVENT

    async def create_event(self, name: str, description: str, event_date: date):
        all_events = await self.get_all_events()

        for event in all_events:  # Check for duplicate event
            if event["name"] == name and event["date"] == event_date:
                raise ValueError(f'An event with name "{name}" on {event_date} already exists.')
        async with self.async_session() as session:
            async with session.begin():
                new_event = Event(name=name, description=description, date=event_date)
                session.add(new_event)
                await session.commit()
                return new_event.id

    async def get_event(self, event_id: int | str) -> Event:
        async with self.async_session() as session:
            async with session.begin():
                query = select(Event).where(Event.id == int(event_id))
                result = await session.execute(query)
                event = result.scalars().first()
                return event

    async def get_all_events(self) -> List[dict]:
        async with self.async_session() as session:
            async with session.begin():
                query = select(Event)
                result = await session.execute(query)
                events = result.scalars().all()

                return [
                    {"id": event.id, "name": event.name, "date": event.date}
                    for event in events
                ]
