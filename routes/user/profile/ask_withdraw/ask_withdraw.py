from typing import Union

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from misc.states import WithdrawState


async def ask_withdraw_handler(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    await state.clear()

    message = call.message
    type = call.data.split(":")[1]
    await state.update_data(type=type)
    match type:
        case 'qiwi':
            await message.edit_caption(caption="🥝 Введите номер QIWI кошелька:\n"
                                    "⚠️ Пример: 79001234567")
            await state.set_state(WithdrawState.number)
        case 'lzt':
            await message.edit_caption(caption="🔗 Введите ссылку на ваш профиль форума LZT:")
            await state.set_state(WithdrawState.link)
        case 'yoomoney':
            await message.edit_caption(caption="🌐 Введите номер YooMoney кошелька:\n"
                                               "⚠️ Пример: 4100117556672083")
            await state.set_state(WithdrawState.number)
        case 'bank':
            await message.edit_caption(caption="💳 Введите номер Российской банковской карты:\n"
                                               "⚠️ Пример: 4276 1234 5678 9123")
            await state.set_state(WithdrawState.number)
        case 'uk_bank':
            await message.edit_caption(caption="💳 Введите номер Украинской банковской карты:\n"
                                               "⚠️ Пример: 4276 1234 5678 9123")
            await state.set_state(WithdrawState.number)
        case 'lava':
            await message.edit_caption(caption="Введите номер банковской карты:")
            await state.set_state(WithdrawState.number)
        case 'crypto':
            await message.edit_caption(caption="🈳 Введите криптовалюту и кошелек:\n"
                                               "⚠️ Пример: BTC btc20o3ksjeie8e93oejje3i8eie")
            await state.set_state(WithdrawState.number)

