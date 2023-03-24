import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from config import Config, load_config
from database.base import Base
from middlewares.AlbumMiddleware import AlbumMiddleware
from middlewares.config import ConfigMiddleware
from middlewares.db import DBSessionMiddleware
from middlewares.remove_keyboard_markup import RemoveKeyboardMarkupMiddleware
from middlewares.throttling import ThrottlingMiddleware
# from misc.bot_commands import set_commands
# from misc.services import run_services
from routes import register_all_routes

logger = logging.getLogger(__name__)


async def main():
    config: Config = load_config('.env')

    engine = create_async_engine(f'sqlite+aiosqlite:///database/database.db',
                                 future=True)  # echo=False
    # creating DB connections pool
    session_pool = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # creating bot
    # session = AiohttpSession(
    #     api=TelegramAPIServer.from_base('http://telegram-bot-api:8081', is_local=True),
    # )
    # bot = Bot(token=config.tg_bot.token, parse_mode='HTML', session=session)
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')

    # await run_services(bot, config, session_pool)

    # storage = RedisStorage.from_url(f"redis://{config.redis.host}:{config.redis.port}") if config.tg_bot.use_redis else MemoryStorage()
    dp = Dispatcher(storage=MemoryStorage())
    #
    # # register middlewares
    dp.message.middleware(ThrottlingMiddleware())
    dp.callback_query.middleware(ThrottlingMiddleware())
    #
    dp.message.middleware(AlbumMiddleware())
    # dp.callback_query.middleware(AlbumMiddleware())
    #
    dp.message.middleware(DBSessionMiddleware(engine, session_pool))
    dp.callback_query.middleware(DBSessionMiddleware(engine, session_pool))
    #
    dp.message.middleware(ConfigMiddleware(config))
    dp.callback_query.middleware(ConfigMiddleware(config))
    #
    dp.message.middleware(RemoveKeyboardMarkupMiddleware())
    dp.callback_query.middleware(RemoveKeyboardMarkupMiddleware())
    #
    # # register all routes
    register_all_routes(dp, config)
    #
    # # set all bot commands
    # await set_commands(bot, config)
    #
    try:
        logger.info('Starting bot')
        await bot.get_updates(offset=-1)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        # await storage.close()
        await bot.session.close()
