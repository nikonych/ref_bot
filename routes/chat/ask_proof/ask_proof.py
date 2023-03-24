from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from misc.states import TokenState


async def ask_proof_handler(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    user_id = int(call.data.split(":")[1])
    msg = await call.message.answer("Отправьте фотографии с отчетом и сумму")
    await state.update_data(messages_id=[msg.message_id])
    message_id = call.message.message_id
    await state.update_data(user_id=user_id)
    await state.update_data(message_id=message_id)
    await state.update_data(message_text=call.message.caption)
    await state.set_state(TokenState.proof)