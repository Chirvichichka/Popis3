import asyncio
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from config import Config
from generation import RaveGenerator
from handlers import user_router, admin_router
from middleware import BotMiddleware, RaveMiddleware, ConfigMiddleware
from tasks import send_random_rave

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
