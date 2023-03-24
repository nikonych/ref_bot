from typing import List

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from config import Config
from utils.misc.get_build_page_func import get_build_page_func
from utils.misc.pagination import generate_pagination


async def pagination_handler(call: CallbackQuery, state: FSMContext, session: AsyncSession, config: Config):
    action, index, step = call.data.split(':')
    index, step = int(index), int(step)
    if action == 'next':
        index += step
    else:
        index -= step

    await state.update_data(current_index=index, step=step)

    data = await state.get_data()

    table_filters: dict = data.get('table_filters')
    build_page_path: str = data.get('build_page_path')
    build_page_data: dict = data.get('build_page_data')
    start_index: int = data.get('current_index')
    row_width: int = data.get('row_width')
    start_text: str = data.get('start_text')
    show_back_button: bool = data.get('show_back_button', True)
    start_buttons: List[dict] = data.get('start_buttons')

    text, markup = await generate_pagination(session=session, config=config, build_page_func=get_build_page_func(build_page_path),
                                             table_filters=table_filters,
                                             start_index=start_index, step=step, row_width=row_width,
                                             start_text=start_text, start_buttons=start_buttons,
                                             show_back_button=show_back_button,
                                             build_page_data=build_page_data)

    if markup and not text:
        await call.message.edit_reply_markup(markup)
    else:
        if call.message.content_type == 'text':
            await call.message.edit_text(text, reply_markup=markup)
        else:
            await call.message.edit_caption(text, reply_markup=markup)
