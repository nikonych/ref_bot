from aiogram.types import Message


async def dev_handler(message: Message):
    await message.answer('Developer: @xc0derx')
