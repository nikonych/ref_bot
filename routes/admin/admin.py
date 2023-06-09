from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, KeyboardButton, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from database.db_commands import DBCommands
from database.models.user import User
from misc.states import UserState
from utils.misc.kb_config import change_desc_btn, payments_btn, statistic_btn, users_btn, back_btn, change_action_btn


async def admin_menu_handler(message: Message, state: FSMContext, session: AsyncSession):
    await state.clear()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                       keyboard=[
                                           [KeyboardButton(text=change_desc_btn), KeyboardButton(text=payments_btn)],
                                           [KeyboardButton(text=statistic_btn), KeyboardButton(text=users_btn)],
                                           # [KeyboardButton(text=change_action_btn)],
                                           [KeyboardButton(text=back_btn)]
                                       ])
    await message.answer("Админ панель", reply_markup=markup)





