from aiogram import Router, F
from aiogram.types import Message

from admin.router import is_admin
from keyboards.admin import admin_menu


router = Router()


@router.message(F.text == "⚙️ Настройки")
async def admin_settings(message: Message):

    if not is_admin(message):
        return

    await message.answer(
        "⚙️ <b>НАСТРОЙКИ</b>\n\n"
        "💵 Цена подписки\n"
        "🎁 Пробный период\n"
        "🤖 Настройки AI\n"
        "🔔 Уведомления\n"
        "🛠 Режим обслуживания\n"
        "👨‍💼 Администраторы\n"
        "📦 Резервное копирование",
        parse_mode="HTML",
        reply_markup=admin_menu,
    )