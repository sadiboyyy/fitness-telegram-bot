from aiogram import Router, F
from aiogram.types import Message

from admin.router import is_admin
from keyboards.admin import admin_menu


router = Router()


@router.message(F.text == "💳 Подписки")
async def admin_subscriptions(message: Message):

    if not is_admin(message):
        return

    await message.answer(
        "💳 <b>УПРАВЛЕНИЕ ПОДПИСКАМИ</b>\n\n"
        "Здесь администратор сможет:\n\n"
        "✅ Смотреть активные подписки\n"
        "⏳ Смотреть заканчивающиеся\n"
        "❌ Смотреть истёкшие\n"
        "➕ Выдавать подписку вручную\n"
        "➖ Отменять подписку\n"
        "💎 Управлять тарифами\n\n"
        "Функции подключим к базе данных на следующем этапе.",
        parse_mode="HTML",
        reply_markup=admin_menu,
    )