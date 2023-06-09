import json

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from misc.states import PaymentState
from utils.misc.kb_config import change_yoomoney_btn, check_yoomoney_btn, balance_yoomoney_btn, check_lzt_btn, balance_lzt_btn, change_lzt_btn, change_qiwi_btn, check_qiwi_btn, balance_qiwi_btn




async def change_payment_handler(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    type = call.data.split(":")[1]
    await state.update_data(type=type)
    await call.message.edit_text("Введите token:")
    await state.set_state(PaymentState.token)


async def get_token_handler(message: Message, state: FSMContext, session: AsyncSession, bot: Bot):
    settings = open("database/settings.json", "r")
    with settings as read_file:
        data = json.load(read_file)
    token = message.text
    type = (await state.get_data()).get("type")
    if type == "qiwi":
        data['payments']['qiwi_token'] = token
        await message.answer("Успешно")
    elif type == "lzt":
        data['payments']['lzt_token'] = token
        await message.answer("Введите секректное слово:")
        await state.set_state(PaymentState.secret)
    elif type == "lava":
        data['payments']['lava_token'] = token
        await message.answer("Успешно")
    write_settings = open("database/settings.json", "w")
    with write_settings as write_file:
        json.dump(data, write_file)


async def get_secret_handler(message: Message, state: FSMContext, session: AsyncSession, bot: Bot):

    settings = open("database/settings.json", "r")
    with settings as read_file:
        data = json.load(read_file)
    data['payments']['lzt_secret'] = message.text
    write_settings = open("database/settings.json", "w")
    with write_settings as write_file:
        json.dump(data, write_file)
    await message.answer("Успешно")


