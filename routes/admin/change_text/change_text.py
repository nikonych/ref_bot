import json

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from misc.states import ChangeState
from utils.misc.kb_config import change_rule_url_btn, change_rule_img_btn, change_rule_text_btn, change_help_img_btn, change_help_text_btn, change_help_user_btn, change_main_img_btn, change_main_text_btn

async def change_text(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    await state.clear()

    await state.update_data(type=call.data.split(":")[1])
    await call.message.answer("Отправьте новый текст")

    await state.set_state(ChangeState.new_text)


async def get_text(message: Message, state: FSMContext, session: AsyncSession, bot: Bot):
    type_img = (await state.get_data()).get("type")
    settings = open("database/settings.json", "r")
    with settings as read_file:
        data = json.load(read_file)
    match type_img:
        case "main":
            data['main_text'] = message.text
        case "help":
            data['help_text'] = message.text
        case "rule":
            data['about_us_text'] = message.text
        case "info":
            data['information_text'] = message.text
        case "license":
            data['license'] = message.text
    write_settings = open("database/settings.json", "w")
    with write_settings as write_file:
        json.dump(data, write_file)
    await message.answer("Успешно")


