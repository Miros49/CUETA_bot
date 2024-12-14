from dataclasses import dataclass

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from environs import Env


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]


@dataclass
class DatabaseConfig:
    name: str
    host: str
    user: str
    password: str


@dataclass
class Config:
    tg_bot: TgBot
    database: DatabaseConfig


def load_config(path: str | None) -> Config:
    env: Env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN'),
            admin_ids=list(map(int, env.list('ADMIN_IDS')))
        ),
        database=DatabaseConfig(
            name=env('DB_NAME'),
            host=env('DB_HOST'),
            user=env('DB_USER'),
            password=env('DB_PASSWORD'))
    )


config: Config = load_config('.env')

storage = MemoryStorage()
bot: Bot = Bot(token=config.tg_bot.token)
dp: Dispatcher = Dispatcher(storage=storage)
