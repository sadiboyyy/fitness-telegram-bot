from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

exercise_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[

        [
            InlineKeyboardButton(
                text="📸 Фото",
                callback_data="exercise_photo",
            ),

            InlineKeyboardButton(
                text="🎥 Видео",
                callback_data="exercise_video",
            ),
        ],

        [
            InlineKeyboardButton(
                text="📖 Техника",
                callback_data="exercise_info",
            )
        ],

        [
            InlineKeyboardButton(
                text="🎥 Проверить мою технику",
                callback_data="check_my_technique",
            )
        ],

        [
            InlineKeyboardButton(
                text="➡ Следующее упражнение",
                callback_data="next_exercise",
            )
        ],

        [
            InlineKeyboardButton(
                text="✅ Выполнил",
                callback_data="exercise_done",
            )
        ],

    ]
)