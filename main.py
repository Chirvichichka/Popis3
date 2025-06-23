import asyncio
import os
import random

from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv

from generation import NewsGenerator
from generation import QuoteGenerator
from generation import RaveGenerator

from keyboards import generation_text_keyboard

from tasks import send_random_rave

from config import Config
from middleware import BotMiddleware, RaveMiddleware, ConfigMiddleware

from handlers import user_router, admin_router

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
rave = RaveGenerator()
config = Config()
dispatcher = Dispatcher()

dispatcher.message.middleware(BotMiddleware(bot))
dispatcher.message.middleware(RaveMiddleware(rave))
dispatcher.message.middleware(ConfigMiddleware(config))

dispatcher.include_router(admin_router)
dispatcher.include_router(user_router)



async def main():
    asyncio.create_task(send_random_rave(bot=bot, chat_id=-4657793483, rave=rave, config=config))
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
