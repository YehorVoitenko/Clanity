from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton


class ButtonOrchestrator:
    @classmethod
    def get_buttons_for_start(cls):
        button_list = [
            [InlineKeyboardButton(text="Start quiz", callback_data='start_quiz_with_new_file')],
            [InlineKeyboardButton(text="Use previous file", callback_data='start_quiz_with_previous_file')],
        ]
        return InlineKeyboardMarkup(inline_keyboard=button_list)
