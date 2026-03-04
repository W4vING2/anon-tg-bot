from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔗 Создать приглашение")],
        [KeyboardButton(text="🔴 Завершить чат"), KeyboardButton(text="ℹ️ О боте")],
    ],
    resize_keyboard=True
)

INFO_TEXT = (
    "ℹ️ <b>Анонимный чат бот</b>\n\n"
    "Этот бот позволяет переписываться анонимно.\n"
    "Никто из собеседников не видит имя или юзернейм друг друга.\n\n"
    "<b>Команды:</b>\n"
    "/start — главное меню\n"
    "/invite — новая ссылка-приглашение\n"
    "/stop — завершить чат"
)
