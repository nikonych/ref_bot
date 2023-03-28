from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from sqlalchemy.ext.asyncio import AsyncSession

from misc.states import TokenState
from utils.misc.kb_config import add_money_btn, empty_btn


async def ask_proof_handler(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    user_id = int(call.data.split(":")[1])
    check_type = (await state.get_data()).get('proof')
    inline_keyboard = [
        [InlineKeyboardButton(text=add_money_btn, callback_data=f"add_money:{user_id}:{check_type}"),
         InlineKeyboardButton(text=empty_btn, callback_data=f"empty:{user_id}:{check_type}")],
    ]
    await call.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=inline_keyboard))
    # msg = await call.message.answer("📁 Прикрепите скриншот отчета отработки токенов!")
    # await state.update_data(messages_id=[msg.message_id])
    message_id = call.message.message_id
    await state.update_data(user_id=user_id)
    await state.update_data(message_id=message_id)
    await state.update_data(message_text=call.message.caption)
    # await state.set_state(TokenState.proof)