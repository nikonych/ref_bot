from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from utils.payments import qiwi, lzt


async def check_payment_handler(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    payment_type = call.data.split(":")[1]
    if payment_type == "qiwi":
        await qiwi.check_qiwi(call)
    if payment_type == "lzt":
        await lzt.check_lzt(call)

