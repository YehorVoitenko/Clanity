import io
import os
import random
import tempfile

import pandas as pd

from io import BytesIO
from typing import BinaryIO

from aiogram.fsm.context import FSMContext
from aiogram.types import Document, Message, File

from config.storage_service_config import MINIO_BUCKET_NAME
from constants.common_constants import AVAILABLE_FILE_FORMATS
from constants.enums import StateKeys
from constants.phrases import InteractivePhrases
from processors.database_processors import FileDBProcessor
from services.bot_services.states import AvailableStates
from services.database import get_database_session
from services.storage_service import storage_client


class QuizProcessor:
    @classmethod
    async def handler_quiz_start(cls, message: Message, state: FSMContext):
        try:
            limit = int(message.text)
            await state.update_data({StateKeys.QUIZ_LIMIT.value: limit})

            state_data = await state.get_data()
            file_bytes = state_data.get(StateKeys.UPLOADED_FILE_DATA.value)

            if file_bytes is None:
                await message.answer(InteractivePhrases.EMPTY_FILE.value)
                await state.clear()
                return

            await cls.process_file_with_words(
                file_data=BytesIO(file_bytes),
                message=message,
                state=state
            )

        except ValueError:
            await message.answer(InteractivePhrases.WRONG_SET_LIMIT.value)

    @classmethod
    async def ask_user_to_send_file(cls, message: Message) -> None:
        await message.answer(InteractivePhrases.ASK_TO_SEND_FILE.value)

    @classmethod
    async def success_file_get(cls, message: Message) -> None:
        await message.answer(InteractivePhrases.ASK_TO_SEND_FILE.value)

    @classmethod
    async def process_user_new_file(cls, message: Message, state: FSMContext):
        document: Document = message.document

        if not document.file_name.endswith(AVAILABLE_FILE_FORMATS):
            await message.answer(f"The file must be in formats {AVAILABLE_FILE_FORMATS}.")
            return

        file: File = await message.bot.get_file(file_id=document.file_id)
        file_data: BinaryIO = await message.bot.download_file(file_path=file.file_path)
        file_data_in_bytes: bytes = file_data.read()

        await state.update_data({StateKeys.UPLOADED_FILE_DATA.value: file_data_in_bytes})

        await cls.create_file_in_storage_client(message=message, file=file, file_data=file_data_in_bytes)

        await message.answer(InteractivePhrases.SET_LIMIT.value)
        await state.set_state(AvailableStates.awaiting_quiz_limit)

    @classmethod
    async def process_previous_user_file(cls, message: Message, state: FSMContext):
        file_response = None

        try:
            file_response = storage_client.get_object(
                bucket_name=MINIO_BUCKET_NAME,
                object_name=f"{message.from_user.id}.xlsx"
            )
            file_data_in_bytes: bytes = file_response.read()

        except Exception as e:
            await message.answer(InteractivePhrases.EMPTY_FILE.value)
            print(f'\nUSER BUG. USER ID {message.from_user.id}')
            print(str(e), '\n')
            return

        finally:
            if file_response:
                file_response.close()
                file_response.release_conn()

        await state.update_data({StateKeys.UPLOADED_FILE_DATA.value: file_data_in_bytes})

        await message.answer(InteractivePhrases.SET_LIMIT.value)
        await state.set_state(AvailableStates.awaiting_quiz_limit)

    @staticmethod
    async def create_file_in_storage_client(message: Message, file: File, file_data: bytes):
        file_content_type = file.file_path.split('.')[1]

        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_content_type}") as tmp_file:
            tmp_file.write(file_data)
            tmp_file_path = tmp_file.name

        object_name = f"{message.from_user.id}.{file_content_type}"
        buf = io.BytesIO(file_data)

        storage_client.put_object(
            bucket_name=MINIO_BUCKET_NAME,
            object_name=object_name,
            data=buf,
            length=buf.getbuffer().nbytes,
        )

        file_link_in_minio = storage_client.presigned_get_object(
            MINIO_BUCKET_NAME, object_name
        )

        task = FileDBProcessor(
            session=next(get_database_session())
        )
        task.create_file_link_if_not_exists(
            user_id=message.from_user.id,
            file_link=file_link_in_minio
        )

        os.remove(tmp_file_path)

    @staticmethod
    async def process_file_with_words(file_data: BinaryIO, message: Message, state: FSMContext):
        try:
            file_buffer = BytesIO(file_data.read())
            df = pd.read_excel(file_buffer)

            if df.shape[1] < 2:
                await message.answer("Excel file must have at least two columns.")
                return

            all_word_pairs = list(df.itertuples(index=False, name=None))

            state_data = await state.get_data()
            limit = state_data.get(StateKeys.QUIZ_LIMIT.value, 10)

            if limit > len(all_word_pairs):
                await message.answer(
                    InteractivePhrases.WRONG_FILE_CONTENT_QUANTITY.value.format(
                        len_of_pairs=len(all_word_pairs),
                        limit=limit
                    )
                )

                limit = len(all_word_pairs)

            quiz_data = random.sample(all_word_pairs, limit)

            await state.update_data({StateKeys.QUIZ_DATA.value: quiz_data})
            await state.update_data({StateKeys.ROW_INDEX.value: 0})

            await state.set_state(AvailableStates.process_user_word_answer)

            eng_word = quiz_data[0][0]
            await message.answer(
                InteractivePhrases.START_QUIZ.value.format(
                    len_of_pairs=len(all_word_pairs),
                    limit=limit,
                    eng_word=eng_word
                )
            )

        except Exception as e:
            await message.answer(f"Failed to read Excel file: {e}")

    @staticmethod
    async def process_user_answer(message: Message, state: FSMContext):
        state_data = await state.get_data()
        index = state_data.get(StateKeys.ROW_INDEX.value, 0)
        quiz_data = state_data.get(StateKeys.QUIZ_DATA.value, [])

        if index >= len(quiz_data):
            await message.answer(InteractivePhrases.FINISH_QUIZ.value)
            await state.clear()
            return

        current_pair = quiz_data[index]
        correct_answer = str(current_pair[1]).strip().lower()
        user_answer = message.text.strip().lower()

        if user_answer == correct_answer:
            index += 1
            await state.update_data({StateKeys.ROW_INDEX.value: index})

            if index >= len(quiz_data):
                await message.answer(InteractivePhrases.CONGRATULATIONS.value)
                await state.clear()
                return

            next_eng_word = quiz_data[index][0]
            await message.answer(
                InteractivePhrases.CORRECT_USER_WORD.value.format(
                    next_eng_word=next_eng_word
                )
            )

        else:
            await message.answer(
                InteractivePhrases.INCORRECT_USER_WORD.value.format(
                    correct_answer=correct_answer,
                    next_word=current_pair[0]
                )
            )
