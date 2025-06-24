from aiogram import BaseMiddleware

from generation.rave.legacy.rave_generator_legacy import RaveGenerator


class RaveMiddleware(BaseMiddleware):
    def __init__(self, rave: RaveGenerator):
        self.rave = rave

    async def __call__(self, handler, event, data):
        data["rave"] = self.rave
        return await handler(event, data)
