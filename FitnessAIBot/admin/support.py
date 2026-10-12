from aiogram import Router, F
from aiogram.types import Message

from admin.router import is_admin
from keyboards.admin import admin_menu


router = Router()


@router.message(F.text == "🆘 Поддержка")
async def admin_support(message: Message):

    if not is_admin(message):
        return

    await message.answer(
        "🆘 <b>ПОДДЕРЖКА</b>\n\n"
        "📩 Новые обращения: —\n"
        "🕒 В работе: —\n"
        "✅ Закрытые: —\n\n"
        "Здесь администратор сможет отвечать пользователям прямо через бота.",
        parse_mode="HTML",
        reply_markup=admin_menu,
    )