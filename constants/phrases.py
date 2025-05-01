from enum import Enum


class InteractivePhrases(Enum):
    WELCOME_MESSAGE = "Welcome! Use to start a vocabulary quiz from an Excel file."
    SET_LIMIT = "Please enter the number of words you want in the quiz:"
    SUCCESS_SET_LIMIT = "✅ Limit set. Starting the quiz..."
    WRONG_SET_LIMIT = "❌ Please enter a valid number (e.g., 10, 20)."
    ASK_TO_SEND_FILE = "📝 Got it! I’ll quiz you on your words. Now send me the Excel file. \n\n<i>*You can forward already send file from our chat)</i>"
    START_QUIZ = "✅ Loaded {len_of_pairs} words.\n🎯 Quiz length: {limit} rounds\n\nTranslate this word to Ukrainian:\n👉 {eng_word}"
    FINISH_QUIZ = "✅ Quiz finished! 🎉"
    CONGRATULATIONS = "<b>🎉 Congratulations! You've completed the quiz.</b>"
    CORRECT_USER_WORD = "✅ Correct!\n\nTranslate this word to Ukrainian:\n👉 {next_eng_word}"
    INCORRECT_USER_WORD = "❌ Incorrect. The correct answer is: {correct_answer}\nTry again.\n\n👉 {next_word}"
    WRONG_FILE_CONTENT_QUANTITY = "⚠️ The file only contains {len_of_pairs} entries, but you requested {limit}.\n I will use the full list instead."
    EMPTY_FILE = "❌ File not found. Please restart the quiz."
    SUCCESS_GET_PREVIOUS_FILE = "✅ Previous file was loaded from server"
    STOP_QUIZ = "🛑 The quiz was stopped"
    INSTRUCTION = """📖 *How to Use Clanity Bot*\n\n"
        "1️⃣ Send me a `.xlsx` file with word translations.\n"
        "2️⃣ Write translations for quiz words.\n\n"
        "📂 Here's an example file to help you get started 👇"""
