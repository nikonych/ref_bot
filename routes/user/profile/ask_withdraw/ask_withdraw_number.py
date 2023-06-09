from typing import Union

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from misc.states import WithdrawState


async def ask_withdraw_number_handler(message: Message, state: FSMContext, session: AsyncSession):

    await message.answer("💳 Введите сумму для вывода:")
    await state.update_data(number=message.text)
    await state.set_state(WithdrawState.money)

