from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from sqlalchemy.ext.asyncio import AsyncSession

from utils.misc.kb_config import change_yoomoney_btn, check_yoomoney_btn, check_lzt_btn, change_lzt_btn, \
    change_qiwi_btn, check_qiwi_btn


async def payments_handler(message: Message, state: FSMContext, session: AsyncSession, bot: Bot):
    inline_keyboard = [
        [InlineKeyboardButton(text=check_qiwi_btn, callback_data="check_payment:qiwi"),
         InlineKeyboardButton(text=change_qiwi_btn, callback_data="change_payment:qiwi"), ],
        [InlineKeyboardButton(text=check_lzt_btn, callback_data="check_payment:lzt"),
         InlineKeyboardButton(text=change_lzt_btn, callback_data="change_payment:lzt"), ],
        # [InlineKeyboardButton(text=check_yoomoney_btn, callback_data="check_payment:yoomoney"),
        #  InlineKeyboardButton(text=change_yoomoney_btn, callback_data="change_payment:yoomoney"), ],

    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    await message.answer("Выберите опцию", reply_markup=keyboard)
