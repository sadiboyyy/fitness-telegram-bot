import sqlite3

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

router = Router()


class BroadcastForm(StatesGroup):
    waiting_text = State()


@router.message(F.text == "📢 Рассылки")
async def broadcast_start(message: Message, state: FSMContext):
    if message.from_user is None or message.from_user.id != 1679392581:
        return

    await state.set_state(BroadcastForm.waiting_text)
    await message.answer(
        "📢 <b>Рассылка для всех пользователей</b>\n\n"
        "Напишите текст, который хотите отправить всем пользователям.\n"
        "Для отмены используйте /cancel",
        parse_mode="HTML",
    )


@router.message(BroadcastForm.waiting_text, F.text)
async def broadcast_send(message: Message, state: FSMContext):
    if message.from_user is None or message.from_user.id != 1679392581:
        await state.clear()
        return

    text = message.text.strip()
    if not text:
        await message.answer("❌ Пустой текст. Напишите сообщение ещё раз.")
        return

    if len(text) > 1000:
        await message.answer(
            "❌ <b>Сообщение слишком длинное.</b>\n\n"
            f"Сейчас: <b>{len(text)}</b> символов.\n"
            "Максимум: <b>1000</b> символов.",
            parse_mode="HTML",
        )
        return

    conn = sqlite3.connect("fitness_bot.db")
    cursor = conn.cursor()
    cursor.execute("SELECT telegram_id FROM users")
    users = cursor.fetchall()
    conn.close()

    sent_count = 0
    fail_count = 0

    for (user_id,) in users:
        try:
            await message.bot.send_message(
                chat_id=user_id,
                text=text,
                parse_mode="HTML",
            )
            sent_count += 1
        except Exception:
            fail_count += 1

    await state.clear()

    await message.answer(
        "✅ <b>Рассылка отправлена</b>\n\n"
        f"👥 Пользователям: <b>{sent_count}</b>\n"
        f"⚠️ Не доставлено: <b>{fail_count}</b>\n\n"
        "Текст рассылки:\n"
        f"{text}",
        parse_mode="HTML",
    )


@router.message(F.text == "/cancel")
async def cancel_broadcast(message: Message, state: FSMContext):
    if message.from_user is None or message.from_user.id != 1679392581:
        return
    await state.clear()
    await message.answer("❌ Создание рассылки отменено.")


      










