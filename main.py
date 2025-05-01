import asyncio
import logging
import sys

from aiogram import F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config.storage_service_config import MINIO_BUCKET_NAME
from constants.enums import StateKeys, FileTypes
from processors.database_processors import UserDBProcessor
from services.bot_services.bot_initializer import initialize_bot, dispatcher
from services.bot_services.buttons import ButtonOrchestrator
from services.database import init_tables, get_database_session
from constants.phrases import InteractivePhrases
from processors.bot_processors import QuizProcessor
from services.bot_services.states import AvailableStates
from services.storage_service import storage_client


from processors.storage_service_processor import StorageServiceProcessor


@dispatcher.message(CommandStart())
async def start_cmd(message: Message):
    if message.from_user.is_bot:
        return

    task = UserDBProcessor(
        session=next(get_database_session())
    )
    task.create_user_if_not_exists(
        user_id=message.from_user.id
    )

    await message.answer(
        text=InteractivePhrases.WELCOME_MESSAGE.value,
        reply_markup=ButtonOrchestrator.get_buttons_for_start()
    )


@dispatcher.callback_query(F.data == 'start_quiz_with_new_file')
async def start_quiz_with_new_file(callback, state: FSMContext):
    await QuizProcessor.ask_user_to_send_file(message=callback.message)
    await state.set_state(AvailableStates.awaiting_file_upload)


@dispatcher.callback_query(F.data == 'start_quiz_with_previous_file')
async def start_quiz_with_previous_file(callback, state: FSMContext):
    await callback.message.answer(InteractivePhrases.SUCCESS_GET_PREVIOUS_FILE.value)

    try:
        file_response = storage_client.get_object(
            bucket_name=MINIO_BUCKET_NAME,
            object_name=f"{callback.from_user.id}.xlsx"
        )
        file_data_in_bytes: bytes = file_response.read()

    finally:
        file_response.close()
        file_response.release_conn()

    await state.update_data({StateKeys.UPLOADED_FILE_DATA.value: file_data_in_bytes})

    await callback.message.answer(InteractivePhrases.SET_LIMIT.value)
    await state.set_state(AvailableStates.awaiting_quiz_limit)


@dispatcher.message(AvailableStates.awaiting_file_upload, F.document)
async def handle_new_file_from_user(message: Message, state: FSMContext):
    await QuizProcessor.process_user_new_file(
        message=message,
        state=state
    )

@dispatcher.message(AvailableStates.awaiting_previous_file_upload)
async def handle_previous_user_file(message: Message, state: FSMContext):
    await QuizProcessor.process_previous_user_file(
        message=message,
        state=state
    )


@dispatcher.message(AvailableStates.process_user_word_answer)
async def process_user_word_answer(message: Message, state: FSMContext):
    await QuizProcessor.process_user_answer(
        message=message,
        state=state
    )


@dispatcher.message(AvailableStates.awaiting_quiz_limit)
async def handler_quiz_limit_input(message: Message, state: FSMContext):
    await QuizProcessor.handler_quiz_start(
        message=message,
        state=state
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    init_tables()
    StorageServiceProcessor.init_minio_bucket()
    asyncio.run(initialize_bot())
