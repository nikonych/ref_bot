from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from utils.schedule.add_percent_to_users import add_percent_to_users


async def run_services(session_pool):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(add_percent_to_users, "interval", hours=24, args=(session_pool,))
    scheduler.start()
