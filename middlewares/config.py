from typing import Callable, Awaitable, Dict, Any, Union

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, CallbackQuery, Message

from config import Config


class ConfigMiddleware(BaseMiddleware):
    def __init__(self, config: Config):
        super().__init__()
        self.config = config

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: Union[Message, CallbackQuery],
            data: Dict[str, Any],
    ) -> Any:
        data["config"] = self.config

        return await handler(event, data)
