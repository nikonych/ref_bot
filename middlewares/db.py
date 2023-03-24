from typing import Callable, Awaitable, Dict, Any, Union

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, CallbackQuery, Message


class DBSessionMiddleware(BaseMiddleware):
    def __init__(self, engine, session_pool):
        super().__init__()
        self.engine = engine
        self.session_pool = session_pool

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: Union[Message, CallbackQuery],
            data: Dict[str, Any],
    ) -> Any:
        async with self.session_pool() as session:
            data["engine"] = self.engine
            data["session"] = session
            return await handler(event, data)
