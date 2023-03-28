import json
from typing import Union

from aiogram import types
from aiogram.filters import CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, KeyboardButton, FSInputFile
from sqlalchemy.ext.asyncio import AsyncSession

from database.db_commands import DBCommands
from database.models.user import User
from config import Config
from utils.misc.kb_config import *

async def back_to_start_handler(message: Message, state: FSMContext, session: AsyncSession, config: Config):

    await start_handler(message, state, session, config)




async def start_handler(upd: Union[Message, CallbackQuery], state: FSMContext, session: AsyncSession, config: Config, command: CommandObject = None):
    await state.clear()

    user_id = upd.from_user.id
    message = upd if isinstance(upd, Message) else upd.message

    user_db = await DBCommands(User, session).get(user_id=user_id)
    if not user_db:
        await DBCommands(User, session).add(user_id=user_id, user_name=upd.from_user.username)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                       keyboard=[
                                           [KeyboardButton(text=load_token_btn)],
                                           [KeyboardButton(text=profile_btn), KeyboardButton(text=rule_btn)],
                                           [KeyboardButton(text=help_btn)]
                                       ])

    if user_id in config.tg_bot.admin_ids:
        markup.keyboard.append([KeyboardButton(text=admin_btn)])
    with open("database/settings.json", "r") as read_file:
        data = json.load(read_file)
    img = FSInputFile('./images/main_img.jpg')
    if "{0}" in data['main_text']:
        await message.answer_photo(img, caption=data['main_text'].format(message.from_user.username), reply_markup=markup)
    else:
        await message.answer_photo(img, caption=data['main_text'], reply_markup=markup)
    # await message.answer(data['main_text'], reply_markup=markup)





































# import time
# from datetime import datetime
#
# from aiogram import F
# from aiogram.dispatcher import router
# from aiogram.filters import Command
# from aiogram.fsm.context import FSMContext
# from aiogram.types import CallbackQuery, Message, ContentType
#
# from data.dbhandler import get_settings, get_user, add_user
# from keyboards.user_inline import get_check_token_type_inl, get_check_file_inl
# from keyboards.user_reply import get_menu_kb
# from data.kb_config import *
#
# @router.message(Command(commands=['start']))
# async def send_welcome(message: Message, state: FSMContext):
#     await state.clear()
#     settings = get_settings()
#     if get_user(user_id=message.from_user.id) is None:
#         add_user(message.from_user.id, message.from_user.full_name, message.from_user.username)
#     await message.answer(settings['main_text'], reply_markup=get_menu_kb())
#
#
# @router.message(F.text=load_token_btn)
# async def gg(message: Message, state: FSMContext):
#     await state.clear()
#     await message.answer("Как вы хотите отработать ваши токены?", reply_markup=get_check_token_type_inl())
#
#
# @dp.callback_query_handler(text_startswith="send_txt:", state="*")
# async def gg(call: CallbackQuery, state: FSMContext):
#     await state.finish()
#
#     await call.message.edit_text(
#         "Загрузите ваши токены в тхт формате "
#         "(Токены должны быть загружены в чистом виде, без лишних символов."
#         " Каждый токен в текстовом файле должен начинаться с новой строки)")
#     # await  (=call.data.split(":")[1])
#     await state.update_data(info=call.data.split(":")[1])
#     await state.set_state("wait_txt")
#
#
# @dp.message_handler(state='wait_txt', content_types=ContentType.DOCUMENT)
# async def gg(message: Message, state: FSMContext):
#     text = f"Пользователь: {message.from_user.username}\n" \
#            f"ID: {message.from_user.id}\n" \
#            f"Полный отчет: {'Да' if (await state.get_data())['info'] == 'yes' else 'Нет'}\n" \
#            f"Дата: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\n"
#     # destination = f"data/tokens/{str(message.from_user.id) + '_' +str(datetime.today())}.txt"
#     # await message.document.download(destination_dir=destination)
#     await bot.send_document(chat_id=get_settings()['botchat'], document=message.document.file_id, caption=text, reply_markup=get_check_file_inl((await state.get_data())['info'], message.from_user.id))
#     await message.answer("Ваши токены были успешно загружены! Ожидайте результата!")
#
# @dp.message_handler(text=profile_btn, state="*")
# async def gg(message: Message, state: FSMContext):
#     user = get_user(user_id=message.from_user.id)
#     text = f"ID: {user['user_id']}\n" \
#            f"Баланс: {user['balance']}\n" \
#            f"Загружено токенов: {user['token_count']}\n" \
#            f"Всего заработано: {user['total_balance']}\n"
#     await message.answer(text)
#
#
# @dp.callback_query_handler(text_startswith="", state="")
# async def gg(call: CallbackQuery, state: FSMContext):
#     pass
