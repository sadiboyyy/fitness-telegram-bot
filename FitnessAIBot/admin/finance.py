from aiogram import Router, F
from aiogram.types import Message

from admin.router import is_admin
from keyboards.admin import admin_menu


router = Router()


@router.message(F.text == "💰 Финансы")
async def admin_finance(message: Message):

    if not is_admin(message):
        return

    await message.answer(
        "💰 <b>ФИНАНСЫ</b>\n\n"
        "💵 Выручка сегодня: —\n"
        "📅 За 7 дней: —\n"
        "📆 За 30 дней: —\n"
        "💳 Платежей: —\n\n"
        "Здесь будет финансовая аналитика Fitness AI.",
        parse_mode="HTML",
        reply_markup=admin_menu,
    )