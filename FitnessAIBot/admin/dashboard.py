from aiogram import Router, F
from aiogram.types import Message

from database import (
    get_users_count,
    get_users_today_count,
    get_users_week_count,
    get_users_month_count,
)

from keyboards.admin import admin_menu
from admin.router import is_admin


router = Router()


@router.message(F.text == "📊 Дашборд")
async def show_dashboard(message: Message):

    if not is_admin(message):
        return

    total_users = get_users_count()
    today_users = get_users_today_count()
    week_users = get_users_week_count()
    month_users = get_users_month_count()

    text = (
        "📊 <b>ДАШБОРД</b>\n\n"

        "👥 <b>Пользователи</b>\n"
        f"├ Всего: <b>{total_users}</b>\n"
        f"├ Сегодня: <b>+{today_users}</b>\n"
        f"├ За 7 дней: <b>+{week_users}</b>\n"
        f"└ За 30 дней: <b>+{month_users}</b>\n\n"

        "💳 <b>Подписки</b>\n"
        "├ Активных: <b>—</b>\n"
        "└ Истекают скоро: <b>—</b>\n\n"

        "💰 <b>Финансы</b>\n"
        "├ Сегодня: <b>—</b>\n"
        "└ За 30 дней: <b>—</b>\n\n"

        "🤖 <b>AI</b>\n"
        "└ Расходы: <b>—</b>\n\n"

        "🟢 Бот работает"
    )

    await message.answer(
        text,
        parse_mode="HTML",
        reply_markup=admin_menu,
    )