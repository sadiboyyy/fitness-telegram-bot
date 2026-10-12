from aiogram.types import KeyboardButton, ReplyKeyboardMarkup 
KeyboardButton(text="🧠 Интересные факты")

from aiogram.fsm.state import StatesGroup, State

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# -------------------------------
# Пользовательское главное меню
# -------------------------------
user_main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="💼 Бизнес"),
            KeyboardButton(text="📦 Услуги"),
        ],
        [
            KeyboardButton(text="📊 Статистика"),
            KeyboardButton(text="⚙️ Настройки"),
        ],
        [
            KeyboardButton(text="🆘 Поддержка"),
            KeyboardButton(text="📞 Контакты"),
        ],
    ],
    resize_keyboard=True
)

# -------------------------------
# Настройки пользователя
# -------------------------------
user_settings_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🧾 Профиль"),
            KeyboardButton(text="🔔 Уведомления"),
        ],
        [
            KeyboardButton(text="💬 Изменить имя"),
            KeyboardButton(text="🌐 Язык"),
        ],
        [
            KeyboardButton(text="◀️ Назад"),
        ],
    ],
    resize_keyboard=True
)

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

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def partnership_menu_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔗 Моя партнёрская ссылка",
                    callback_data="partner_my_link"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📊 Моя статистика",
                    callback_data="partner_stats"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📋 Условия сотрудничества",
                    callback_data="partner_terms"
                )
            ],
            [
                InlineKeyboardButton(
                    text="💰 Выплаты",
                    callback_data="partner_payout"
                )
            ],
            [
                InlineKeyboardButton(
                    text="◀️ Главное меню",
                    callback_data="partner_main_menu"
                )
            ],
        ]
    )

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
        ],
        [KeyboardButton(text="💎 Подписка"), KeyboardButton(text="💳 Оплата")],
        [KeyboardButton(text="🪙 FitCoins"),],
        [ KeyboardButton(text="✅ Задание дня"),],

        [KeyboardButton(text="🏆 Достижения"),],
        [KeyboardButton(text="🧘 Медитация"),],
        [KeyboardButton(text="🤸 Растяжка"),],

        [KeyboardButton(text="🤝 Партнёрская программа"),],
        [
            KeyboardButton(text="🔐 Админ-панель"),
        ],
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

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def partnership_menu_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔗 Моя партнёрская ссылка",
                    callback_data="partner_my_link"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📊 Моя статистика",
                    callback_data="partner_stats"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📋 Условия",
                    callback_data="partner_terms"
                )
            ],
            [
                InlineKeyboardButton(
                    text="💰 Как получить выплату",
                    callback_data="partner_payout"
                )
            ],
            [
                InlineKeyboardButton(
                    text="◀️ Главное меню",
                    callback_data="partner_main_menu"
                )
            ],
        ]
    )

