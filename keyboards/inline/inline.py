from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class BackMarkupInline:
    back_button = InlineKeyboardButton(text='⬅️ Назад', callback_data='back')
    back_markup = InlineKeyboardMarkup(inline_keyboard=[
        [back_button]
    ])