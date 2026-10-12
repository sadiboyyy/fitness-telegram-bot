from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from keyboards.menu import partnership_menu_keyboard

from database import create_partner_code, get_referral_count

from database import get_dashboard_stats

from database import (
    get_bot_settings,
    update_bot_setting,
    get_subscription_settings,
    update_subscription_setting,
)

from .keyboards import (
    content_keyboard,
    broadcast_keyboard,
    settings_keyboard,
    support_keyboard,
    ai_settings_keyboard,
    subscription_settings_keyboard,
    voice_settings_keyboard,
    photo_settings_keyboard,
    video_settings_keyboard,
    exercises_keyboard,
    broadcast_settings_keyboard,
    

)

from database import (
    get_bot_settings,
    update_bot_setting,
    get_subscription_settings,
    update_subscription_setting,
    get_voice_settings,
    update_voice_setting,
    get_photo_settings,
    update_photo_setting,
    
)

from database import (
    add_exercise,
    get_exercises,
    find_exercises,
    delete_exercise,
)

from keyboards.admin import admin_menu

from admin.keyboards import (
    settings_keyboard,
    broadcast_settings_keyboard,
    partnership_keyboard,
)

class BroadcastState(StatesGroup):
    waiting_for_message = State()

class AISettingsState(StatesGroup):
    waiting_for_value = State()

class PhotoSettingsState(StatesGroup):
    waiting_for_value = State()

class VideoSettingsState(StatesGroup):
    waiting_for_value = State()

class ExerciseState(StatesGroup):
    waiting_for_name = State()
    waiting_for_muscle = State()
    waiting_for_description = State()
    waiting_for_search = State()
    waiting_for_delete = State()

class SubscriptionSettingsState(StatesGroup):
    waiting_for_value = State()

router = Router()

# ТВОЙ TELEGRAM ID
ADMIN_ID = 1679392581


def is_admin(message: Message) -> bool:
    return (
        message.from_user is not None
        and message.from_user.id == ADMIN_ID
    )


@router.message(Command("admin"))
async def admin_panel(message: Message):

    if not is_admin(message):
        return

    await message.answer(
        "🔐 <b>ADMIN PANEL</b>\n\n"
        "Управление Fitness AI\n\n"
        "Выберите раздел 👇",
        reply_markup=admin_menu,
        parse_mode="HTML",
    )


@router.message(F.text == "🔐 Админ-панель")
async def back_to_admin_panel(message: Message):
    
  if not is_admin(message):
      return

  await message.answer(
      "🛠 <b>Админ-панель</b>\n\n"
      "Выберите раздел:",
      reply_markup=admin_menu,
      parse_mode="HTML",
  )

@router.message(F.text == "◀️ Админ-панель")
async def back_to_admin_panel(message: Message):
    
  if not is_admin(message):
      return

  await message.answer(
      "🛠 <b>Админ-панель</b>\n\n"
      "Выберите раздел:",
      reply_markup=admin_menu,
      parse_mode="HTML",
  )

@router.message(F.text == "🤖 Настройки AI")
async def ai_settings(message: Message):
    
    if not is_admin(message):
        return

    settings = get_bot_settings()

    await message.answer(
        "🤖 <b>Настройки AI</b>\n\n"
        f"💬 Текстовые запросы: <b>{settings['text_limit']}</b> в день\n"
        f"🎙 Голосовые запросы: <b>{settings['voice_limit']}</b> в день\n"
        f"📸 Фотоанализ: <b>{settings['photo_limit']}</b> в день\n"
        f"🎥 Видеоанализ: <b>{settings['video_limit']}</b> в день\n"
        f"💰 Лимит API: <b>${settings['api_daily_limit']:.2f}</b> в день\n\n"
        "Выберите параметр, который хотите изменить:",
        reply_markup=ai_settings_keyboard(),
        parse_mode="HTML",
    )


@router.message(F.text == "🏋️ Контент")
async def admin_content(message: Message):

    if not is_admin(message):
        return

    await message.answer(
        "🏋️ <b>Управление контентом</b>\n\n"
        "Выберите раздел:",
        reply_markup=content_keyboard(),
        parse_mode="HTML",
    )
@router.message(F.text == "💪 Упражнения")
async def exercises(message: Message):


   if not is_admin(message):
    return

   await message.answer(
    "💪 <b>Управление упражнениями</b>\n\n"
    "Выберите действие:",
    reply_markup=exercises_keyboard(),
    parse_mode="HTML",
)
   
@router.message(F.text == "🥗 Питание")
async def admin_food(message: Message):

    if not is_admin(message):
        return

    await message.answer(
        "🥗 <b>Питание</b>\n\n"
        "Управление контентом питания.\n\n"
        "🥩 Продукты\n"
        "🍽 Приёмы пищи\n"
        "📋 Рационы\n"
        "💡 Советы",
        parse_mode="HTML",
    )
@router.message(F.text == "🏋️ Тренировки")
async def admin_workouts(message: Message):

    if not is_admin(message):
        return

    await message.answer(
        "🏋️ <b>Тренировки</b>\n\n"
        "Управление тренировочными программами.\n\n"
        "➕ Добавить программу\n"
        "✏️ Изменить программу\n"
        "🗑 Удалить программу",
        parse_mode="HTML",
    )
@router.message(F.text == "🧘 Медитации")
async def admin_meditations(message: Message):

    if not is_admin(message):
        return

    await message.answer(
        "🧘 <b>Медитации</b>\n\n"
        "Управление медитациями и аудиоконтентом.\n\n"
        "➕ Добавить\n"
        "✏️ Изменить\n"
        "🗑 Удалить",
        parse_mode="HTML",
    )

@router.message(F.text == "📢 Рассылка")
async def admin_broadcast(message: Message):
    if not is_admin(message):
        return

    await message.answer(
        "📢 Рассылка\nВведите текст сообщения для всех пользователей:",
        reply_markup=admin_menu
    )
@router.message(F.text == "✍️ Написать рассылку")
async def start_broadcast(message: Message, state: FSMContext):
  if not is_admin(message):
     return

  await state.set_state(BroadcastState.waiting_for_message)

  await message.answer(
      "✍️ <b>Создание рассылки</b>\n\n"
      "Введите текст, который будет отправляться пользователям.\n\n"
      "🔢 Максимум: <b>1000 символов</b>\n\n"
      "Для отмены нажмите «◀️ Назад».",
      parse_mode="HTML",
  )

@router.message(BroadcastState.waiting_for_message)
async def save_broadcast_text(message: Message, state: FSMContext):
   
    if not is_admin(message):
        return

    text = message.text.strip()

    if not text:
        await message.answer(
            "❌ Текст не может быть пустым."
        )
        return

    if len(text) > 1000:
        await message.answer(
            f"❌ Слишком длинный текст.\n\n"
            f"Максимум: <b>1000 символов</b>.\n"
            f"Сейчас: <b>{len(text)}</b> символов.",
            parse_mode="HTML",
        )
        return

    update_broadcast_setting("text", text)

    await state.clear()

    await message.answer(
        "✅ <b>Текст рассылки сохранён!</b>\n\n"
        f"📝 Символов: <b>{len(text)}</b>\n\n"
        f"{text}",
        reply_markup=broadcast_settings_keyboard(),
        parse_mode="HTML",
    )



@router.message(F.text == "⚙️ Настройки")
async def admin_settings(message: Message):

    if not is_admin(message):
        return

    await message.answer(
        "⚙️ <b>Настройки бота</b>\n\n"
        "Выберите раздел:",
        reply_markup=settings_keyboard(),
        parse_mode="HTML",
    )
@router.message(F.text == "🤖 Настройки AI")
async def ai_settings(message: Message):

    if not is_admin(message):
        return

    await message.answer(
        "🤖 <b>Настройки AI</b>\n\n"
        "Здесь будут:\n\n"
        "💬 Лимит текстовых запросов\n"
        "🎙 Лимит голосовых запросов\n"
        "📸 Лимит фотоанализа\n"
        "🎥 Лимит видеоанализа\n"
        "💰 Контроль расходов API",
        parse_mode="HTML",
    )
@router.message(F.text == "💬 Лимит текста") 
async def set_text_limit(message: Message, state: FSMContext):
    if not is_admin(message):
        return

    await state.update_data(setting_name="text_limit")
    await state.set_state(AISettingsState.waiting_for_value)

    await message.answer(
        "💬 <b>Лимит текстовых запросов</b>\n\n"
        "Введите новое количество запросов в день.\n\n"
        "Например: <code>30</code>",
        parse_mode="HTML",
    )
@router.message(F.text == "🎙 Лимит голоса") 
async def set_voice_limit(message: Message, state: FSMContext):
    if not is_admin(message):
        return

    await state.update_data(setting_name="voice_limit")
    await state.set_state(AISettingsState.waiting_for_value)

    await message.answer(
        "🎙 <b>Лимит голосовых запросов</b>\n\n"
        "Введите новое количество запросов в день.\n\n"
        "Например: <code>10</code>",
        parse_mode="HTML",
    )
@router.message(F.text == "📸 Лимит фото")
async def set_photo_limit(message: Message, state: FSMContext):
      if not is_admin(message):
          return

      await state.update_data(setting_name="photo_limit")
      await state.set_state(AISettingsState.waiting_for_value)

      await message.answer(
          "📸 <b>Лимит фотоанализа</b>\n\n"
          "Введите новое количество анализов в день.\n\n"
          "Например: <code>5</code>",
          parse_mode="HTML",
      )
@router.message(F.text == "🎥 Лимит видео") 
async def set_video_limit(message: Message, state: FSMContext):
      if not is_admin(message):
          return

      await state.update_data(setting_name="video_limit")
      await state.set_state(AISettingsState.waiting_for_value)

      await message.answer(
          "🎥 <b>Лимит видеоанализа</b>\n\n"
          "Введите новое количество анализов в день.\n\n"
          "Например: <code>3</code>",
          parse_mode="HTML",
      )
@router.message(F.text == "💰 Лимит API")
async def set_api_limit(message: Message, state: FSMContext):
      if not is_admin(message):
          return

      await state.update_data(setting_name="api_daily_limit")
      await state.set_state(AISettingsState.waiting_for_value)

      await message.answer(
          "💰 <b>Дневной лимит API</b>\n\n"
          "Введите максимальный расход в долларах.\n\n"
          "Например: <code>15</code>",
          parse_mode="HTML",
      )



@router.message(F.text == "💳 Настройки подписки")
async def subscription_settings(message: Message):

    if not is_admin(message):
        return

    await message.answer(
        "💳 <b>Настройки подписки</b>\n\n"
        "Здесь настроим:\n\n"
        "💵 Стоимость\n"
        "📅 Срок действия\n"
        "🎁 Пробный период\n"
        "💰 Скидки",
        parse_mode="HTML",
    )

@router.message(F.text == "🎙 Настройки голосового чата")
async def voice_settings(message: Message):

    if not is_admin(message):
        return

    await message.answer(
        "🎙 <b>Голосовой чат</b>\n\n"
        "Статус: ✅\n\n"
        "Здесь можно будет изменить лимиты "
        "и настройки голосового чата.",
        parse_mode="HTML",
    )

@router.message(F.text == "📸 Настройки анализа фото")
async def photo_settings(message: Message):

    if not is_admin(message):
        return

    await message.answer(
        "📸 <b>Анализ фото</b>\n\n"
        "Статус: ✅\n\n"
        "Настройки лимитов и стоимости анализа.",
        parse_mode="HTML",
    )

@router.message(F.text == "🎥 Настройки анализа видео")
async def video_settings(message: Message):

    if not is_admin(message):
        return

    await message.answer(
        "🎥 <b>Анализ видео</b>\n\n"
        "Статус: ✅\n\n"
        "Настройки лимитов и стоимости анализа.",
        parse_mode="HTML",
    )

@router.message(AISettingsState.waiting_for_value)
async def save_ai_setting(message: Message, state: FSMContext):
    if not is_admin(message):
        return

    value_text = message.text.strip().replace(",", ".")

    try:
        data = await state.get_data()
        setting_name = data.get("setting_name")

        if setting_name == "api_daily_limit":
            value = float(value_text)

            if value <= 0:
                raise ValueError
        else:
            value = int(value_text)

            if value < 0:
                raise ValueError

    except (ValueError, TypeError):
        await message.answer(
            "❌ Введите корректное число.\n\n"
            "Например:\n"
            "<code>20</code>\n"
            "или\n"
            "<code>10.50</code> для лимита API.",
            parse_mode="HTML",
        )
        return

    update_bot_setting(setting_name, value)

    await state.clear()

    settings = get_bot_settings()

    await message.answer(
        "✅ <b>Настройка сохранена!</b>\n\n"
        f"💬 Текст: <b>{settings['text_limit']}</b>\n"
        f"🎙 Голос: <b>{settings['voice_limit']}</b>\n"
        f"📸 Фото: <b>{settings['photo_limit']}</b>\n"
        f"🎥 Видео: <b>{settings['video_limit']}</b>\n"
        f"💰 API: <b>${settings['api_daily_limit']:.2f}</b>",
        reply_markup=ai_settings_keyboard(),
        parse_mode="HTML",
    )
@router.message(F.text == "🔄 Обновить")
async def refresh_ai_settings(message: Message):
    if not is_admin(message):
        return

    settings = get_bot_settings()

    await message.answer(
        "🤖 <b>Настройки AI</b>\n\n"
        f"💬 Текстовые запросы: <b>{settings['text_limit']}</b> в день\n"
        f"🎙 Голосовые запросы: <b>{settings['voice_limit']}</b> в день\n"
        f"📸 Фотоанализ: <b>{settings['photo_limit']}</b> в день\n"
        f"🎥 Видеоанализ: <b>{settings['video_limit']}</b> в день\n"
        f"💰 Лимит API: <b>${settings['api_daily_limit']:.2f}</b> в день",
        reply_markup=ai_settings_keyboard(),
        parse_mode="HTML",
    )


@router.message(F.text == "🆘 Поддержка")
async def admin_support(message: Message):

    if not is_admin(message):
        return

    await message.answer(
        "🆘 <b>Поддержка</b>\n\n"
        "Выберите раздел:",
        reply_markup=support_keyboard(),
        parse_mode="HTML",
    )

@router.message(F.text == "◀️ Админ-панель")
async def back_to_admin_panel(message: Message):
    if not is_admin(message):
      return

    await message.answer(
        "🛠 <b>Админ-панель</b>\n\n"
        "Выберите нужный раздел:",
        reply_markup=admin_menu,
        parse_mode="HTML",
    )


@router.message(F.text == "📩 Новые обращения")
async def new_support_requests(message: Message):

    if not is_admin(message):
        return

    await message.answer(
        "📩 <b>Новые обращения</b>\n\n"
        "Пока новых обращений нет.",
        parse_mode="HTML",
    )

@router.message(F.text == "📋 Все обращения")
async def all_support_requests(message: Message):

    if not is_admin(message):
        return

    await message.answer(
        "📋 <b>Все обращения</b>\n\n"
        "Здесь будет список обращений пользователей.",
        parse_mode="HTML",
    )


@router.message(F.text == "💳 Настройки подписки") 
async def subscription_settings(message: Message):
    if not is_admin(message):
        return

    settings = get_subscription_settings()

    await message.answer(
        "💳 <b>Настройки подписки</b>\n\n"
        f"💵 Стоимость: <b>${settings['price']:.2f}</b>\n"
        f"📅 Срок: <b>{settings['duration_days']} дней</b>\n"
        f"🎁 Пробный период: <b>{settings['trial_days']} дней</b>\n"
        f"🏷 Скидка: <b>{settings['discount_percent']}%</b>\n\n"
        "Выберите параметр для изменения:",
        reply_markup=subscription_settings_keyboard(),
        parse_mode="HTML",
    )

@router.message(F.text == "💵 Цена")
async def subscription_price(message: Message, state: FSMContext):
    if not is_admin(message):
        return

    await state.update_data(setting_name="price")
    await state.set_state(SubscriptionSettingsState.waiting_for_value)

    await message.answer(
        "💵 <b>Стоимость подписки</b>\n\n"
        "Введите новую стоимость в долларах.\n\n"
        "Например: <code>14.99</code>",
        parse_mode="HTML",
    )
@router.message(F.text == "📅 Срок")
async def subscription_duration(message: Message, state: FSMContext):
    if not is_admin(message):
        return

    await state.update_data(setting_name="duration_days")
    await state.set_state(SubscriptionSettingsState.waiting_for_value)

    await message.answer(
        "📅 <b>Срок подписки</b>\n\n"
        "Введите количество дней.\n\n"
        "Например: <code>30</code>",
        parse_mode="HTML",
    ) 

@router.message(F.text == "🎁 Пробный период") 
async def subscription_trial(message: Message, state: FSMContext):
      if not is_admin(message):
          return

      await state.update_data(setting_name="trial_days")
      await state.set_state(SubscriptionSettingsState.waiting_for_value)

      await message.answer(
          "🎁 <b>Пробный период</b>\n\n"
          "Введите количество бесплатных дней.\n\n"
          "Например: <code>3</code>",
          parse_mode="HTML",
      )

@router.message(F.text == "🏷 Скидка")
async def subscription_discount(message: Message, state: FSMContext):
    
    if not is_admin(message):
        return

    await state.update_data(setting_name="discount_percent")
    await state.set_state(SubscriptionSettingsState.waiting_for_value)

    await message.answer(
        "🏷 <b>Скидка</b>\n\n"
        "Введите размер скидки в процентах.\n\n"
        "Например: <code>20</code>",
        parse_mode="HTML",
    )

@router.message(SubscriptionSettingsState.waiting_for_value)
async def save_subscription_setting( message: Message, state: FSMContext, ):
    if not is_admin(message):
       return

    value_text = message.text.strip().replace(",", ".")

    data = await state.get_data()
    setting_name = data.get("setting_name")

    try:
        if setting_name == "price":
            value = float(value_text)

            if value <= 0:
                raise ValueError

        else:
            value = int(value_text)

            if value < 0:
                raise ValueError

            if setting_name == "discount_percent" and value > 100:
                raise ValueError

    except (ValueError, TypeError):
        await message.answer(
            "❌ Некорректное значение.\n\n"
            "Попробуйте ещё раз.",
        )
        return

    update_subscription_setting(setting_name, value)

    await state.clear()

    settings = get_subscription_settings()

    await message.answer(
        "✅ <b>Настройка подписки сохранена!</b>\n\n"
        f"💵 Стоимость: <b>${settings['price']:.2f}</b>\n"
        f"📅 Срок: <b>{settings['duration_days']} дней</b>\n"
        f"🎁 Пробный период: <b>{settings['trial_days']} дней</b>\n"
        f"🏷 Скидка: <b>{settings['discount_percent']}%</b>",
        reply_markup=subscription_settings_keyboard(),
        parse_mode="HTML",
    )


@router.message(F.text == "📸 Настройки анализа фото")
async def photo_settings(message: Message):
    
  if not is_admin(message):
    return

  settings = get_photo_settings()

  status = "🟢 Включён" if settings["enabled"] else "🔴 Выключен"
  access = (
      "👑 Только подписчики"
      if settings["subscribers_only"]
      else "👥 Все пользователи"
  )

  await message.answer(
      "📸 <b>Настройки анализа фото</b>\n\n"
      f"Статус: <b>{status}</b>\n"
      f"🔢 Лимит: <b>{settings['daily_limit']}</b> анализов в день\n"
      f"🔐 Доступ: <b>{access}</b>\n\n"
      "Выберите параметр:",
      reply_markup=photo_settings_keyboard(),
      parse_mode="HTML",
  )

@router.message(F.text == "📸 Включить / выключить")
async def toggle_photo(message: Message):
  if not is_admin(message):
    return

  settings = get_photo_settings()

  new_value = 0 if settings["enabled"] else 1

  update_photo_setting("enabled", new_value)

  status = "🟢 включён" if new_value else "🔴 выключен"

  await message.answer(
      f"✅ Анализ фото теперь <b>{status}</b>.",
      reply_markup=photo_settings_keyboard(),
      parse_mode="HTML",
  )

@router.message(F.text == "🔢 Лимит анализов") 
async def photo_daily_limit(message: Message, state: FSMContext):
  if not is_admin(message):
    return

  await state.update_data(setting_name="daily_limit")
  await state.set_state(PhotoSettingsState.waiting_for_value)

  await message.answer(
      "🔢 <b>Лимит анализа фото</b>\n\n"
      "Введите количество анализов в день.\n\n"
      "Например: <code>5</code>",
      parse_mode="HTML",
  )

@router.message(F.text == "👑 Только подписчики")
async def toggle_photo_subscribers(message: Message):
  if not is_admin(message):
    return

  settings = get_photo_settings()

  new_value = 0 if settings["subscribers_only"] else 1

  update_photo_setting("subscribers_only", new_value)

  access = (
      "👑 только подписчики"
      if new_value
      else "👥 все пользователи"
  )

  await message.answer(
      f"✅ Доступ к анализу фото: <b>{access}</b>.",
      reply_markup=photo_settings_keyboard(),
      parse_mode="HTML",
  )


@router.message(PhotoSettingsState.waiting_for_value) 
async def save_photo_setting( message: Message, state: FSMContext, ):
  if not is_admin(message):
    return

  try:
      value = int(message.text.strip())

      if value <= 0:
          raise ValueError

  except (ValueError, TypeError):

      await message.answer(
          "❌ Введите положительное целое число.\n\n"
          "Например: <code>5</code>",
          parse_mode="HTML",
      )

      return

  data = await state.get_data()
  setting_name = data.get("setting_name")

  update_photo_setting(setting_name, value)

  await state.clear()

  settings = get_photo_settings()

  status = "🟢 Включён" if settings["enabled"] else "🔴 Выключен"

  access = (
      "👑 Только подписчики"
      if settings["subscribers_only"]
      else "👥 Все пользователи"
  )

  await message.answer(
      "✅ <b>Настройка сохранена!</b>\n\n"
      f"Статус: <b>{status}</b>\n"
      f"🔢 Лимит: <b>{settings['daily_limit']} анализов в день</b>\n"
      f"🔐 Доступ: <b>{access}</b>",
      reply_markup=photo_settings_keyboard(),
      parse_mode="HTML",
  ) 

@router.message(F.text == "🔄 Обновить")
async def refresh_photo_settings(message: Message):
  if not is_admin(message):
    return

  settings = get_photo_settings()

  status = "🟢 Включён" if settings["enabled"] else "🔴 Выключен"

  access = (
      "👑 Только подписчики"
      if settings["subscribers_only"]
      else "👥 Все пользователи"
  )

  await message.answer(
      "📸 <b>Настройки анализа фото</b>\n\n"
      f"Статус: <b>{status}</b>\n"
      f"🔢 Лимит: <b>{settings['daily_limit']} анализов в день</b>\n"
      f"🔐 Доступ: <b>{access}</b>",
      reply_markup=photo_settings_keyboard(),
      parse_mode="HTML",
  )

@router.message(F.text == "🎥 Настройки анализа видео")
async def video_settings(message: Message):
  if not is_admin(message):
    return

  settings = get_video_settings()

  status = "🟢 Включён" if settings["enabled"] else "🔴 Выключен"

  access = (
      "👑 Только подписчики"
      if settings["subscribers_only"]
      else "👥 Все пользователи"
  )

  await message.answer(
      "🎥 <b>Настройки анализа видео</b>\n\n"
      f"Статус: <b>{status}</b>\n"
      f"🔢 Лимит: <b>{settings['daily_limit']}</b> анализов в день\n"
      f"⏱ Максимальная длительность: "
      f"<b>{settings['max_duration']} сек.</b>\n"
      f"🔐 Доступ: <b>{access}</b>\n\n"
      "Выберите параметр:",
      reply_markup=video_settings_keyboard(),
      parse_mode="HTML",
  )

@router.message(F.text == "🎥 Включить / выключить")
async def toggle_video(message: Message):
  if not is_admin(message):
    return

  settings = get_video_settings()

  new_value = 0 if settings["enabled"] else 1

  update_video_setting("enabled", new_value)

  status = "🟢 включён" if new_value else "🔴 выключен"

  await message.answer(
      f"✅ Анализ видео теперь <b>{status}</b>.",
      reply_markup=video_settings_keyboard(),
      parse_mode="HTML",
  )

@router.message(F.text == "🎥 Настройки анализа видео")
async def video_settings(message: Message):
  if not is_admin(message):
    return

  settings = get_video_settings()

  status = "🟢 Включён" if settings["enabled"] else "🔴 Выключен"

  access = (
      "👑 Только подписчики"
      if settings["subscribers_only"]
      else "👥 Все пользователи"
  )

  await message.answer(
      "🎥 <b>Настройки анализа видео</b>\n\n"
      f"Статус: <b>{status}</b>\n"
      f"🔢 Лимит: <b>{settings['daily_limit']}</b> анализов в день\n"
      f"⏱ Максимальная длительность: "
      f"<b>{settings['max_duration']} сек.</b>\n"
      f"🔐 Доступ: <b>{access}</b>\n\n"
      "Выберите параметр:",
      reply_markup=video_settings_keyboard(),
      parse_mode="HTML",
  )

@router.message(F.text == "🎥 Включить / выключить")
async def toggle_video(message: Message):
  if not is_admin(message):
    return

  settings = get_video_settings()

  new_value = 0 if settings["enabled"] else 1

  update_video_setting("enabled", new_value)

  status = "🟢 включён" if new_value else "🔴 выключен"

  await message.answer(
      f"✅ Анализ видео теперь <b>{status}</b>.",
      reply_markup=video_settings_keyboard(),
      parse_mode="HTML",
  ) 

@router.message(F.text == "🔢 Лимит анализов")
async def video_daily_limit(message: Message, state: FSMContext):
  if not is_admin(message):
    return

  await state.update_data(setting_name="daily_limit")
  await state.set_state(VideoSettingsState.waiting_for_value)

  await message.answer(
      "🔢 <b>Лимит анализа видео</b>\n\n"
      "Введите количество анализов в день.\n\n"
      "Например: <code>3</code>",
      parse_mode="HTML",
  )

@router.message(F.text == "⏱ Длительность")
async def video_max_duration(message: Message, state: FSMContext):
  if not is_admin(message):
    return

  await state.update_data(setting_name="max_duration")
  await state.set_state(VideoSettingsState.waiting_for_value)

  await message.answer(
      "⏱ <b>Максимальная длительность видео</b>\n\n"
      "Введите максимальную длительность в секундах.\n\n"
      "Например: <code>60</code>",
      parse_mode="HTML",
  )

@router.message(F.text == "👑 Только подписчики")
async def toggle_video_subscribers(message: Message):
  if not is_admin(message):
    return

  settings = get_video_settings()

  new_value = 0 if settings["subscribers_only"] else 1

  update_video_setting("subscribers_only", new_value)

  access = (
      "👑 только подписчики"
      if new_value
      else "👥 все пользователи"
  )

  await message.answer(
      f"✅ Доступ к анализу видео: <b>{access}</b>.",
      reply_markup=video_settings_keyboard(),
      parse_mode="HTML",
  )  

@router.message(VideoSettingsState.waiting_for_value)
async def save_video_setting( message: Message, state: FSMContext, ):
  if not is_admin(message):
    return

  try:
      value = int(message.text.strip())

      if value <= 0:
          raise ValueError

  except (ValueError, TypeError):

      await message.answer(
          "❌ Введите положительное целое число.\n\n"
          "Например: <code>60</code>",
          parse_mode="HTML",
      )

      return

  data = await state.get_data()
  setting_name = data.get("setting_name")

  update_video_setting(setting_name, value)

  await state.clear()

  settings = get_video_settings()

  status = "🟢 Включён" if settings["enabled"] else "🔴 Выключен"

  access = (
      "👑 Только подписчики"
      if settings["subscribers_only"]
      else "👥 Все пользователи"
  )

  await message.answer(
      "✅ <b>Настройка сохранена!</b>\n\n"
      f"Статус: <b>{status}</b>\n"
      f"🔢 Лимит: <b>{settings['daily_limit']}</b> анализов в день\n"
      f"⏱ Длительность: <b>{settings['max_duration']} сек.</b>\n"
      f"🔐 Доступ: <b>{access}</b>",
      reply_markup=video_settings_keyboard(),
      parse_mode="HTML",
  ) 

@router.message(F.text == "🔄 Обновить")
async def refresh_video_settings(message: Message):
  if not is_admin(message):
     return

  settings = get_video_settings()

  status = "🟢 Включён" if settings["enabled"] else "🔴 Выключен"

  access = (
      "👑 Только подписчики"
      if settings["subscribers_only"]
      else "👥 Все пользователи"
  )

  await message.answer(
      "🎥 <b>Настройки анализа видео</b>\n\n"
      f"Статус: <b>{status}</b>\n"
      f"🔢 Лимит: <b>{settings['daily_limit']}</b> анализов в день\n"
      f"⏱ Длительность: <b>{settings['max_duration']} сек.</b>\n"
      f"🔐 Доступ: <b>{access}</b>",
      reply_markup=video_settings_keyboard(),
      parse_mode="HTML",
  ) 

@router.message(F.text == "💪 Упражнения")
async def admin_exercises(message: Message):
  if not is_admin(message):
    return

  await message.answer(
      "💪 <b>Управление упражнениями</b>\n\n"
      "Здесь ты можешь управлять базой упражнений.",
      reply_markup=exercises_keyboard(),
      parse_mode="HTML",
  )

@router.message(F.text == "➕ Добавить упражнение")
async def add_exercise_start( message: Message, state: FSMContext, ):
  if not is_admin(message):
    return

  await state.set_state(ExerciseState.waiting_for_name)

  await message.answer(
      "➕ <b>Добавление упражнения</b>\n\n"
      "Введите название упражнения:",
      parse_mode="HTML",
  )  



@router.message(ExerciseState.waiting_for_name)
async def exercise_name( message: Message, state: FSMContext, ):
  if not is_admin(message):
    return

  await state.update_data(name=message.text)

  await state.set_state(
      ExerciseState.waiting_for_muscle
  )

  await message.answer(
      "💪 Введите мышечную группу.\n\n"
      "Например:\n"
      "Грудь\n"
      "Спина\n"
      "Ноги\n"
      "Плечи\n"
      "Бицепс\n"
      "Трицепс"
  )

@router.message(ExerciseState.waiting_for_muscle)
async def exercise_muscle( message: Message, state: FSMContext, ):
  if not is_admin(message):
    return

  await state.update_data(
      muscle_group=message.text
  )

  await state.set_state(
      ExerciseState.waiting_for_description
  )

  await message.answer(
      "📝 Введите описание или совет по технике.\n\n"
      "Например:\n"
      "«Не прогибайте поясницу и контролируйте движение»"
  ) 

@router.message(ExerciseState.waiting_for_description)
async def exercise_description(
    message: Message,
    state: FSMContext, 
):
 
    if not is_admin(message):
        return

    data = await state.get_data()

    exercise_id = add_exercise(
        name=data["name"],
        muscle=data["muscle_group"],
        exercise_type="strength",
        tip=message.text,
        place="gym",
  )

    await state.clear()

    await message.answer(
        "✅ <b>Упражнение добавлено!</b>\n\n"
        f"🆔 ID: <b>{exercise_id}</b>\n"
        f"💪 Название: <b>{data['name']}</b>\n"
        f"🎯 Группа: <b>{data['muscle_group']}</b>\n"
        f"📝 Совет: {message.text}",
        reply_markup=exercises_keyboard(),
        parse_mode="HTML",
    ) 

@router.message(F.text == "🔎 Поиск")
async def search_exercise_start( message: Message, state: FSMContext, ):
    if not is_admin(message):
      return

    await state.set_state(
        ExerciseState.waiting_for_search
    )

    await message.answer(
        "🔎 <b>Поиск упражнения</b>\n\n"
        "Введите название упражнения.\n\n"
        "Например:\n"
        "<code>жим</code>",
        parse_mode="HTML",
    )

@router.message(ExerciseState.waiting_for_search) 
async def search_exercise( message: Message, state: FSMContext, ):
   if not is_admin(message):
    return

    search = message.text.strip()

    exercises = find_exercises(search)

    await state.clear()

    if not exercises:
        await message.answer(
            "❌ Упражнения не найдены.",
            reply_markup=exercises_keyboard(),
        )
        return

    text = "🔎 <b>Результаты поиска</b>\n\n"

    for exercise in exercises:
        exercise_id, name, muscle, description = exercise

        text += (
            f"🆔 <b>{exercise_id}</b>\n"
            f"💪 {name}\n"
            f"🎯 {muscle}\n"
            f"📝 {description or 'Нет описания'}\n\n"
        )

    await message.answer(
        text,
        reply_markup=exercises_keyboard(),
        parse_mode="HTML",
    )

@router.message(F.text == "📋 Все упражнения")
async def exercise_list(message: Message):
   
    if not is_admin(message):
        return

    exercises = get_exercises()

    if not exercises:
      await message.answer(
          "📋 База упражнений пока пустая.",
          reply_markup=exercises_keyboard(),
      )
      return

    text = "📋 <b>База упражнений</b>\n\n"

    for exercise in exercises:
        exercise_id, name, muscle, description = exercise

        text += (
            f"🆔 <b>{exercise_id}</b> — "
            f"<b>{name}</b>\n"
            f"🎯 {muscle}\n"
            f"📝 {description or 'Нет описания'}\n\n"
        )

      # Telegram имеет ограничение на размер сообщения
    if len(text) <= 4000:
        await message.answer(
            text,
            reply_markup=exercises_keyboard(),
            parse_mode="HTML",
        )
        return

    # Если упражнений много — разбиваем сообщение
    parts = []
    current = "📋 <b>База упражнений</b>\n\n"

    for exercise in exercises:
        exercise_id, name, muscle, description = exercise

        item = (
            f"🆔 <b>{exercise_id}</b> — "
            f"<b>{name}</b>\n"
            f"🎯 {muscle}\n"
            f"📝 {description or 'Нет описания'}\n\n"
        )

        if len(current) + len(item) > 4000:
            parts.append(current)
            current = ""

        current += item

    if current:
        parts.append(current)

    for part in parts:
        await message.answer(
            part,
            parse_mode="HTML",
        )

    await message.answer(
        "Выберите действие:",
        reply_markup=exercises_keyboard(),
    )

@router.message(F.text == "🗑 Удалить упражнение")
async def delete_exercise_start(
    message: Message, 
    state: FSMContext,
 ):
    if not is_admin(message):
        return

    await state.set_state(
        ExerciseState.waiting_for_delete
    )

    await message.answer(
        "🗑 <b>Удаление упражнения</b>\n\n"
        "Введите ID упражнения.\n\n"
        "Например:\n"
        "<code>12</code>",
        parse_mode="HTML",
    )

@router.message(ExerciseState.waiting_for_delete)
async def delete_exercise_confirm( message: Message, state: FSMContext, ):
   if not is_admin(message):
    return

    try:
        exercise_id = int(message.text.strip())
    except (ValueError, TypeError):

        await message.answer(
            "❌ ID должен быть числом.\n\n"
            "Например: <code>12</code>",
            parse_mode="HTML",
        )

        return

    deleted = delete_exercise(exercise_id)

    await state.clear()

    if not deleted:
        await message.answer(
            f"❌ Упражнение с ID <b>{exercise_id}</b> не найдено.",
            reply_markup=exercises_keyboard(),
            parse_mode="HTML",
        )
        return

    await message.answer(
        f"✅ Упражнение с ID <b>{exercise_id}</b> удалено.",
        reply_markup=exercises_keyboard(),
        parse_mode="HTML",
    )

def broadcast_settings_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="✍️ Написать рассылку"),
            ],
            [
                KeyboardButton(text="▶️ Включить рассылку"),
                KeyboardButton(text="⏸ Выключить рассылку"),
            ],
            [
                KeyboardButton(text="📊 Статус рассылки"),
            ],
            [
                KeyboardButton(text="🔢 Лимит символов"),
                KeyboardButton(text="⏱ Интервал"),
            ],
            [
                KeyboardButton(text="◀️ Назад"),
            ],
        ],
        resize_keyboard=True,
    )

@router.message(F.text == "🤝 Партнёрство")
async def admin_partnership(message: Message):
    if not is_admin(message):
        return

    await message.answer(
        "🤝 <b>Партнёрство</b>\n\n"
        "Выберите действие:",
        reply_markup=partnership_keyboard(),
        parse_mode="HTML",
    )


@router.message(F.text == "🤝 Партнёрская программа")
async def partner_program(message: Message):
    user_id = message.from_user.id

    partner_code = create_partner_code(user_id)
    referrals = get_referral_count(user_id)

    me = await message.bot.get_me()

    partner_link = (
        f"https://t.me/{me.username}?start=partner_{partner_code}"
    )

    await message.answer(
        "🤝 <b>ПАРТНЁРСКАЯ ПРОГРАММА</b>\n\n"

        "Приглашайте друзей и получайте вознаграждение "
        "за пользователей, которые пришли по вашей "
        "персональной ссылке.\n\n"

        "💰 <b>Комиссия:</b> 20%\n"
        "🎁 Получайте вознаграждение за привлечённых пользователей\n"
        "📊 Следите за своей статистикой\n\n"

        "━━━━━━━━━━━━━━━━━━\n\n"

        "🔗 <b>Ваша партнёрская ссылка:</b>\n\n"
        f"<code>{partner_link}</code>\n\n"

        "👥 <b>Приглашено:</b> "
        f"{referrals}\n\n"

        "━━━━━━━━━━━━━━━━━━\n\n"

        "Поделитесь ссылкой с друзьями, "
        "в социальных сетях или разместите её "
        "на своих площадках.",
        
        reply_markup=partnership_menu_keyboard(),
        parse_mode="HTML",
    )

@router.message(lambda message: message.text == "📊 Дашборд")
async def admin_dashboard(message: Message):
   if not is_admin(message):
    return

    try:
        stats = get_dashboard_stats()

        text = (
            "📊 <b>АДМИН-ДАШБОРД</b>\n\n"

            f"👥 <b>Всего пользователей:</b> "
            f"{stats['total_users']}\n"

            f"🆕 <b>Новых сегодня:</b> "
            f"{stats['new_today']}\n"

            f"📅 <b>Новых за 7 дней:</b> "
            f"{stats['new_week']}\n\n"

            f"💎 <b>Активных подписок:</b> "
            f"{stats['active_subscriptions']}\n"

            f"🆓 <b>Без подписки:</b> "
            f"{stats['free_users']}\n"

            f"⏳ <b>Заканчиваются в течение 7 дней:</b> "
            f"{stats['expiring_soon']}\n\n"

            f"🤝 <b>Партнёров:</b> "
            f"{stats['partners']}\n"
        )

        await message.answer(
            text,
            parse_mode="HTML",
            reply_markup=admin_dashboard_keyboard()
        )

    except Exception as e:

        print("Ошибка Дашборда:", e)

        await message.answer(
            "❌ Не удалось загрузить статистику.\n\n"
            f"<code>{e}</code>",
            parse_mode="HTML"
        )

@router.message(lambda message: message.text == "🔄 Обновить")
async def refresh_dashboard(message: Message):
   if not is_admin(message):
    return

    stats = get_dashboard_stats()

    text = (
        "📊 <b>АДМИН-ДАШБОРД</b>\n\n"

        f"👥 <b>Всего пользователей:</b> {stats['total_users']}\n"
        f"🆕 <b>Новых сегодня:</b> {stats['new_today']}\n"
        f"📅 <b>Новых за 7 дней:</b> {stats['new_week']}\n\n"

        f"💎 <b>Активных подписок:</b> "
        f"{stats['active_subscriptions']}\n"

        f"🆓 <b>Без подписки:</b> "
        f"{stats['free_users']}\n"

        f"⏳ <b>Заканчиваются:</b> "
        f"{stats['expiring_soon']}\n\n"

        f"🤝 <b>Партнёров:</b> {stats['partners']}\n"
    )

    await message.answer(
        text,
        parse_mode="HTML",
        reply_markup=admin_dashboard_keyboard()
    )

@router.message(F.text == "◀️ Настройки")
async def back_to_main_menu(message: Message):
    await message.answer(
        "◀️ Настройки",
        reply_markup=main_menu_keyboard
    )

  





def is_admin_id(user_id: int) -> bool:
    return user_id == ADMIN_ID