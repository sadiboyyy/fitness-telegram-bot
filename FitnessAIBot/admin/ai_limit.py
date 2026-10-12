from aiogram import Router, F
from aiogram.types import Message

from admin.router import is_admin
from keyboards.admin import admin_menu


router = Router()


@router.message(F.text == "🤖 AI / Лимиты")
async def admin_ai_limits(message: Message):

    if not is_admin(message):
        return

    await message.answer(
        "🤖 <b>AI / ЛИМИТЫ</b>\n\n"
        "💬 Текстовые AI-запросы: —\n"
        "🎙 Голосовые запросы: —\n"
        "📸 Анализы фото: —\n"
        "🎥 Анализы видео: —\n"
        "💰 Расходы API: —\n\n"
        "Здесь можно будет задавать дневные и месячные лимиты.",
        parse_mode="HTML",
        reply_markup=admin_menu,
    )