import pandas as pd

from typing import List
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from datetime import date, datetime, timedelta

from . import User, Event, Registration, BeerPongTeam, FundRaiser

Base = declarative_base()


class DataBase:
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.engine = create_async_engine(self.database_url, echo=False)
        self.async_session = async_sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)

    async def create_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    # -------------------------------   USER   -------------------------------

    async def init_user(self, user_id: int, username: str | None):
        async with self.async_session() as session:
            async with session.begin():
                user = User(id=user_id, username=username if username else None)
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

    def is_user_adult(self, date_of_birth: date) -> bool:
        """
        Проверяет, исполнилось ли пользователю 18 лет.
        :param date_of_birth: Дата рождения пользователя.
        :return: True, если пользователю есть 18 лет, иначе False.
        """
        today = date.today()
        age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
        return age >= 18

    # # -------------------------------   ADMIN   -------------------------------
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

    # -------------------------------   EVENT   -------------------------------

    async def create_event(self, name: str, description: str, event_date: date, photo_id: str | None):
        all_events = await self.get_upcoming_events()

        for event in all_events:  # Check for duplicate event
            if event["name"] == name and event["date"] == event_date:
                raise ValueError(f'An event with name "{name}" on {event_date} already exists.')
        async with self.async_session() as session:
            async with session.begin():
                new_event = Event(name=name, description=description, date=event_date, photo_id=photo_id)
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

    async def get_upcoming_events(self) -> List[dict]:
        current_time = datetime.utcnow() + timedelta(hours=3)

        async with self.async_session() as session:
            async with session.begin():
                # Фильтрация мероприятий, которые еще не прошли
                query = select(Event).where(Event.date > current_time)
                result = await session.execute(query)
                events = result.scalars().all()

                return [
                    {"id": event.id, "name": event.name, "description": event.description, "date": event.date}
                    for event in events
                ]

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

    # -------------------------------    Registration   -------------------------------

    async def create_registration(self, event_id: int, user_id: int, username: str | None, registration_wave: int,
                                  registration_type: str, fundraiser_id: int, status: str) -> int:
        async with self.async_session() as session:
            async with session.begin():
                registration: Registration = Registration(
                    event_id=event_id,
                    user_id=user_id,
                    username=username,
                    registration_wave=registration_wave,
                    registration_type=registration_type,
                    fundraiser_id=fundraiser_id,
                    status=status
                )
                session.add(registration)
                await session.commit()

                return registration.id

    async def get_registration(self, event_id: int, user_id: int) -> Registration:
        async with self.async_session() as session:
            async with session.begin():
                query = select(Registration).where(
                    (Registration.event_id == event_id) & (Registration.user_id == user_id)
                )
                result = await session.execute(query)
                registration = result.scalars().first()

                return registration

    async def get_registration_by_id(self, registration_id: int) -> Registration | None:
        """
        Возвращает запись о регистрации по ID.
        :param registration_id: ID регистрации.
        :return: Объект Registration, если запись найдена, иначе None.
        """
        async with self.async_session() as session:
            async with session.begin():
                query = select(Registration).where(Registration.id == registration_id)
                result = await session.execute(query)
                registration = result.scalars().first()
                return registration

    async def remove_registration(self, event_id: int, user_id: int) -> bool:
        """
        Снимает регистрацию пользователя с определённого события.
        Возвращает True, если удаление прошло успешно, иначе False.
        """
        async with self.async_session() as session:
            async with session.begin():
                # Запрос на поиск регистрации пользователя для события
                query = select(Registration).where(
                    (Registration.event_id == event_id) & (Registration.user_id == user_id)
                )
                result = await session.execute(query)
                registration = result.scalars().first()

                # Если регистрация найдена, удаляем её
                if registration:
                    await session.delete(registration)
                    await session.commit()
                    return True

                return False

    async def get_all_registrations(self, event_id: int) -> List[Registration]:
        async with self.async_session() as session:
            async with session.begin():
                query = select(Registration).where(Registration.event_id == event_id)
                result = await session.execute(query)
                registrations = result.scalars().all()

                return [registration for registration in registrations]

    async def update_registration_status(self, registration_id: int, new_status: str):
        """
        Изменяет статус указанной регистрации.
        :param registration_id: ID регистрации.
        :param new_status: Новый статус для регистрации.
        """
        async with self.async_session() as session:
            async with session.begin():
                query = select(Registration).where(Registration.id == registration_id)
                result = await session.execute(query)
                registration = result.scalars().first()

                if registration:
                    registration.status = new_status
                    await session.commit()
                else:
                    raise ValueError(f"Регистрация с ID {registration_id} не найдена.")

    async def assign_fundraiser_to_registration(self, registration_id: int, fundraiser_id: int):
        """
        Устанавливает указанный fundraiser_id для конкретной регистрации.
        """
        async with self.async_session() as session:
            async with session.begin():
                query = select(Registration).where(Registration.id == registration_id)
                result = await session.execute(query)
                registration = result.scalars().first()
                if registration:
                    registration.fundraiser_id = fundraiser_id
                    await session.commit()
                else:
                    raise ValueError(f"Регистрация с ID {registration_id} не найдена.")

    async def set_first_warning(self, registration_id: int):
        """
        Устанавливает текущее дата и время в поле `first_warning` для указанной регистрации.
        :param registration_id: ID регистрации.
        """
        async with self.async_session() as session:
            async with session.begin():
                query = select(Registration).where(Registration.id == registration_id)
                result = await session.execute(query)
                registration = result.scalars().first()

                if registration:
                    current_datetime = (datetime.utcnow() + timedelta(hours=3)).strftime("%d.%m.%Y %H:%M:%S")
                    registration.first_warning = current_datetime
                    await session.commit()
                else:
                    raise ValueError(f"Регистрация с ID {registration_id} не найдена.")

    # -------------------------------   BeerPong 25.12.2024   -------------------------------

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

    async def check_team_limit(self) -> bool:
        async with self.async_session() as session:
            async with session.begin():
                # Считаем количество строк в таблице BeerPongTeam
                query = select(func.count()).select_from(BeerPongTeam)
                result = await session.execute(query)
                count = result.scalar()

                return count <= 16

    async def join_team(self, player_id: int, player_username: str) -> BeerPongTeam | None:
        async with self.async_session() as session:
            async with session.begin():
                # Ищем команду, у которой status равен False
                query = select(BeerPongTeam).where(BeerPongTeam.status == False)
                result = await session.execute(query)
                team = result.scalars().first()

                if team:
                    # Если неполная команда найдена, заполняем второго игрока
                    team.player_2_id = player_id
                    team.player_2_username = player_username
                    team.status = True
                    await session.commit()
                    return team
                else:
                    # Если неполной команды нет, создаём новую с первым игроком
                    new_team = BeerPongTeam(
                        player_1_id=player_id,
                        player_1_username=player_username,
                        status=False,
                        created_manually=False
                    )
                    session.add(new_team)
                    await session.commit()
                    return None

    async def get_event_registrations(self, event_id: int) -> List[User]:
        async with self.async_session() as session:
            async with session.begin():
                query = select(Registration).where(Registration.event_id == event_id)
                result = await session.execute(query)
                return list(set([user.user_id for user in result.scalars().all()]))

    async def is_user_in_team(self, user_id: int) -> bool:
        """
        Проверяет, состоит ли пользователь в какой-либо команде.
        Возвращает True, если пользователь найден в одной из команд.
        """
        async with self.async_session() as session:
            async with session.begin():
                # Запрос на поиск пользователя в качестве player_1 или player_2
                query = select(BeerPongTeam).where(
                    (BeerPongTeam.player_1_id == user_id) | (BeerPongTeam.player_2_id == user_id)
                )
                result = await session.execute(query)
                team = result.scalars().first()

                return team is not None

    async def generate_registration_report(self, event_id: int) -> str:
        async with self.async_session() as session:
            async with session.begin():
                # Запрос всех зарегистрированных пользователей на событие
                query = select(
                    User.id,
                    User.username,
                    User.name,
                    User.status,
                    User.phone_number,
                    User.date_of_birth,
                    BeerPongTeam.player_1_username,
                    BeerPongTeam.player_2_username
                ).join(
                    Registration, User.id == Registration.user_id
                ).outerjoin(
                    BeerPongTeam, (User.id == BeerPongTeam.player_1_id) | (User.id == BeerPongTeam.player_2_id)
                ).where(
                    Registration.event_id == event_id
                )

                result = await session.execute(query)
                rows = result.all()

                data = []
                for row in rows:
                    user_in_team = row.player_1_username if row.player_1_username == row.username else row.player_2_username
                    teammate = row.player_2_username if row.player_1_username == row.username else row.player_1_username

                    if user_in_team:
                        data.append({
                            'Username': f'@{row.username}',
                            'ФИО': row.name,
                            'Статус': row.status,
                            'Номер телефона': row.phone_number,
                            'Дата рождения': row.date_of_birth,
                            'Участвует в бир-понге': 'ДА' if user_in_team else 'НЕТ',
                            'Напарник': teammate if teammate else 'N/A'
                        })

                # Создаем Excel
                df = pd.DataFrame(data)
                file_path = f'BeerPong_registrations.xlsx'
                df.to_excel(file_path, index=False)

                with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
                    df.to_excel(writer, index=False, sheet_name='Registrations')
                    worksheet = writer.sheets['Registrations']

                    # Автоматическая настройка ширины столбцов
                    for idx, col in enumerate(df.columns):
                        max_len = df[col].astype(str).map(len).max() + 2
                        worksheet.set_column(idx, idx, max_len)

                return file_path

    # -------------------------------   FUNDRAISER   -------------------------------

    async def get_fundraiser(self, fundraiser_id: int) -> FundRaiser | None:
        """
        Ищет сборщика по id.
        :param fundraiser_id: id сборщика.
        :return: Объект FundRaiser, если найден, иначе None.
        """
        async with self.async_session() as session:
            async with session.begin():
                query = select(FundRaiser).where(FundRaiser.id == fundraiser_id)
                result = await session.execute(query)
                return result.scalars().first()

    async def get_all_fundraisers(self) -> list[FundRaiser]:
        """
        Возвращает список всех сборщиков.
        :return: Список объектов FundRaiser.
        """
        async with self.async_session() as session:
            async with session.begin():
                query = select(FundRaiser)
                result = await session.execute(query)
                return result.scalars().all()

    async def get_fundraiser_with_least_registrations(self) -> FundRaiser | None:
        """
        Возвращает сборщика с наименьшим числом number_of_registrations,
        учитывая только тех, у кого статус True (свободен).
        """
        async with self.async_session() as session:
            async with session.begin():
                query = select(FundRaiser).where(FundRaiser.status == True).order_by(FundRaiser.number_of_registrations)
                result = await session.execute(query)
                return result.scalars().first()

    async def increment_registration_count(self, fundraiser_id: int):
        """Добавляет в поле number_of_registrations одну регистрацию."""
        async with self.async_session() as session:
            async with session.begin():
                query = select(FundRaiser).where(FundRaiser.id == fundraiser_id)
                result = await session.execute(query)
                fundraiser = result.scalars().first()
                if fundraiser:
                    fundraiser.number_of_registrations += 1
                    await session.commit()
                else:
                    raise ValueError(f"Fundraiser с ID {fundraiser_id} не найден.")

    async def decrement_registration_and_increment_verification(self, fundraiser_id: int):
        """
        Удаляет одну регистрацию из number_of_registrations и добавляет одну в waiting_for_verification.
        """
        async with self.async_session() as session:
            async with session.begin():
                query = select(FundRaiser).where(FundRaiser.id == fundraiser_id)
                result = await session.execute(query)
                fundraiser = result.scalars().first()
                if fundraiser:
                    if fundraiser.number_of_registrations > 0:
                        fundraiser.number_of_registrations -= 1
                        fundraiser.waiting_for_verification += 1
                        await session.commit()
                    else:
                        raise ValueError("Нет доступных регистраций для удаления.")
                else:
                    raise ValueError(f"Fundraiser с ID {fundraiser_id} не найден.")

    async def move_verification_to_verified(self, fundraiser_id: int):
        """
        Удаляет одну запись из waiting_for_verification и добавляет одну в verified.
        """
        async with self.async_session() as session:
            async with session.begin():
                query = select(FundRaiser).where(FundRaiser.id == fundraiser_id)
                result = await session.execute(query)
                fundraiser = result.scalars().first()
                if fundraiser:
                    if fundraiser.waiting_for_verification > 0:
                        fundraiser.waiting_for_verification -= 1
                        fundraiser.verified += 1
                        await session.commit()
                    else:
                        raise ValueError("Нет записей в ожидании подтверждения для перемещения.")
                else:
                    raise ValueError(f"Fundraiser с ID {fundraiser_id} не найден.")
