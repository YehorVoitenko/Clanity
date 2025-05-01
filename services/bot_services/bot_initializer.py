from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config.bot_config import TOKEN

dispatcher = Dispatcher(storage=MemoryStorage())

from aiogram import Bot
from aiogram.types import BotCommand


async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="▶️ Начать"),
        BotCommand(command="instruction", description="📖 Инструкция"),
        BotCommand(command="stop_quiz", description="🛑 Остановить викторину"),
    ]
    await bot.set_my_commands(commands)


async def initialize_bot() -> None:
    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        )
    )
    await set_bot_commands(bot)

    await dispatcher.start_polling(bot)
