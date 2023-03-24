from typing import Union

import requests
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from bs4 import BeautifulSoup
from requests.utils import default_headers
from sqlalchemy.ext.asyncio import AsyncSession

from misc.states import TokenState, WithdrawState


async def ask_withdraw_link_handler(message: Message, state: FSMContext, session: AsyncSession):

    await message.answer("Введите ваш username:")
    if message.text.startswith("https://zelenka.guru/members/") or message.text.startswith("https://lolz.guru/members/"):
        await state.update_data(number=message.text.split("/")[-2])
    await state.set_state(WithdrawState.user_name)

async def ask_withdraw_user_name_handler(message: Message, state: FSMContext, session: AsyncSession):
    await message.answer("Введите сумму для вывода:")
    await state.update_data(user_name=message.text)
    await state.set_state(WithdrawState.money)