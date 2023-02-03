
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message


from loader import dp





@dp.callback_query_handler(text_startswith="", state="*")
async def gg(call: CallbackQuery, state: FSMContext):
    pass


@dp.message_handler(state='')
async def gg(message: Message, state: FSMContext):
    pass


@dp.message_handler(text="gg")
async def gg(message: Message, state: FSMContext):
    await message.answer("gg")

@dp.callback_query_handler(text_startswith="", state="")
async def gg(call: CallbackQuery, state: FSMContext):
    pass


