from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
import asyncio
import logging
from config import bot, ADMIN
from handlers import router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

dp = Dispatcher()


# optional --->
async def bot_stopped():
    await bot.send_message(ADMIN, '🛑Bot to\'xtadi!!!')


async def bot_started():
    await bot.send_message(ADMIN, "🏁Bot ishga tushdi!!!")


async def start():
    dp.startup.register(bot_started)
    dp.shutdown.register(bot_stopped)
    await bot.set_my_commands([
        BotCommand(command='/start', description='Botni ishga tushurish'),
        BotCommand(command='/help', description='Yordam uchun'),
        BotCommand(command='/stop', description='Jarayonni to\'xtatish'),
        BotCommand(command='/new', description='Jarayonni boshidan boshlash'),
    ])
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(start())
