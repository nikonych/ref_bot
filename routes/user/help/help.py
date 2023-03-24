import json
from typing import Union, List

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, InputMedia, InputMediaPhoto, InlineKeyboardButton, \
    InlineKeyboardMarkup, FSInputFile
from sqlalchemy.ext.asyncio import AsyncSession

from database.db_commands import DBCommands
from database.models.user import User
from utils.misc.kb_config import  help_chat_btn


async def help_handler(message: Message, state: FSMContext, session: AsyncSession):
    await state.clear()

    user_id = message.from_user.id
    with open("database/settings.json", "r") as read_file:
        data = json.load(read_file)
    user_db = await DBCommands(User, session).get(user_id=user_id)
    inline_keyboard = [
        [InlineKeyboardButton(text=help_chat_btn, url=data['help_url']),
         ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    img = FSInputFile('./images/help_img.jpg')
    await message.answer_photo(img, caption=data['help_text'], reply_markup=keyboard)



