# - *- coding: utf- 8 - *-
from datetime import datetime, timedelta

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import dp, bot
import data.config as config

#from tgbot.services.api_sqlite import get_paymentx, get_crystal, get_yoo, get_settingsx



# Кнопки заявки вывода
async def withdraw_admin_buttons(withdraw_info):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("✅ Выполнено", callback_data=f"adminwithdraw_accept:{withdraw_info[0]}:{withdraw_info[1]}"),
                 InlineKeyboardButton("❌ Отклонить", callback_data=f"adminwithdraw_cancel:{withdraw_info[0]}:{withdraw_info[1]}"),
                 InlineKeyboardButton("⚠ Неправильный ввод", callback_data=f"adminwithdraw_wrong:{withdraw_info[0]}:{withdraw_info[1]}")
                 )
    return keyboard

# Варианты вывода средств
async def choose_withdraw():
    keyboard = InlineKeyboardMarkup()
    chooses = await config.get_choose_withdraw()
    len_chooses = len(chooses)

    if len_chooses == 1:
        keyboard.add(InlineKeyboardButton(chooses[0], callback_data=f"withdraw_to:{chooses[0]}"))
    elif len_chooses % 2 == 0:
        for i in range(0, len_chooses, 2):
            keyboard.add(InlineKeyboardButton(chooses[i], callback_data=f"withdraw_to:{chooses[i]}"),
                         InlineKeyboardButton(chooses[i+1], callback_data=f"withdraw_to:{chooses[i+1]}"))
    else:
        for i in range(0, len_chooses, 2):
            keyboard.add(InlineKeyboardButton(chooses[i], callback_data=f"withdraw_to:{chooses[i]}"),
                         InlineKeyboardButton(chooses[i+1], callback_data=f"withdraw_to:{chooses[i+1]}"))
        keyboard.add(InlineKeyboardButton(chooses[-1], callback_data=f"withdraw_to:{chooses[-1]}"))

    keyboard.add(InlineKeyboardButton("⬅ Назад", callback_data="user_profile"))

    return keyboard



# Back to user profile
async def back_button_to_profile():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("⬅ Назад", callback_data="user_profile"))
    return keyboard

# Back to main menu
async def back_button():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("⬅ Назад", callback_data="main"))
    return keyboard

# Клава Топ команды
async def top_buttons(user_id):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton('🏆 Топ за все время', callback_data=f"top_by_alllogs:{user_id}"),
                 InlineKeyboardButton('🏆 Топ за месяц', callback_data=f"top_by_monthlogs:{user_id}"))
    keyboard.add(InlineKeyboardButton('🏆 Топ за неделю', callback_data=f"top_by_weeklogs:{user_id}"),
                 InlineKeyboardButton('🏆 Топ за сегодня', callback_data=f"top_by_daylogs:{user_id}"))
    keyboard.add(InlineKeyboardButton('🧊 Топ по холодкам', callback_data=f"top_by_allcolds:{user_id}"))
    return keyboard

# Клава Информация
async def info_buttons(settings):
    button_list = []

    try:
        if settings['logchat'] != 0:
            if config.otstuklink == '':
                link = await bot.create_chat_invite_link(settings['logchat'], member_limit=2)
                link = link.invite_link
                await config.updatelink('otstuklink', link)
                config.otstuklink = link
            else: link = config.otstuklink

            button_list.append(InlineKeyboardButton('Канал отстука', url=link))
    except: pass

    try:
        if settings['profitchat'] != 0:
            if config.profitlink == '':
                link = await bot.create_chat_invite_link(settings['profitchat'], member_limit=2)
                link = link.invite_link
                await config.updatelink('profitlink', link)
                config.profitlink =link
            else: link = config.otstuklink

            button_list.append(InlineKeyboardButton('Канал профитов', url=link))
    except: pass

    try:
        if settings['workerchat'] != 0:
            if config.workerchatlink == '':
                link = await bot.create_chat_invite_link(settings['workerchat'], member_limit=2)
                link = link.invite_link
                await config.updatelink('workerchatlink', link)
                config.workerchatlink = link
            else: link = config.otstuklink

            button_list.append(InlineKeyboardButton('Канал отстука', url=link))
    except: pass

    try:
        if settings['newschat'] != 0:
            if config.newslink == '':
                link = await bot.create_chat_invite_link(settings['newschat'], member_limit=2)
                link = link.invite_link
                await config.updatelink('newslink', link)
                config.newslink = link
            else: link = config.otstuklink

            button_list.append(InlineKeyboardButton('Новостной канал', url=link))
    except: pass

    keyboard = InlineKeyboardMarkup()

    if len(button_list) == 4: keyboard.add(button_list[0], button_list[1]); keyboard.add(button_list[2], button_list[3])
    elif len(button_list) == 3: keyboard.add(button_list[0], button_list[1]); keyboard.add(button_list[2])
    elif len(button_list) == 2: keyboard.add(button_list[0], button_list[1])
    elif len(button_list) == 1: keyboard.add(button_list[0])
    else: keyboard = None

    return keyboard



# Клавиши профиля
async def profile_buttons(user_data):
    keyboard = InlineKeyboardMarkup()

    if user_data['is_visible']:
        keyboard.add(InlineKeyboardButton('🔴 Скрыть юзернейм', callback_data=f"hide_username:{user_data['user_id']}"),
                     InlineKeyboardButton('🔄 Обновить юзернейм', callback_data=f"refresh_username:{user_data['user_id']}"))
    else:
        keyboard.add(InlineKeyboardButton('🟢 Показать юзернейм', callback_data=f"show_username:{user_data['user_id']}"),
                     InlineKeyboardButton('🔄 Обновить юзернейм', callback_data=f"refresh_username:{user_data['user_id']}"))

    keyboard.add(InlineKeyboardButton('💳 Вывести средства', callback_data=f"withdraw:{user_data['user_id']}"),
                 InlineKeyboardButton('⚙ Настройка отработки', callback_data=f"otrabotka_settings:{user_data['user_id']}"))

    return keyboard


# Выбор способов пополнения
def refill_choice_finl():
    keyboard = InlineKeyboardMarkup()

    get_payments = get_paymentx()
    crystal = get_crystal()
    wm = get_yoo()
    active_kb = []

    if get_payments['way_form'] == "True":
        active_kb.append(InlineKeyboardButton("🥝 QIWI", callback_data="refill_choice:Form"))
    # if get_payments['way_number'] == "True":
    #     active_kb.append(InlineKeyboardButton("📞 QIWI номер", callback_data="refill_choice:Number"))
    # if get_payments['way_nickname'] == "True":
    #     active_kb.append(InlineKeyboardButton("Ⓜ QIWI никнейм", callback_data="refill_choice:Nickname"))

    if crystal['status'] == True:
        active_kb.append(InlineKeyboardButton("💎 Crystal", callback_data="refill_choice:Crystal"))

    if wm['status'] == True:
        active_kb.append(InlineKeyboardButton("🌍 Yoomoney", callback_data="refill_choice:YooMoney"))


    if len(active_kb) == 5:
        keyboard.add(active_kb[0], active_kb[1])
        keyboard.add(active_kb[2], active_kb[3])
        keyboard.add(active_kb[4])
    if len(active_kb) == 4:
        keyboard.add(active_kb[0], active_kb[1])
        keyboard.add(active_kb[2], active_kb[3])
    elif len(active_kb) == 3:
        keyboard.add(active_kb[0], active_kb[1])
        keyboard.add(active_kb[2])
    elif len(active_kb) == 2:
        keyboard.add(active_kb[0], active_kb[1])
    elif len(active_kb) == 1:
        keyboard.add(active_kb[0])
    else:
        keyboard = None

    if len(active_kb) >= 1:
        keyboard.add(InlineKeyboardButton("Назад", callback_data="user_profile"))

    return keyboard


# Проверка киви платежа
def refill_bill_finl(send_requests, get_receipt, get_way):
    keyboard = InlineKeyboardMarkup(
    ).add(
        InlineKeyboardButton("🌀 Перейти к оплате", url=send_requests)
    ).add(
        InlineKeyboardButton("🔄 Проверить оплату", callback_data=f"Pay:{get_way}:{get_receipt}")
    )

    return keyboard


def refill_bill_finl_wm(send_requests):
    keyboard = InlineKeyboardMarkup(
    ).add(
        InlineKeyboardButton("🌀 Перейти к оплате", url=send_requests)
    )

    return keyboard



# Кнопки при открытии самого товара
def products_open_finl(user_id ,position_id, remover, category_id, subcategory_id):
    if user_id not in get_admins():
        keyboard = InlineKeyboardMarkup(
        ).add(
            InlineKeyboardButton("💳 Купить товар", callback_data=f"buy_item_select:{position_id}")
        ).add(
            InlineKeyboardButton("Назад", callback_data=f"buy_position_return:{remover}:{category_id}:{subcategory_id}")
        )
    else:
        keyboard = InlineKeyboardMarkup(
        ).add(
            InlineKeyboardButton("✅ Купить", callback_data=f"buy_item_select:{position_id}"),
            InlineKeyboardButton("❄️ Посмотреть", callback_data=f"show_item_select:{position_id}:{category_id}:{subcategory_id}")
        ).add(
            InlineKeyboardButton("Назад", callback_data=f"buy_position_return:{remover}:{category_id}:{subcategory_id}")
        )

    return keyboard


# Подтверждение покупки товара
def products_confirm_finl(position_id, get_count):
    keyboard = InlineKeyboardMarkup(
    ).add(
        InlineKeyboardButton("✅ Подтвердить", callback_data=f"xbuy_item:yes:{position_id}:{get_count}"),
        InlineKeyboardButton("❌ Отменить", callback_data=f"xbuy_item:not:{position_id}:{get_count}")
    )

    return keyboard


def products_item_check(item_id, position_id, category_id, subcategory_id):
    keyboard = InlineKeyboardMarkup(
    ).add(
        InlineKeyboardButton("✅ Да", callback_data=f"change_item_check:{item_id}:gg:{position_id}:{category_id}:{subcategory_id}"),
        InlineKeyboardButton("⛔️ Нет", callback_data=f"show_item_select:{position_id}:{category_id}:{subcategory_id}")
    )
    return keyboard

def products_item_check_file(item_id, position_id, category_id, subcategory_id):
    keyboard = InlineKeyboardMarkup(
    ).add(
        InlineKeyboardButton("✅ Да", callback_data=f"change_item_file_check:{item_id}:gg:{position_id}:{category_id}:{subcategory_id}"),
        InlineKeyboardButton("⛔️ Нет", callback_data=f"show_item_select:{position_id}:{category_id}:{subcategory_id}")
    )
    return keyboard

# Ссылка на поддержку
def user_support_finl():
    settings = get_settingsx()

    keyboard = InlineKeyboardMarkup(
    ).add(
        InlineKeyboardButton("💌 Написать", callback_data=f"links_to_admins"),
    )
    if settings['misc_chat_link'] != None:
        keyboard.add(
            InlineKeyboardButton("🍷 Ламповый Чат", url=settings['misc_chat_link']))
    keyboard.add(
        InlineKeyboardButton("Закрыть", callback_data="close_this")
    )
    return keyboard

def admin_support_finl(admin, support):
    keyboard = InlineKeyboardMarkup(
    ).add(
        InlineKeyboardButton("🧛🏻‍♀️ Support", url=f"https://t.me/{support}"),
        InlineKeyboardButton("🎩 Admin", url=f"https://t.me/{admin}"),
    ).add(
        InlineKeyboardButton("Назад", callback_data="open_faq")
    )

    return keyboard

def user_edit_item(position_id, remover, category_id, subcategory_id):
    keyboard = InlineKeyboardMarkup(
    ).add(
        InlineKeyboardButton("🆙 Изменить", callback_data=f"change_item_select:{position_id}:{category_id}:{subcategory_id}"),
    ).add(
        InlineKeyboardButton("Назад", callback_data=f"buy_position_open:{position_id}:{remover}:{category_id}:{subcategory_id}")
    )

    return keyboard
