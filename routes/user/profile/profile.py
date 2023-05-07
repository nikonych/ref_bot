from typing import Union, List

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, InputMedia, InputMediaPhoto, InlineKeyboardButton, \
    InlineKeyboardMarkup
from sqlalchemy.ext.asyncio import AsyncSession

from database.db_commands import DBCommands
from database.models.user import User
from utils.misc.kb_config import withdraw_money_btn, refill_btn


async def back_to_profile_handler(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    await call.message.delete()

    await profile_handler(call, state, session)


async def profile_handler(upd: Union[Message, CallbackQuery], state: FSMContext, session: AsyncSession):
    await state.clear()

    user_id = upd.from_user.id
    message = upd if isinstance(upd, Message) else upd.message

    user_db = await DBCommands(User, session).get(user_id=user_id)

    text = f"ID: {user_db.user_id}\n" \
           f"@{user_db.user_name}\n" \
           f"Registration: {user_db.registration_time}\n" \
           f"Баланс: {user_db.balance}₽\n" \
           f"Refill: {user_db.refill_count}\n" \
           f"Refill_from_referrer: {user_db.refill_from_referrer}\n" \
           f"Referrer count: {user_db.referrer_count}\n" \
           f"Action_date: {user_db.time_to_action}\n"
    inline_keyboard = [
        [InlineKeyboardButton(text=refill_btn, callback_data=f"refill_money"),
         ],
        [InlineKeyboardButton(text=withdraw_money_btn, callback_data=f"withdraw_money"),
         ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    if isinstance(upd, CallbackQuery):
        await message.edit_text(text, reply_markup=keyboard)
    else:
        await message.answer(text, reply_markup=keyboard)



