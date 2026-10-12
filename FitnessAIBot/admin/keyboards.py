from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def content_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="💪 Упражнения"),
                KeyboardButton(text="🏋️ Тренировки"),
            ],
            [
                KeyboardButton(text="🥗 Питание"),
                KeyboardButton(text="🧘 Медитации"),
            ],
            [
                KeyboardButton(text="📚 Информация"),
            ],
            [
                KeyboardButton(text="◀️ Админ-панель"),
            ],
        ],
        resize_keyboard=True,
    )


def broadcast_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="👥 Всем пользователям"),
            ],
            [
                KeyboardButton(text="💳 Premium пользователям"),
            ],
            [
                KeyboardButton(text="🟢 Активным пользователям"),
            ],
            [
                KeyboardButton(text="◀️ Админ-панель"),
            ],
        ],
        resize_keyboard=True,
    )


def settings_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="💳 Настройки подписки"),
            ],
            [
                KeyboardButton(text="🤖 Настройки AI"),
            ],
            [
                KeyboardButton(text="🎙 Настройки голосового чата"),
            ],
            [
                KeyboardButton(text="📸 Настройки анализа фото"),
                
            ],
            [
                KeyboardButton(text="🎥 Настройки анализа видео"),
            ],
            [
                KeyboardButton(text="◀️ Админ-панель"),
            ],
        ],
        resize_keyboard=True,
    )

def voice_settings_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🎙 Включить голосовой чат"),
            ],
            [
                KeyboardButton(text="🔇 Выключить голосовой чат"),
            ],
            [
                KeyboardButton(text="⏱ Лимит голосового сообщения"),
            ],
            [
                KeyboardButton(text="◀️ Назад"),
            ],
        ],
        resize_keyboard=True,
    )


def support_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📩 Новые обращения"),
            ],
            [
                KeyboardButton(text="📋 Все обращения"),
            ],
            [
                KeyboardButton(text="◀️ Админ-панель"),
            ],
        ],
        resize_keyboard=True,
    )

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def ai_settings_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="💬 Лимит текста"),
                KeyboardButton(text="🎙 Лимит голоса"),
            ],
            [
                KeyboardButton(text="📸 Лимит фото"),
                KeyboardButton(text="🎥 Лимит видео"),
            ],
            [
                KeyboardButton(text="💰 Лимит API"),
            ],
            [
                KeyboardButton(text="🔄 Обновить"),
            ],
            [
                KeyboardButton(text="◀️ Настройки"),
            ],
        ],
        resize_keyboard=True,
    )

def subscription_settings_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="💵 Цена"),
                KeyboardButton(text="📅 Срок"),
            ],
            [
                KeyboardButton(text="🎁 Пробный период"),
                KeyboardButton(text="🏷 Скидка"),
            ],
            [
                KeyboardButton(text="🔄 Обновить"),
            ],
            [
                KeyboardButton(text="◀️ Настройки"),
            ],
        ],
        resize_keyboard=True,
    )

def photo_settings_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📸 Включить / выключить"),
            ],
            [
                KeyboardButton(text="🔢 Лимит анализов"),
            ],
            [
                KeyboardButton(text="👑 Только подписчики"),
            ],
            [
                KeyboardButton(text="🔄 Обновить"),
            ],
            [
                KeyboardButton(text="◀️ Настройки"),
            ],
        ],
        resize_keyboard=True,
    )

def video_settings_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🎥 Включить / выключить"),
            ],
            [
                KeyboardButton(text="🔢 Лимит анализов"),
                KeyboardButton(text="⏱ Длительность"),
            ],
            [
                KeyboardButton(text="👑 Только подписчики"),
            ],
            [
                KeyboardButton(text="🔄 Обновить"),
            ],
            [
                KeyboardButton(text="◀️ Настройки"),
            ],
        ],
        resize_keyboard=True,
    )

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def exercises_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="➕ Добавить упражнение"),
                KeyboardButton(text="✏️ Редактировать"),
            ],
            [
                KeyboardButton(text="🗑 Удалить"),
                KeyboardButton(text="🔎 Поиск"),
            ],
            [
                KeyboardButton(text="📋 Все упражнения"),
            ],
            [
                KeyboardButton(text="◀️ Назад"),
            ],
        ],
        resize_keyboard=True,
    )


def partnership_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="➕ Добавить партнёра"),
                KeyboardButton(text="📋 Список партнёров"),
            ],
            [
                KeyboardButton(text="✏️ Редактировать"),
                KeyboardButton(text="🗑 Удалить"),
            ],
            [
                KeyboardButton(text="🔎 Поиск"),
                KeyboardButton(text="📊 Статистика"),
            ],
            [
                KeyboardButton(text="◀️ Назад"),
            ],
        ],
        resize_keyboard=True,
    )

def broadcast_settings_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📢 Создать рассылку"),
                KeyboardButton(text="📊 Статистика рассылки"),
            ],
            [
                KeyboardButton(text="⚙️ Настройки рассылки"),
            ],
            [
                KeyboardButton(text="◀️ Назад"),
            ],
        ],
        resize_keyboard=True,
    )


def admin_dashboard_keyboard():
    return ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🔄 Обновить"),
            KeyboardButton(text="👥 Пользователи"),
        ],
        [
            KeyboardButton(text="💳 Подписки"),
            KeyboardButton(text="💰 Финансы"),
        ],
        [
            KeyboardButton(text="◀️ Назад"),
        ],
    ],
    resize_keyboard=True
)



