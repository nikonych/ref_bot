from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy.ext.asyncio import AsyncSession

from utils.misc.kb_config import yes_btn, no_btn, add_money_btn, empty_btn, send_proof_btn


async def empty_token_handler(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    user_id = call.from_user.id
    message = call.message
    check_type = call.data.split(":")[2]
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=yes_btn, callback_data=f"sure:yes:{user_id}:{check_type}"),
         InlineKeyboardButton(text=no_btn, callback_data=f"sure:no:{user_id}:{check_type}")]
    ])
    msg = await call.message.edit_caption(caption=call.message.caption + "\n\n"
                                                                   "Вы уверены что токены пустые?",
                                    reply_markup=keyboard)
    await state.update_data(messages_id=[msg.message_id])



