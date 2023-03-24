from typing import Union

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message
from cachetools import TTLCache

cache = TTLCache(maxsize=float('inf'), ttl=0.00000001)


class ThrottlingMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Union[Message, CallbackQuery], data):
        user_id = event.from_user.id
        if not cache.get(user_id):
            cache[user_id] = True
            return await handler(event, data)
        else:
            return
