from typing import Union

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from misc.states import TokenState, WithdrawState


async def ask_withdraw_handler(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    await state.clear()

    message = call.message
    type = call.data.split(":")[1]
    await state.update_data(type=type)
    match type:
        case 'qiwi':
            await message.edit_text("🥝 Введите номер QIWI кошелька:\n"
                                    "⚠️ Пример: 79001234567")
            await state.set_state(WithdrawState.number)
        case 'lzt':
            await message.edit_text("🔗 Введите ссылку на ваш профиль форума LZT:")
            await state.set_state(WithdrawState.link)
        case 'yoomoney':
            await message.edit_text("Введите номер YooMoney кошелька:")
            await state.set_state(WithdrawState.number)
        case 'bank':
            await message.edit_text("Введите номер банковской карты:")
            await state.set_state(WithdrawState.number)

