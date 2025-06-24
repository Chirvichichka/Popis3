from typing import Callable, Dict, Any

from aiogram import BaseMiddleware, Bot


class BotMiddleware(BaseMiddleware):
    def __init__(self, bot: Bot):
        self.bot = bot

    async def __call__(
            self,
            handler: Callable,
            event: Any,
            data: Dict[str, Any]
    ) -> Any:
        data["bot"] = self.bot
        return await handler(event, data)
