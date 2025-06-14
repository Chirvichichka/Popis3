import asyncio
import os

from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv

from generation import NewsGenerator

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dispatcher = Dispatcher()
router = Router()


@router.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Привет, я попис3")


@router.message(Command("news"))
async def news_command(message: Message):
    news_generator = NewsGenerator()
    news = news_generator.generate(language="ru")
    await message.answer(news)


dispatcher.include_router(router)


async def main():
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
