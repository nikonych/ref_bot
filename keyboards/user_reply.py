import json

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from utils.misc.kb_config import *


def get_menu_kb():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True,
                                   keyboard=[

                                       [KeyboardButton(text=action_btn), KeyboardButton(text=profile_btn)],
                                       [KeyboardButton(text=help_btn), KeyboardButton(text=information_btn)],
                                       [KeyboardButton(text=about_us_btn)]
                                   ])

    return keyboard


def get_accept_kb():
    list = []

    with open("database/settings.json", "r") as read_file:
        data = json.load(read_file)
    for channel in data["channels"]:
        list.append([KeyboardButton(text=channel)])

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True,
                                   keyboard=list)

    return keyboard
