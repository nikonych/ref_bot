import asyncio
import concurrent.futures
import os
import queue
import zipfile
from threading import Thread

from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from keyboards.inline_admin import accept_user_inl
from keyboards.reply_z_all import menu_frep
from keyboards.inline_user import profile_buttons, info_buttons, top_buttons
from loader import dp, bot
import services.dbhandler as db

import time
import data.config as config
from services.user_functions import get_profile_text
from utils.misc.bot_filters import IsNoBan


# Открытие главного меню
@dp.message_handler(IsNoBan() , text=['⬅ Главное меню', '/start'], state="*")
async def main_start(message: Message, state: FSMContext):
    await state.finish()
    # print(open('tgbot/data/resourses/photo/main.jpg', 'rb').name)
    get_user = db.get_userx(user_id=message.from_user.id)
    if get_user is not None:
        await message.answer(f"<b>👋 Приветик {message.from_user.first_name}!</b>\n"
                             f"❤️ Добро пожаловать в {config.TEAM_NAME}!\n",
                             reply_markup=menu_frep(message.from_user.id))
    else:
        get_user = db.get_req(user_id=message.from_user.id)
        if get_user is None or get_user['status'] != 'Wait':
            await state.set_state('insert_lolz')
            await message.answer("Отправьте <b>ссылку на ваш профиль lolz.guru:</b>")
        else:
            await message.answer('⏳ Вы уже отправили заявку на рассмотрение, ожидайте')


@dp.message_handler(state='insert_lolz')
async def balance_for_withdraw(message: Message, state: FSMContext):
    if message.text.startswith("https://lolz.guru") or message.text.startswith("lolz.guru"):
        await state.update_data(insert_lolz=message.text)
        await state.set_state("insert_stazh")
        await message.answer('Введите ваш <b>опыт работы:</b>')
    else:
        await message.answer("<b>Введите валидную ссылку</b>")


@dp.message_handler(state='insert_stazh')
async def balance_for_withdraw(message: Message, state: FSMContext):
    async with state.proxy() as data:
        lolz = data['insert_lolz']
    stazh = message.text
    admin_chat = db.get_settings()['adminchat']
    user_id = message.from_user.id
    try:
        await bot.send_message(admin_chat,
                           f'🔰 Заявка на вступление:\n'
                           f'   🧑‍🚀 Пользователь: <a href="tg://user?id={user_id}">{message.from_user.first_name}</a>\n'
                           f'   💻 Форум: {lolz}\n'
                           f'   ✍️ Сообщение: {stazh}'
                           f'\n'
                           f'📜 История:'
                           , reply_markup=await accept_user_inl(user_id))
        db.new_req(user_id=user_id, status='Wait', lolz=lolz, stazh=stazh)
        await state.finish()
        await message.answer("⏳ Заявка на рассмотрении, ожидайте")
    except:
        pass




# Профиль
@dp.message_handler(text="👤 Профиль", state="*")
async def user_profile(message: Message, state: FSMContext):
    await state.finish()
    user_data = db.get_userx(user_id=message.from_user.id)
    await message.answer(await get_profile_text(user_data), reply_markup=await profile_buttons(user_data))






# Информация
@dp.message_handler(text="📕 Информация", state="*")
async def info_handler(message: Message, state: FSMContext):
    await state.finish()
    info_kb = await info_buttons(db.get_settings())
    dict_logs = db.get_logs_cols_sum()
    text = config.info_text.format(total_logs=dict_logs['SUM(alllogs)'],
                                   total_colds=dict_logs['SUM(allcolds)'],
                                   day_logs=dict_logs['SUM(daylogs)'],
                                   day_colds=dict_logs['SUM(daycolds)'],
                                   week_logs=dict_logs['SUM(weeklogs)'],
                                   week_colds=dict_logs['SUM(weekcolds)'],
                                   month_logs=dict_logs['SUM(monthlogs)'],
                                   month_colds=dict_logs['SUM(monthcolds)'],
                                   total_users=len(db.get_all_usersx()))
    await message.answer(text,reply_markup=info_kb)







# Доп функции
@dp.message_handler(text="💎 Доп. функции", state="*")
async def additional_functions_handler(message: Message, state: FSMContext):
    await message.answer('⚙️В разработке')