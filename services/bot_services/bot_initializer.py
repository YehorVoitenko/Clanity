from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config.bot_config import TOKEN

dispatcher = Dispatcher(storage=MemoryStorage())


async def initialize_bot() -> None:
    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        )
    )

    await dispatcher.start_polling(bot)
