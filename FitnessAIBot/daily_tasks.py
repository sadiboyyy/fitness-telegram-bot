import random
from datetime import datetime

from aiogram import F, Router
from aiogram.types import Message

from database import conn, cursor
from fitcoins import add_fitcoins


router = Router()


DAILY_TASKS = [
    {
        "title": "🚶 8 000 шагов",
        "description": "Пройдите сегодня минимум 8 000 шагов.",
    },
    {
        "title": "💧 Вода",
        "description": "Выпейте достаточно воды в течение дня.",
    },
    {
        "title": "🏋️ Тренировка",
        "description": "Выполните сегодняшнюю тренировку.",
    },
    {
        "title": "🥗 Полезный приём пищи",
        "description": "Сделайте один полноценный приём пищи с источником белка и овощами.",
    },
    {
        "title": "🧘 Восстановление",
        "description": "Сделайте 10 минут растяжки или лёгкой мобильности.",
    },
]
@router.message(F.text == "✅ Задание дня")
async def show_daily_task(message: Message):
    today = datetime.now().strftime("%Y-%m-%d")

    cursor.execute(
        """
        SELECT task_id
        FROM completed_daily_tasks
        WHERE user_id = ?
          AND completed_date = ?
        LIMIT 1
        """,
        (
            message.from_user.id,
            today,
        ),
    )

    completed = cursor.fetchone()

    if completed:
        await message.answer(
            "✅ <b>Сегодняшнее задание уже выполнено!</b>\n\n"
            "🔥 Возвращайтесь завтра за новым заданием.",
            parse_mode="HTML",
        )
        return

    # Один и тот же пользователь получает
    # стабильное задание в течение текущего дня.
    task_index = (
        message.from_user.id
        + int(datetime.now().strftime("%Y%m%d"))
    ) % len(DAILY_TASKS)

    task = DAILY_TASKS[task_index]

    await message.answer(
        "🎯 <b>Задание дня</b>\n\n"
        f"{task['title']}\n\n"
        f"{task['description']}\n\n"
        "🏆 Награда: <b>+10 FitCoins</b>\n\n"
        "После выполнения отправьте:\n"
        "<b>✅ Выполнил задание</b>",
        parse_mode="HTML",
    )
@router.message(F.text == "✅ Выполнил задание")
async def complete_daily_task(message: Message):
    today = datetime.now().strftime("%Y-%m-%d")

    cursor.execute(
        """
        SELECT id
        FROM completed_daily_tasks
        WHERE user_id = ?
          AND completed_date = ?
        LIMIT 1
        """,
        (
            message.from_user.id,
            today,
        ),
    )

    if cursor.fetchone():
        await message.answer(
            "⚠️ Вы уже получили награду за сегодняшнее задание."
        )
        return

    cursor.execute(
        """
        INSERT INTO completed_daily_tasks (
            user_id,
            task_id,
            completed_date
        )
        VALUES (?, ?, ?)
        """,
        (
            message.from_user.id,
            0,
            today,
        ),
    )

    conn.commit()

    coins_added = add_fitcoins(
        user_id=message.from_user.id,
        amount=10,
        reason="Дневное задание",
    )

    if coins_added:
        await message.answer(
            "🎉 <b>Дневное задание выполнено!</b>\n\n"
            "🪙 Вы получили <b>+10 FitCoins</b>!\n\n"
            "🔥 Продолжайте в том же духе. "
            "Завтра вас ждёт новое задание.",
            parse_mode="HTML",
        )
    else:
        await message.answer(
            "✅ Задание отмечено выполненным.\n\n"
            "Награда за сегодня уже была начислена."
        )