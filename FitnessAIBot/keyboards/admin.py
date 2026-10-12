from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📊 Дашборд"),
            KeyboardButton(text="👥 Пользователи"),
        ],
        [
            KeyboardButton(text="💰 Финансы"),
            KeyboardButton(text="📢 Рассылки"),
        ],
        [
            KeyboardButton(text="🎟 Промокоды"),
            KeyboardButton(text="🤝 Партнёрская программа"),
        ],
        [
            KeyboardButton(text="🏋️ Контент"),
            KeyboardButton(text="🆘 Поддержка"),
        ],
        [
            KeyboardButton(text="⚙️ Настройки"),
            KeyboardButton(text="🏠 Главное меню"),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Управление Fitness AI",
)

admin_settings_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="💳 Подписки"),
            KeyboardButton(text="🤖 AI настройки"),
        ],
        [
            KeyboardButton(text="📦 Тарифы"),
            KeyboardButton(text="🔒 Ограничения"),
        ],
        [
            KeyboardButton(text="◀️ Назад"),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Настройки бота",
)

users_admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🔎 Найти пользователя"),
            KeyboardButton(text="🆕 Последние регистрации"),
        ],
        [
            KeyboardButton(text="💎 С подпиской"),
            KeyboardButton(text="🆓 Без подписки"),
        ],
        [
            KeyboardButton(text="🚫 Заблокированные"),
            KeyboardButton(text="📊 Статистика пользователей"),
        ],
        [
            KeyboardButton(text="⬅️ Назад в админку"),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Управление пользователями",
)

def user_card_keyboard(
    telegram_id: int,
    is_blocked: bool = False,
):
    block_text = (
        "✅ Разблокировать"
        if is_blocked
        else "🚫 Заблокировать"
    )

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💎 Подписка",
                    callback_data=f"admin_subscription:{telegram_id}",
                ),
                InlineKeyboardButton(
                    text="💳 Платежи",
                    callback_data=f"admin_payments:{telegram_id}",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="✉️ Написать",
                    callback_data=f"admin_message:{telegram_id}",
                ),
                InlineKeyboardButton(
                    text=block_text,
                    callback_data=f"admin_block:{telegram_id}",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🔄 Обновить",
                    callback_data=f"admin_refresh:{telegram_id}",
                ),
            ],
        ]
    )