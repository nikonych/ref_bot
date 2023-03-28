from typing import Union

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from misc.states import TokenState


async def upload_handler(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    await state.clear()

    user_id = call.from_user.id
    message = call.message
    await state.update_data(proof=call.data.split(":")[1])

    await message.edit_text("🔗 Загрузите файл в \"txt\" формате!\n"
                         "⚠️ Токены должны быть загружены без лишней информации, в чистом виде!")
    await state.set_state(TokenState.file)
