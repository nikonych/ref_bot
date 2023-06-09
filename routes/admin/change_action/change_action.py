import json

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from misc.states import ChangeState
from utils.misc.kb_config import change_day_action_price_btn, change_day_action_name_btn, change_day_action_description_btn, change_week_action_price_btn, change_week_action_name_btn, change_week_action_description_btn, change_month_action_name_btn, change_month_action_description_btn, change_month_action_price_btn


async def change_handler(message: Message, state: FSMContext, session: AsyncSession):
    await state.clear()
    inline_keyboard = [
        [InlineKeyboardButton(text=change_day_action_price_btn, callback_data=f"change_action_price:day"), InlineKeyboardButton(text=change_day_action_name_btn, callback_data=f"change_action_name:day"), InlineKeyboardButton(text=change_day_action_description_btn, callback_data=f"change_action_description:day")],
        [InlineKeyboardButton(text=change_week_action_price_btn, callback_data=f"change_action_price:week"), InlineKeyboardButton(text=change_week_action_name_btn, callback_data=f"change_action_name:week"), InlineKeyboardButton(text=change_week_action_description_btn, callback_data=f"change_action_description:week")],
        [InlineKeyboardButton(text=change_month_action_price_btn, callback_data=f"change_action_price:month"), InlineKeyboardButton(text=change_month_action_name_btn, callback_data=f"change_action_name:month"), InlineKeyboardButton(text=change_month_action_description_btn, callback_data=f"change_action_description:month")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    await message.answer(".", reply_markup=keyboard)


async def change_name(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    await state.clear()

    await state.update_data(type=call.data.split(":")[1])
    await call.message.answer("Отправьте новый текст")

    await state.set_state(ChangeState.new_action_name)


async def get_name(message: Message, state: FSMContext, session: AsyncSession, bot: Bot):
    type_img = (await state.get_data()).get("type")
    settings = open("database/settings.json", "r")
    with settings as read_file:
        data = json.load(read_file)
    match type_img:
        case "day":
            data['actions'][0]['name'] = message.text
        case "week":
            data['actions'][1]['name'] = message.text
        case "month":
            data['actions'][2]['name'] = message.text
    write_settings = open("database/settings.json", "w")
    with write_settings as write_file:
        json.dump(data, write_file)
    await message.answer("Успешно")


async def change_description(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    await state.clear()

    await state.update_data(type=call.data.split(":")[1])
    await call.message.answer("Отправьте новый текст")

    await state.set_state(ChangeState.new_action_description)


async def get_description(message: Message, state: FSMContext, session: AsyncSession, bot: Bot):
    type_img = (await state.get_data()).get("type")
    settings = open("database/settings.json", "r")
    with settings as read_file:
        data = json.load(read_file)
    print(message.text)
    print(data['actions'][0]['description'])
    match type_img:
        case "day":
            data['actions'][0]['description'] = message.text
        case "week":
            data['actions'][1]['description'] = message.text
        case "month":
            data['actions'][2]['description'] = message.text
    write_settings = open("database/settings.json", "w")
    with write_settings as write_file:
        json.dump(data, write_file)
    await message.answer("Успешно")

async def change_price(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    await state.clear()

    await state.update_data(type=call.data.split(":")[1])
    await call.message.answer("Отправьте новый текст")

    await state.set_state(ChangeState.new_action_price)


async def get_price(message: Message, state: FSMContext, session: AsyncSession, bot: Bot):
    type_img = (await state.get_data()).get("type")
    settings = open("database/settings.json", "r")
    with settings as read_file:
        data = json.load(read_file)
    match type_img:
        case "day":
            data['actions'][0]['price'] = int(message.text)
        case "week":
            data['actions'][1]['price'] = int(message.text)
        case "month":
            data['actions'][2]['price'] = int(message.text)
    write_settings = open("database/settings.json", "w")
    with write_settings as write_file:
        json.dump(data, write_file)
    await message.answer("Успешно")