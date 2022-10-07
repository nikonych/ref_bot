# - *- coding: utf- 8 - *-
from aiogram.types import Update

from loader import dp
from utils.misc.bot_logging import bot_logger


# Обработка телеграм ошибок
@dp.errors_handler()
async def all_errors(update: Update, exception):
    get_data = None

    if "'NoneType' object is not subscriptable" in str(exception):
        if "callback_query" in update:
            get_data = update.callback_query.data

    if get_data is not None:
        split_data = get_data.split(":")


    bot_logger.exception(
        f"Exception: {exception}\n"
        f"Update: {update}"
    )
