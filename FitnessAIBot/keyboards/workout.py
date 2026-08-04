from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

goal_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔥 Похудение")],
        [KeyboardButton(text="💪 Набор мышечной массы")],
        [KeyboardButton(text="⚖️ Поддержание формы")],
    ],
    resize_keyboard=True
)

experience_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🟢 Новичок")],
        [KeyboardButton(text="🟡 Средний")],
        [KeyboardButton(text="🔴 Продвинутый")],
    ],
    resize_keyboard=True
)

place_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🏋️ Тренажерный зал")],
        [KeyboardButton(text="🏠 Дом")],
    ],
    resize_keyboard=True
)

days_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="2"),
            KeyboardButton(text="3"),
            KeyboardButton(text="4"),
        ],
        [
            KeyboardButton(text="5"),
            KeyboardButton(text="6"),
        ]
    ],
    resize_keyboard=True
)