
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📊 Дашборд"),
            KeyboardButton(text="👥 Пользователи"),
        ],
        [
            KeyboardButton(text="💰 Финансы"),
            KeyboardButton(text="📢 Рассылка"),
        ],
        [
            KeyboardButton(text="⚙️ Настройки бота"),
            KeyboardButton(text="🛠️ Контент"),
        ],
        [
            KeyboardButton(text="🏠 Главное меню"),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Управление Fitness AI",
)


admin_settings_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="💳 Подписки"),
            KeyboardButton(text="🤖 AI настройки"),
        ],
        [
            KeyboardButton(text="📦 Тарифы"),
            KeyboardButton(text="🔒 Ограничения"),
        ],
        [
            KeyboardButton(text="◀️ Назад"),
        ],
    ],
    resize_keyboard=True
)


users_admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🔎 Найти пользователя"),
            KeyboardButton(text="🆕 Последние регистрации"),
        ],
        [
            KeyboardButton(text="💎 С подпиской"),
            KeyboardButton(text="🆓 Без подписки"),
        ],
        [
            KeyboardButton(text="🚫 Заблокированные"),
            KeyboardButton(text="📊 Статистика пользователей"),
        ],
        [
            KeyboardButton(text="⬅️ Назад в админку"),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Управление пользователями",
)


def user_card_keyboard(
    telegram_id: int,
    is_blocked: bool = False,
):
    block_text = "✅ Разблокировать" if is_blocked else "🚫 Заблокировать"

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

class BroadcastForm(StatesGroup):
    waiting_text = State()

class PartnerSearchForm(StatesGroup):
    waiting_id = State()
    waiting_username = State()
    waiting_phone = State()

@router.message(F.text == "🏠 Главное меню")
async def admin_back_to_main(message: Message):
    await message.answer(
        "🏠 <b>Главное меню</b>",
        parse_mode="HTML",
        reply_markup=main_menu_keyboard()
    )

@router.message(F.text == "🤝 Партнёрская программа") 
async def admin_partner_program(message: Message, state: FSMContext):
      await state.clear()

      await message.answer(
          "🤝 <b>ПАРТНЁРСКАЯ ПРОГРАММА</b>\n\n"
          "Здесь можно найти партнёра и посмотреть:\n\n"
          "👤 его аккаунт\n"
          "👥 количество приведённых пользователей\n"
          "💰 заработок\n"
          "🔗 партнёрский код",
          parse_mode="HTML",
          reply_markup=admin_partner_keyboard()
      )

@router.message(F.text == "🔎 Поиск по ID") 
async def partner_search_id(message: Message, state: FSMContext):
      await state.set_state(PartnerSearchForm.waiting_id)

      await message.answer(
          "🔎 <b>ПОИСК ПАРТНЁРА ПО ID</b>\n\n"
          "Введите Telegram ID пользователя:",
          parse_mode="HTML"
      )

@router.message(PartnerSearchForm.waiting_id) 
async def partner_find_by_id( 
     message: Message, 
     state: FSMContext 
):
    try:
       user_id = int(message.text.strip())
    except ValueError:

        await message.answer(
            "❌ ID должен состоять только из цифр.\n\n"
            "Попробуйте ещё раз."
        )
        return

    partner = find_partner_by_id(user_id)

    if not partner:

        await message.answer(
            "❌ Пользователь с таким ID не найден."
        )
        return

    await show_partner_info(message, partner)

    await state.clear()

@router.message(PartnerSearchForm.waiting_id) 
async def partner_find_by_id( 
    message: Message,
    state: FSMContext ):
  try:
      user_id = int(message.text.strip())
  except ValueError:

    await message.answer(
        "❌ ID должен состоять только из цифр.\n\n"
        "Попробуйте ещё раз."
    )
    return

  partner = find_partner_by_id(user_id)

  if not partner:

      await message.answer(
          "❌ Пользователь с таким ID не найден."
      )
      return

  await show_partner_info(message, partner)

  await state.clear()

async def show_partner_info(message: Message, partner):
  (
      user_id,
      username,
      first_name,
      partner_code,
      referred_by,
      registered_at
  ) = partner

  referrals = get_partner_referrals_count(user_id)

  earnings = get_partner_earnings(user_id)

  username_text = (
      f"@{username}"
      if username
      else "Не указан"
  )

  partner_code_text = (
      partner_code
      if partner_code
      else "Не создан"
  )

  await message.answer(
      "🤝 <b>ИНФОРМАЦИЯ О ПАРТНЁРЕ</b>\n\n"

      f"👤 Имя: <b>{first_name or 'Не указано'}</b>\n"
      f"🔗 Username: <b>{username_text}</b>\n"
      f"🆔 ID: <code>{user_id}</code>\n\n"

      f"🔑 Партнёрский код: "
      f"<code>{partner_code_text}</code>\n\n"

      f"👥 Приведено пользователей: "
      f"<b>{referrals}</b>\n"

      f"💰 Заработок: "
      f"<b>${earnings:.2f}</b>\n\n"

      f"📅 Регистрация: "
      f"{registered_at or 'Неизвестно'}",

      parse_mode="HTML"
  )






