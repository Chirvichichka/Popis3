from main_imports import *

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dispatcher = Dispatcher()
router = Router()

commands = ["/start", "/commands", "/news", "/quote"]


@router.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Привет, я попис-адептус, я пока не умею материться")


@router.message(Command("commands"))
async def commands_command(message: Message):
    await message.answer("\n".join(commands))


@router.message(Command("news"))
async def news_command(message: Message):
    await bot.send_chat_action(message.chat.id, "typing")
    news_generator = NewsGenerator()
    news = news_generator.generate(language="ru")
    await message.answer(news)


@router.message(Command("quote"))
async def quote_command(message: Message):
    await bot.send_chat_action(message.chat.id, "typing")
    quote_generator = QuoteGenerator()
    quote = quote_generator.generate(language="ru")
    await message.answer(quote)


dispatcher.include_router(router)


async def main():
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
