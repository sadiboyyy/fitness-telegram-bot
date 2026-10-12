from datetime import datetime

from aiogram import F, Router
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
)

from database import conn, cursor
from keyboards.menu import main_menu
from subscription import register_user


router = Router()


fitcoins_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🪙 Мой баланс")],
        [KeyboardButton(text="📜 История FitCoins")],
        [KeyboardButton(text="🎁 Как получить FitCoins")],
        [KeyboardButton(text="🏠 Главное меню")],
    ],
    resize_keyboard=True,
)
def add_fitcoins(
    user_id: int,
    amount: int,
    reason: str,
) -> bool:
    today = datetime.now().strftime("%d.%m.%Y")

    cursor.execute(
        """
        SELECT id
        FROM fitcoin_transactions
        WHERE user_id = ?
          AND reason = ?
          AND substr(created_at, 1, 10) = ?
        LIMIT 1
        """,
        (
            user_id,
            reason,
            today,
        ),
    )

    existing_transaction = cursor.fetchone()

    if existing_transaction:
        return False

    cursor.execute(
        """
        INSERT OR IGNORE INTO fitcoins (
            user_id,
            balance
        )
        VALUES (?, 0)
        """,
        (user_id,),
    )

    cursor.execute(
        """
        UPDATE fitcoins
        SET balance = balance + ?
        WHERE user_id = ?
        """,
        (
            amount,
            user_id,
        ),
    )

    cursor.execute(
        """
        INSERT INTO fitcoin_transactions (
            user_id,
            amount,
            reason,
            created_at
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            user_id,
            amount,
            reason,
            datetime.now().strftime("%d.%m.%Y %H:%M"),
        ),
    )

    conn.commit()

    return True

def get_fitcoins_balance(user_id: int) -> int:
    cursor.execute(
        """
        SELECT balance
        FROM fitcoins
        WHERE user_id = ?
        """,
        (user_id,),
    )

    result = cursor.fetchone()

    if result is None:
        return 0

    return int(result[0])

@router.message(F.text == "🪙 FitCoins")
async def open_fitcoins(
    message: Message,
):
    register_user(message)

    balance = get_fitcoins_balance(
        message.from_user.id
    )

    await message.answer(
        "🪙 <b>FitCoins</b>\n\n"
        f"Ваш баланс: <b>{balance} FitCoins</b>\n\n"
        "Получайте монеты за активность и позже "
        "обменивайте их на дополнительные функции.",
        parse_mode="HTML",
        reply_markup=fitcoins_keyboard,
    )

@router.message(F.text == "🪙 Мой баланс")
async def show_fitcoins_balance(
    message: Message,
):
    register_user(message)

    balance = get_fitcoins_balance(
        message.from_user.id
    )

    await message.answer(
        "🪙 <b>Ваш баланс</b>\n\n"
        f"<b>{balance} FitCoins</b>",
        parse_mode="HTML",
        reply_markup=fitcoins_keyboard,
    )

@router.message(F.text == "📜 История FitCoins")
async def show_fitcoins_history(
    message: Message,
):
    register_user(message)

    cursor.execute(
        """
        SELECT amount, reason, created_at
        FROM fitcoin_transactions
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT 10
        """,
        (message.from_user.id,),
    )

    transactions = cursor.fetchall()

    if not transactions:
        await message.answer(
            "📜 У вас пока нет операций с FitCoins.",
            reply_markup=fitcoins_keyboard,
        )
        return

    text = "📜 <b>Последние операции</b>\n\n"

    for amount, reason, created_at in transactions:
        sign = "+" if amount > 0 else ""

        text += (
            f"🕒 {created_at}\n"
            f"🪙 {sign}{amount} — {reason}\n\n"
        )

    await message.answer(
        text,
        parse_mode="HTML",
        reply_markup=fitcoins_keyboard,
    )

@router.message(F.text == "🎁 Как получить FitCoins")
async def show_fitcoins_rewards(
    message: Message,
):
    await message.answer(
        "🪙 <b>Что такое FitCoins?</b>\n\n"

        "FitCoins — это внутренняя валюта Fitness AI.\n"
        "Вы получаете её за полезную активность в боте "
        "и можете тратить на дополнительные возможности.\n\n"

        "🎁 <b>Как заработать FitCoins:</b>\n\n"

        "📏 Добавить замеры — +10\n"
        "📷 Добавить фото прогресса — +10\n"
        "✅ Выполнить дневное задание — +10\n"
        "🏋️ Завершить тренировку — +20\n"
        "🔥 Продлить серию тренировок — +5\n"
        "🏆 Получить достижение — +20–100\n\n"

        "🛍 <b>На что можно потратить FitCoins:</b>\n\n"

        "🤖 Дополнительный вопрос ИИ — 20 FitCoins\n"
        "🎙 Дополнительный голосовой вопрос — 30 FitCoins\n"
        "📸 Дополнительный анализ формы — 50 FitCoins\n"
        "🍽 Анализ еды по фотографии — 40 FitCoins\n"
        "📄 PDF программы — 50 FitCoins\n"
        "🔓 Premium на 1 день — 200 FitCoins\n\n"

        "💡 FitCoins нельзя вывести в реальные деньги. "
        "Это бонусная валюта внутри Fitness AI.",
        parse_mode="HTML",
        reply_markup=fitcoins_keyboard,
    )
