import asyncio
import logging

from core import dp, bot

from database import db
from handlers import user_handlers, admin_handlers, fundraiser_handlers


logging.basicConfig(level=logging.INFO)


async def main() -> None:
    # await db.add_missing_columns()
    await db.create_tables()

    dp.include_router(user_handlers.router)
    dp.include_router(admin_handlers.router)
    dp.include_router(fundraiser_handlers.router)

    await bot.delete_webhook(drop_pending_updates=False)

    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
