from typing import List

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from datetime import date

from . import User, Event, Registration, BeerPongTeam

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

    async def get_event(self, event_id: int) -> Event:
        async with self.async_session() as session:
            async with session.begin():
                query = select(Event).where(Event.id == event_id)
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

    # Registration

    async def create_registration(self, event_id: int, user_id: int) -> int:
        async with self.async_session() as session:
            async with session.begin():
                registration = Registration(event_id=event_id, user_id=user_id)
                session.add(registration)
                await session.commit()

                return registration.id

    async def check_registration(self, event_id: int, user_id: int) -> Registration:
        async with self.async_session() as session:
            async with session.begin():
                query = select(Registration).where(
                    Registration.event_id == event_id and Registration.user_id == user_id
                )
                result = await session.execute(query)
                registration = result.scalars().first()

                return registration

    # BeerPong 25.12.2024

    async def create_team(self, player_1_id: int, player_1_username: str, player_2_id: int,
                          player_2_username: str) -> int:
        async with self.async_session() as session:
            async with session.begin():
                team = BeerPongTeam(
                    player_1_id=player_1_id, player_1_username=player_1_username,
                    player_2_id=player_2_id, player_2_username=player_2_username,
                    status=True, created_manually=True
                )
                session.add(team)
                await session.commit()
                return team.id

    async def join_team(self, player_id: int, player_username: str) -> BeerPongTeam | None:
        async with self.async_session() as session:
            async with session.begin():
                query = session.query(BeerPongTeam).where(not BeerPongTeam.status)
                result = await session.execute(query)
                team = result.scalars().first()

                if not team:
                    team = BeerPongTeam(
                        player_1_id=player_id, player_1_username=player_username, status=False, created_manually=False
                    )
                    session.add(team)
                    await session.commit()
                    return None

                team.player_2_id = player_id
                team.player_2_username = player_username
                team.status = True
                await session.commit()

                return team
