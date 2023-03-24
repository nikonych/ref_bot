from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from misc.states import TokenState


async def ask_balance_handler(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    user_id = int(call.data.split(":")[1])
    message_id = call.message.message_id
    msg = await call.message.answer("Введите сумму")
    await state.update_data(messages_id=[msg.message_id])
    await state.update_data(user_id=user_id)
    await state.update_data(message_id=message_id)
    await state.update_data(message_text=call.message.caption)
    await state.set_state(TokenState.money)