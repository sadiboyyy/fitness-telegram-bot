from aiogram import Router, F
from aiogram.types import Message

from admin.router import is_admin
from keyboards.admin import admin_menu


router = Router()


@router.message(F.text == "🎟 Промокоды")
async def admin_promocodes(message: Message):

    if not is_admin(message):
        return

    await message.answer(
        "🎟 <b>ПРОМОКОДЫ</b>\n\n"
        "➕ Создать промокод\n"
        "📋 Все промокоды\n"
        "✅ Активные\n"
        "❌ Отключённые\n"
        "📊 Количество использований\n\n"
        "Позже подключим скидки и бесплатные дни подписки.",
        parse_mode="HTML",
        reply_markup=admin_menu,
    )