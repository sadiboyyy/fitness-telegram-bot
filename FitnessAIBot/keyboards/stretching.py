from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


stretching_goal_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🧘 Всё тело"),
            KeyboardButton(text="🦵 Ноги"),
        ],
        [
            KeyboardButton(text="🧍 Спина"),
            KeyboardButton(text="💪 Плечи и руки"),
        ],
        [
            KeyboardButton(text="🏋️ После тренировки"),
           
        ],
        [
            KeyboardButton(text="🏠 Главное меню"),
        ],
    ],
    resize_keyboard=True,
)


stretching_duration_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="4 минут"),
            KeyboardButton(text="7 минут"),
        ],
        [
            KeyboardButton(text="10 минут"),
           
        ],
        [
            KeyboardButton(text="🏠 Главное меню"),
        ],
    ],
    resize_keyboard=True,
)


stretching_level_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🌱 Новичок"),
            KeyboardButton(text="💪 Средний"),
        ],
        [
            KeyboardButton(text="🔥 Продвинутый"),
        ],
        [
            KeyboardButton(text="🏠 Главное меню"),
        ],
    ],
    resize_keyboard=True,
)