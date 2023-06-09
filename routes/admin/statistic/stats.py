import json

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from database.db_commands import DBCommands
from database.models.user import User


async def statistics_handler(message: Message, state: FSMContext, session: AsyncSession, bot: Bot):

    users = await DBCommands(User, session).get(_first=False)
    user_count = 0
    withdraw_count = 0
    balance_count = 0
    for user in users:
        user_count += 1
        withdraw_count += int(user.withdraw_balance)
        balance_count += int(user.balance)
    text = f"🌍 <b>Статистика:</b>\n\n" \
           f"👯 Пользователей: <b>{user_count}</b>\n" \
           f"💰 Сумма общей выплаты: <b>{withdraw_count}</b>\n" \
           f"🤑 Общий баланс: <b>{balance_count}</b>\n"

    await message.answer(text)


