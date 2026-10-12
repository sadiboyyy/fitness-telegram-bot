from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from admin.router import is_admin, is_admin_id

from database import (
    get_users_count,
    get_last_users,
    find_user,
    get_user_by_id,
    toggle_user_block,
)

from keyboards.admin import (
    admin_menu,
    users_admin_menu,
    user_card_keyboard,
)


router = Router()

class AdminUserSearch(StatesGroup):
    waiting_for_user = State()

def build_user_card(user):
    (
        telegram_id,
        username,
        first_name,
        registered_at,
        is_active,
        is_blocked,
    ) = user

    name = first_name or "Без имени"
    username_text = f"@{username}" if username else "Не указан"

    date_text = (
        registered_at[:16].replace("T", " ")
        if registered_at
        else "Неизвестно"
    )

    active_text = "🟢 Активен" if is_active else "⚪ Неактивен"

    blocked_text = (
        "🚫 Заблокирован"
        if is_blocked
        else "✅ Доступ разрешён"
    )

    text = (
        "👤 <b>КАРТОЧКА ПОЛЬЗОВАТЕЛЯ</b>\n\n"
        f"Имя: <b>{name}</b>\n"
        f"Username: {username_text}\n"
        f"Telegram ID: <code>{telegram_id}</code>\n\n"
        f"📅 Регистрация: {date_text}\n"
        f"📱 Статус: {active_text}\n"
        f"🔒 Доступ: {blocked_text}"
    )

    return text

@router.message(F.text == "👥 Пользователи")
async def admin_users(message: Message):

    if not is_admin(message):
        return

    total_users = get_users_count()

    await message.answer(
        "👥 <b>УПРАВЛЕНИЕ ПОЛЬЗОВАТЕЛЯМИ</b>\n\n"
        f"Всего пользователей: <b>{total_users}</b>\n\n"
        "Выберите действие 👇",
        parse_mode="HTML",
        reply_markup=users_admin_menu,
    )
@router.message(F.text == "🆕 Последние регистрации")
async def last_users(message: Message):

    if not is_admin(message):
        return

    users = get_last_users(10)

    text = "🆕 <b>ПОСЛЕДНИЕ РЕГИСТРАЦИИ</b>\n\n"

    if not users:
        text += "Пользователей пока нет."

    else:
        for user in users:
            telegram_id, username, first_name, registered_at = user

            name = first_name or "Без имени"

            if username:
                username_text = f"@{username}"
            else:
                username_text = "нет username"

            date_text = registered_at[:16].replace("T", " ")

            text += (
                f"👤 <b>{name}</b>\n"
                f"├ {username_text}\n"
                f"├ ID: <code>{telegram_id}</code>\n"
                f"└ 📅 {date_text}\n\n"
            )

    await message.answer(
        text,
        parse_mode="HTML",
        reply_markup=users_admin_menu,
    )

@router.message(F.text == "⬅️ Назад в админку")
async def back_to_admin(message: Message):

    if not is_admin(message):
        return

    await message.answer(
        "🔐 <b>ADMIN PANEL</b>\n\n"
        "Выберите раздел 👇",
        parse_mode="HTML",
        reply_markup=admin_menu,
    )

@router.message(F.text == "🔎 Найти пользователя")
async def start_user_search(
    message: Message,
    state: FSMContext,
):
    if not is_admin(message):
        return

    await state.set_state(
        AdminUserSearch.waiting_for_user
    )

    await message.answer(
        "🔎 <b>ПОИСК ПОЛЬЗОВАТЕЛЯ</b>\n\n"
        "Отправьте:\n"
        "• Telegram ID\n"
        "или\n"
        "• @username\n\n"
        "Например:\n"
        "<code>1679392581</code>\n"
        "или <code>@username</code>",
        parse_mode="HTML",
    )

@router.message(AdminUserSearch.waiting_for_user)
async def process_user_search(
    message: Message,
    state: FSMContext,
):
    if not is_admin(message):
        await state.clear()
        return

    if not message.text:
        await message.answer(
            "❌ Отправьте Telegram ID или @username."
        )
        return

    user = find_user(message.text)

    await state.clear()

    if not user:
        await message.answer(
            "❌ <b>Пользователь не найден.</b>\n\n"
            "Проверьте Telegram ID или username.",
            parse_mode="HTML",
            reply_markup=users_admin_menu,
        )
        return

    (
        telegram_id,
        username,
        first_name,
        registered_at,
        is_active,
        is_blocked,
    ) = user

    name = first_name or "Без имени"

    username_text = (
        f"@{username}"
        if username
        else "Не указан"
    )

    date_text = registered_at[:16].replace(
        "T",
        " "
    )

    blocked_text = (
        "🚫 Заблокирован"
        if is_blocked
        else "✅ Не заблокирован"
    )

    active_text = (
        "🟢 Активен"
        if is_active
        else "⚪ Неактивен"
    )


def user_card_keyboard(
    telegram_id: int,
    is_blocked: bool = False,
):
    block_text = (
        "✅ Разблокировать"
        if is_blocked
        else "🚫 Заблокировать"
    )

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💎 Подписка",
                    callback_data=f"admin_subscription:{telegram_id}",
                ),
                InlineKeyboardButton(
                    text="💳 Платежи",
                    callback_data=f"admin_payments:{telegram_id}",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="✉️ Написать",
                    callback_data=f"admin_message:{telegram_id}",
                ),
                InlineKeyboardButton(
                    text=block_text,
                    callback_data=f"admin_block:{telegram_id}",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🔄 Обновить",
                    callback_data=f"admin_refresh:{telegram_id}",
                ),
            ],
        ]
    )
@router.callback_query(F.data.startswith("admin_refresh:"))
async def refresh_user_card(callback: CallbackQuery):

    if callback.from_user.id != 1679392581:
        await callback.answer()
        return

    telegram_id = int(
        callback.data.split(":")[1]
    )

    user = get_user_by_id(telegram_id)

    if not user:
        await callback.answer(
            "Пользователь не найден",
            show_alert=True,
        )
        return

    text = build_user_card(user)

    await callback.message.edit_text(
        text,
        parse_mode="HTML",
        reply_markup=user_card_keyboard(
            telegram_id,
            bool(user[5]),
        ),
    )

    await callback.answer("Обновлено")

@router.callback_query(F.data.startswith("admin_block:"))
async def block_user(callback: CallbackQuery):

    if not is_admin_id(callback.from_user.id):
        await callback.answer()
        return

    telegram_id = int(
        callback.data.split(":")[1]
    )

    new_status = toggle_user_block(telegram_id)

    if new_status is None:
        await callback.answer(
            "Пользователь не найден",
            show_alert=True,
        )
        return

    user = get_user_by_id(telegram_id)

    text = build_user_card(user)

    await callback.message.edit_text(
        text,
        parse_mode="HTML",
        reply_markup=user_card_keyboard(
            telegram_id,
            bool(user[5]),
        ),
    )

    if new_status:
        await callback.answer(
            "🚫 Пользователь заблокирован"
        )
    else:
        await callback.answer(
            "✅ Пользователь разблокирован"
        )