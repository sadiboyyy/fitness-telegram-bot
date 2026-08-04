from aiogram.types import ReplyKeyboardMarkup, KeyboardButton



nutrition_result_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🔄 Сгенерировать заново")
        ],
        [
            KeyboardButton(text="🛒 Список покупок")
        ],
        [
            KeyboardButton(text="📄 Скачать PDF")
        ],
        [
            KeyboardButton(text="🏠 Главное меню")
        ]
    ],
    resize_keyboard=True
)
goal_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔥 Похудение")],
        [KeyboardButton(text="💪 Набор массы")],
        [KeyboardButton(text="⚖️ Поддержание")]
    ],
    resize_keyboard=True
)


gender_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="👨 Мужчина")],
        [KeyboardButton(text="👩 Женщина")]
    ],
    resize_keyboard=True
)


workouts_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="0-1")],
        [KeyboardButton(text="2-3")],
        [KeyboardButton(text="4-5")],
        [KeyboardButton(text="6-7")]
    ],
    resize_keyboard=True
)


activity_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🪑 Сидячий образ жизни")],
        [KeyboardButton(text="🚶 Небольшая активность")],
        [KeyboardButton(text="🏃 Активный образ жизни")],
        [KeyboardButton(text="💼 Очень активный")]
    ],
    resize_keyboard=True
)


restrictions_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Нет ограничений")],
        [KeyboardButton(text="Не ем свинину")],
        [KeyboardButton(text="Не ем рыбу")],
        [KeyboardButton(text="Вегетарианец")],
        [KeyboardButton(text="Другое")]
    ],
    resize_keyboard=True
)


meals_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="3")],
        [KeyboardButton(text="4")],
        [KeyboardButton(text="5")],
        [KeyboardButton(text="6")]
    ],
    resize_keyboard=True
)


   
