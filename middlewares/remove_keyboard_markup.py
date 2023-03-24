import logging
from typing import Callable, Awaitable, Dict, Any, Union

from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.types import TelegramObject, Message, CallbackQuery, ReplyKeyboardRemove


class RemoveKeyboardMarkupMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: Union[Message, CallbackQuery],
            data: Dict[str, Any],
    ) -> Any:
        has_flag = get_flag(handler=data, name='remove_keyboard_markup')
        if has_flag is True:
            try:
                if isinstance(event, Message):
                    msg = await event.reply('⏳', reply_markup=ReplyKeyboardRemove())
                else:
                    msg = await event.message.reply('⏳', reply_markup=ReplyKeyboardRemove())

                await msg.delete()
            except Exception as e:
                logging.warning(f'RemoveKeyboardMarkupMiddleware exception: {e}')

        return await handler(event, data)
