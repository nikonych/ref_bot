import json

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.misc.kb_config import *


async def get_channels_inl(bot):
    list = []

    with open("database/settings.json", "r") as read_file:
        data = json.load(read_file)
    k = 1
    for channel in data["channels"]:
        link = await bot.create_chat_invite_link(chat_id=channel, name=f"Channel {k}")
        list.append([InlineKeyboardButton(text=f"Channel {k}", url=f"{link.invite_link}")])
        k += 1
    list.append([InlineKeyboardButton(text="Подписался",callback_data=f"accept_license")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=list)
    return keyboard

def get_check_token_type_inl():
    keyboard = InlineKeyboardMarkup()
    keyboard.inline_keyboard =[[InlineKeyboardButton(text=full_info_btn, callback_data=f"send_txt:yes")],
                 [InlineKeyboardButton(text=no_info_btn, callback_data=f"send_txt:no")]]
    return keyboard


def get_check_file_inl(check_type, user_id):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text=add_money_btn, callback_data=f"add_money:{user_id}:{check_type}"),
                 InlineKeyboardButton(text=empty_btn, callback_data=f"empty:{user_id}:{check_type}")
                 )
    if check_type == "yes":
        keyboard.add(InlineKeyboardButton(text=send_proof_btn, callback_data=f"send_proof:{user_id}:{check_type}"))
    return keyboard


def get_are_you_sure_inl(user_id, check_type):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text=yes_btn, callback_data=f"sure:yes:{user_id}:{check_type}"),
                 InlineKeyboardButton(text=no_btn, callback_data=f"sure:no:{user_id}:{check_type}")
                 )
    return keyboard