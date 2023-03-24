from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from sqlalchemy.ext.asyncio import AsyncSession

from utils.misc.kb_config import qiwi_btn, lolz_btn, yoomoney_btn, bank_card_btn, back_btn


async def choose_withdraw_handler(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    await state.clear()
    user_id = call.from_user.id
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=qiwi_btn, callback_data=f"choose_withdraw:qiwi")],
        [InlineKeyboardButton(text=lolz_btn, callback_data=f"choose_withdraw:lzt")],
        # [InlineKeyboardButton(text=yoomoney_btn, callback_data=f"choose_withdraw:yoomoney")],
        [InlineKeyboardButton(text=bank_card_btn, callback_data=f"choose_withdraw:bank")],
        [InlineKeyboardButton(text=back_btn, callback_data=f"back_profile")],
    ])
    await call.message.edit_text(call.message.text + "\n\n"
                                                     "Выбери кошелек для вывода средств:", reply_markup=keyboard)
