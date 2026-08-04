from aiogram.types import KeyboardButton, ReplyKeyboardMarkup 
KeyboardButton(text="🧠 Интересные факты")

from aiogram.fsm.state import StatesGroup, State



class NutritionForm(StatesGroup):
    goal = State()
    height = State()
    weight = State()
    age = State()
    gender = State()
    workouts = State()
    activity = State()
    restrictions = State()
    budget = State()
    meals = State()
    favorite_foods = State()

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="💪 Программа тренировок"),
            KeyboardButton(text="🥗 Рассчитать калории"),
            KeyboardButton(text="🍽 Программа питания"),
        ],
        [ KeyboardButton(text="🔄 Изменить программу"), 
         
      
            KeyboardButton(text="📈 Мой прогресс"),
            KeyboardButton(text="🤖 Спросить ИИ"),
        ],
        [KeyboardButton(text="🎙 Голосовой фитнес-чат"),
         KeyboardButton(text="⏰ Напоминания о тренировках"),
        ]
    ],
    resize_keyboard=True,

    input_field_placeholder="Выберите действие",
)


cancel_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="❌ Отмена")],
    ],
    resize_keyboard=True,
)
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


ai_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📸 Анализ формы тела"),
        ],
        [
            KeyboardButton(text="🎥 Проверить технику упражнений"),
        ],
        [
            KeyboardButton(text="💬 Задать вопрос"),
        ],
         [
            KeyboardButton(text="🧠 Интересные факты"),
        ],
        [
            KeyboardButton(text="◀️ Главное меню"),
        ],
    ],
    resize_keyboard=True,
    # input_field_placeholder="Выберите функцию ИИ",
)