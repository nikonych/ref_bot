from typing import Union

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, \
    InlineKeyboardButton
from sqlalchemy.ext.asyncio import AsyncSession

from utils.misc.kb_config import full_info_btn, no_info_btn


async def back_to_tokens_handler(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    await call.message.delete()

    await tokens_handler(call, state, session)


async def tokens_handler(upd: Union[Message, CallbackQuery], state: FSMContext, session: AsyncSession):
    await state.clear()

    user_id = upd.from_user.id
    message = upd if isinstance(upd, Message) else upd.message
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=full_info_btn, callback_data=f"send_txt:yes")],
        [InlineKeyboardButton(text=no_info_btn, callback_data=f"send_txt:no")]
    ])

    await message.answer("Как вы хотите отработать ваши токены?", reply_markup=keyboard)
