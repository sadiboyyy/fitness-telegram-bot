from datetime import datetime

from aiogram import F, Router
from aiogram.types import(
   Message,
     CallbackQuery,
       ReplyKeyboardMarkup,
         KeyboardButton,
           InlineKeyboardMarkup,
             InlineKeyboardButton,
)

from database import (
    create_partner_code,
    get_partner_earnings,
    get_referral_count,
    get_referral_list,
)
from keyboards.menu import main_menu


router = Router()

partner_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📊 Статистика партнёра")],
        [KeyboardButton(text="🔗 Моя реферальная ссылка")],
        [KeyboardButton(text="💰 Мой заработок")],
        [KeyboardButton(text="🏠 Главное меню")],
    ],
    resize_keyboard=True,
)

def create_partner(
    user_id: int,
    partner_code: str,
):
    cursor.execute(
        """
        INSERT OR IGNORE INTO partners (
            user_id,
            partner_code,
            commission_percent,
            created_at
        )
        VALUES (?, ?, 30, ?)
        """,
        (
            user_id,
            partner_code,
            datetime.now().strftime("%d.%m.%Y %H:%M"),
        ),
    )

    conn.commit()

@router.message(F.text == "🤝 Партнёрская программа")
async def partner_program(message: Message):
    user_id = message.from_user.id

    # Получаем или создаём персональный код
    partner_code = create_partner_code(user_id)

    # Количество приглашённых
    referrals = get_referral_count(user_id)

    # Получаем username бота
    bot_info = await message.bot.get_me()

    partner_link = (
        f"https://t.me/{bot_info.username}"
        f"?start=partner_{partner_code}"
    )

    await message.answer(
        "🤝 <b>ПАРТНЁРСКАЯ ПРОГРАММА</b>\n\n"

        "Приглашайте друзей и получайте вознаграждение "
        "за пользователей, которые зарегистрировались "
        "по вашей персональной ссылке.\n\n"

        "💰 <b>Комиссия:</b> 20%\n"
        "🎁 Вознаграждение за привлечённых пользователей\n"
        "📊 Статистика приглашений\n\n"

        "━━━━━━━━━━━━━━━━━━\n\n"

        "🔗 <b>Ваша партнёрская ссылка:</b>\n\n"
        f"<code>{partner_link}</code>\n\n"

        "👥 <b>Приглашено:</b> "
        f"{referrals}\n\n"

        "━━━━━━━━━━━━━━━━━━\n\n"

        "📢 Вы можете разместить свою ссылку "
        "в социальных сетях, отправить друзьям "
        "или использовать её на своих площадках.\n\n"

        "Чем больше пользователей вы приведёте, "
        "тем больше сможете заработать.",

        reply_markup=partnership_menu_keyboard(),
        parse_mode="HTML",
)
    
@router.callback_query(F.data == "partner_stats") 
async def partner_stats(callback: CallbackQuery):
    user_id = callback.from_user.id

    referrals = get_referral_count(user_id)
    list_referrals = get_referral_list(user_id)
    earnings = get_partner_earnings(user_id)

    await callback.answer()

    await callback.message.answer(
        "📊 <b>МОЯ ПАРТНЁРСКАЯ СТАТИСТИКА</b>\n\n"
        f"👥 Приглашено пользователей: <b>{referrals}</b>\n"
        f"💎 Оплатили подписку: <b>{len(list_referrals)}</b>\n"
        f"💰 Заработано: <b>${earnings:.2f}</b>\n"
        f"💳 Доступно к выплате: <b>${max(earnings - 0, 0):.2f}</b>\n\n"
        "Список приведённых пользователей будет обновляться автоматически после оплаты подписки.",
        parse_mode="HTML",
    )

@router.callback_query(F.data == "partner_terms")
async def partner_terms(callback: CallbackQuery):
  await callback.answer()

  await callback.message.answer(
      "📋 <b>УСЛОВИЯ ПАРТНЁРСКОЙ ПРОГРАММЫ</b>\n\n"

      "🤝 <b>Как это работает?</b>\n\n"
      "1️⃣ Вы получаете персональную партнёрскую ссылку.\n"
      "2️⃣ Делитесь ей с другими людьми.\n"
      "3️⃣ Пользователь переходит по вашей ссылке.\n"
      "4️⃣ Бот автоматически фиксирует приглашение.\n"
      "5️⃣ Если пользователь оформляет подписку, "
      "вы получаете партнёрское вознаграждение.\n\n"

      "━━━━━━━━━━━━━━━━━━\n\n"

      "💰 <b>КОМИССИЯ</b>\n\n"
      "Размер комиссии: <b>20%</b> от оплаченной подписки.\n\n"

      "━━━━━━━━━━━━━━━━━━\n\n"

      "📌 <b>ВАЖНО</b>\n\n"
      "• Запрещён спам.\n"
      "• Запрещена накрутка регистраций.\n"
      "• Нельзя приглашать пользователей "
      "с целью искусственного увеличения статистики.\n"
      "• Партнёрские начисления проверяются системой.\n\n"

      "При нарушении условий партнёрская программа "
      "может быть отключена.",

      parse_mode="HTML",
  ) 
  @router.callback_query(F.data == "partner_payout")
  async def partner_payout(callback: CallbackQuery): 
        user_id = callback.from_user.id
        partner_code = create_partner_code(user_id)

        await callback.answer()

        await callback.message.answer(
            "💰 <b>ЗАПРОС НА ВЫПЛАТУ</b>\n\n"
            "Для получения партнёрской выплаты напишите администратору.\n\n"
            "📋 <b>В сообщении укажите:</b>\n\n"
            f"👤 Ваш Telegram: <code>@{callback.from_user.username or 'username отсутствует'}</code>\n\n"
            "💰 Скриншот вашего партнёрского баланса\n\n"
            f"🔗 Номер партнёрской ссылки: <code>{partner_code}</code>\n\n"
            "💳 Номер банковской карты\n"
            "или\n"
            "🪙 Binance-кошелёк\n\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "💵 <b>Минимальная сумма выплаты: $20</b>\n\n"
            "После проверки данных администратор "
            "произведёт выплату.",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="📩 Написать админу",
                            url="https://t.me/YurchikBond"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="◀️ Назад",
                            callback_data="partner_main_menu"
                        )
                    ]
                ]
            ),
            parse_mode="HTML",
        )




@router.callback_query(F.data == "partner_main_menu")
async def partner_main_menu(callback: CallbackQuery):
    await callback.answer()

    await callback.message.answer(
        "🏠 <b>Главное меню</b>",
        reply_markup=main_menu,
        parse_mode="HTML",
    )


