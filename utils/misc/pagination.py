from typing import Callable, List

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from config import Config
from keyboards.inline.inline import BackMarkupInline


async def generate_pagination(session: AsyncSession, config: Config, build_page_func: Callable,
                              table_filters: dict = None,
                              start_index: int = 0, step: int = None, row_width: int = 1,
                              start_text: str = '', start_buttons: List[dict] = None,
                              show_back_button: bool = True, build_page_data: dict = None):
    # set default values
    step = step if step else config.misc.default_pagination_step
    table_filters = table_filters if table_filters else {}
    row_width = row_width if row_width else 1

    # build page
    text, buttons, items_count = await build_page_func(session, table_filters, start_index, step, build_page_data)

    # add start text
    if start_text:
        text = start_text + '\n' + text

    # build markup
    markup = InlineKeyboardBuilder()

    # add start buttons
    if start_buttons:
        markup.add(*[InlineKeyboardButton(text=button['text'],
                                          callback_data=button['callback_data'])
                     for button in start_buttons])

    # add page content buttons
    if buttons:
        markup.add(*buttons)
    else:
        markup.add(InlineKeyboardButton(text='🚫 Еще ничего нет 🚫', callback_data='do_not_click'))

    markup.adjust(row_width)

    # add control buttons
    control_buttons = []
    if start_index - step >= 0:
        control_buttons.append(InlineKeyboardButton(text='⬅️', callback_data=f'prev:{start_index}:{step}'))
    if start_index + step <= items_count:
        control_buttons.append(InlineKeyboardButton(text='➡️', callback_data=f'next:{start_index}:{step}'))
    markup.add(*control_buttons)
    markup.adjust(1)

    # add back button (optional)
    if show_back_button:
        markup.add(BackMarkupInline.back_button)
        markup.adjust(1)

    return text, markup.as_markup()
