import json

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from misc.states import ChangeState
from utils.misc.kb_config import change_rule_url_btn, change_rule_img_btn, change_rule_text_btn, change_help_img_btn, change_help_text_btn, change_help_user_btn, change_main_img_btn, change_main_text_btn

async def change_img(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    await state.clear()

    await state.update_data(type=call.data.split(":")[1])
    await call.message.answer("Отправьте новую фотографию")

    await state.set_state(ChangeState.new_img)


async def get_img(message: Message, state: FSMContext, session: AsyncSession, bot: Bot):
    type_img = (await state.get_data()).get("type")
    match type_img:
        case "main":
            await bot.download(message.photo[-1].file_id, './images/main_img.jpg')
            # await message.photo[-1].download('./images/main_img.jpg')
        case "help":
            await bot.download(message.photo[-1].file_id, './images/help_img.jpg')
        case "rule":
            await bot.download(message.photo[-1].file_id, './images/rule_img.jpg')
    await message.answer("Успешно")


