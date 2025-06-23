from main_imports import *

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dispatcher = Dispatcher()
router = Router()

rave = RaveGenerator()

commands = ["/start", "/commands", "/news", "/quote", "/rave", "/prob"]


@router.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Привет, я попис-адептус, я пока не умею материться", reply_markup=generation_text_keyboard)


@router.message(Command("commands"))
async def commands_command(message: Message):
    await message.answer("\n".join(commands), reply_markup=generation_text_keyboard)


@router.message(Command("prob"))
async def prob_command(message: Message):
    await message.answer(f"Вероятность этого {random.randint(1, 99)}.{random.randint(1, 99):02}%")


@router.message(Command("rave"))
async def rave_command(message: Message):
    await message.answer(rave.generate())


@router.message(Command("news"))
async def news_command(message: Message):
    await bot.send_chat_action(message.chat.id, "typing")

    start_word = message.text.replace("/news ", "")

    news_generator = NewsGenerator()
    news = news_generator.generate(language="ru", start_word = start_word)

    await message.answer(news)


@router.message(Command("quote"))
async def quote_command(message: Message):
    await bot.send_chat_action(message.chat.id, "typing")
    quote_generator = QuoteGenerator()
    quote = quote_generator.generate(language="ru")
    await message.answer(quote)


@router.message(F.text)
async def handle_text(message: Message):
    rave.add_text(message.text.lower())


dispatcher.include_router(router)


async def send_random_rave():
    while True:
        wait_time = random.randint(60, 300)
        text = rave.generate()

        await asyncio.sleep(wait_time)
        await bot.send_message(chat_id = -4657793483, text = text)


async def main():
    asyncio.create_task(send_random_rave())
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
