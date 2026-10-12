from datetime import datetime

from aiogram import Router, F
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
)

from database import conn, cursor
from fitcoins import add_fitcoins

router = Router()

achievement_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🏆 Мои достижения")],
        [KeyboardButton(text="🏅 Все достижения")],
        [KeyboardButton(text="🏠 Главное меню")],
    ],
    resize_keyboard=True,
)

DEFAULT_ACHIEVEMENTS = [

    (
        "FIRST_MEASURE",

        "🥇 Первые замеры",

        "Добавить первые замеры",

        20,
    ),

    (
        "FIRST_PHOTO",

        "📸 Первое фото",

        "Добавить первое фото прогресса",

        20,
    ),

    (
        "FITCOINS100",

        "🪙 Первые 100 FitCoins",

        "Накопить 100 FitCoins",

        50,
    ),

    (
        "STREAK7",

        "🔥 Серия 7 дней",

        "Тренироваться 7 дней подряд",

        100,
    ),

]
def create_default_achievements():

    for achievement in DEFAULT_ACHIEVEMENTS:

        cursor.execute(
            """
            INSERT OR IGNORE INTO achievements(
                code,
                title,
                description,
                reward
            )
            VALUES(?,?,?,?)
            """,
            achievement,
        )

    conn.commit()


create_default_achievements()

def unlock_achievement(
    user_id,
    code,
):

    cursor.execute(
        """
        SELECT id
        FROM user_achievements
        WHERE
            user_id=?
        AND
            achievement_code=?
        """,
        (
            user_id,
            code,
        ),
    )

    if cursor.fetchone():
        return False

    cursor.execute(
        """
        SELECT
            title,
            reward
        FROM achievements
        WHERE code=?
        """,
        (code,),
    )

    achievement = cursor.fetchone()

    if achievement is None:
        return False

    title, reward = achievement

    cursor.execute(
        """
        INSERT INTO user_achievements(
            user_id,
            achievement_code,
            unlocked_at
        )
        VALUES(?,?,?)
        """,
        (
            user_id,
            code,
            datetime.now().strftime("%d.%m.%Y"),
        ),
    )

    conn.commit()

    add_fitcoins(
        user_id,
        reward,
        f"Достижение {title}",
    )

    return title, reward

@router.message(F.text == "🏆 Мои достижения")
async def my_achievements(message: Message):

    cursor.execute(
        """
        SELECT
            a.title,
            a.reward,
            u.unlocked_at
        FROM user_achievements u
        JOIN achievements a
        ON
        a.code=u.achievement_code
        WHERE
        user_id=?
        """,
        (
            message.from_user.id,
        ),
    )

    achievements = cursor.fetchall()

    if not achievements:

        await message.answer(
            "🏆 Пока достижений нет.",
            reply_markup=achievement_keyboard,
        )

        return

    text = "🏆 Ваши достижения\n\n"

    for title, reward, date in achievements:

        text += (
            f"{title}\n"

            f"🪙 +{reward}\n"

            f"📅 {date}\n\n"
        )

    await message.answer(
        text,
        reply_markup=achievement_keyboard,
    )