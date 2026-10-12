
from email import message

from openai import OpenAI
from config import OPENAI_API_KEY
from config import BOT_TOKEN

import json 
import os 
import base64
from keyboards.exercise import exercise_keyboard 
from keyboards.menu import (
    main_menu,
    cancel_menu,
    ai_menu,
    user_main_menu,
    user_settings_menu,
)
from keyboards.admin import admin_menu, admin_settings_menu
from keyboards.workout import goal_keyboard, experience_keyboard, days_keyboard, place_keyboard
from keyboards.facts import facts_menu 
from nutritions import router as nutrition_router
from voice_chat import router as voice_chat_router
from workout_reminders import router as reminders_router
from scheduler import scheduler

from states.workout import WorkoutForm 
import asyncio
from video_analyzer import extract_frames 
from vision import analyze_frames

from facts_ai import generate_fact
from workouts import create_workout_program
from aiogram import F
from aiogram.filters import Command
from aiogram.types import BotCommand, KeyboardButton, ReplyKeyboardMarkup
from handlers.progress import router as progress_router
from subscription import router as subscription_router
from fitcoins import router as fitcoins_router 
from daily_tasks import router as daily_tasks_router
from payments import router as payments_router
from achievements import (router as achievements_router)
from handlers.meditation import router as meditation_router 
from partner import router as partner_router 
from handlers.stretching import stretching_router
from admin.router import router as admin_router 
from admin.users import router as admin_users_router
from admin.dashboard import router as admin_dashboard_router


from database import (
    conn,
    cursor,
    create_users_table,
    add_user,
    get_users_count,
    get_last_users,
    get_subscription_status,
    get_expiring_subscriptions,
)


# Временно храним настройки программ пользователей в памяти.
# После перезапуска бота данные удалятся.
user_workout_settings = {}

# Номер варианта программы каждого пользователя.
user_program_versions = {}

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, FSInputFile 



from keyboards.workout  import (
    goal_keyboard,
    experience_keyboard,
    days_keyboard,
    place_keyboard

)
from admin.subscriptions import router as admin_subscriptions_router
from admin.finance import router as admin_finance_router
from admin.broadcasts import router as admin_broadcasts_router
from admin.promocodes import router as admin_promocodes_router
from admin.ai_limit import router as admin_ai_limits_router
from admin.support import router as admin_support_router
from admin.settings import router as admin_settings_router


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_router(nutrition_router)
dp.include_router(voice_chat_router)
dp.include_router(reminders_router)
dp.include_router(progress_router)
dp.include_router(subscription_router)
dp.include_router(fitcoins_router)
dp.include_router(daily_tasks_router)
dp.include_router(payments_router)
dp.include_router(achievements_router)
dp.include_router(meditation_router)
dp.include_router(partner_router)
dp.include_router(stretching_router) 


dp.include_router(admin_router)
dp.include_router(admin_dashboard_router)
dp.include_router(admin_users_router)
dp.include_router(admin_subscriptions_router)
dp.include_router(admin_finance_router)
dp.include_router(admin_broadcasts_router)
dp.include_router(admin_promocodes_router)
dp.include_router(admin_ai_limits_router)

dp.include_router(admin_support_router)
dp.include_router(admin_settings_router)

# dp.include_router(fallback_router)


# Временное хранение прогресса.
# После перезапуска бота данные удалятся.
users_progress: dict[int, list[float]] = {}
ADMIN_ID = 1679392581

class WorkoutForm(StatesGroup):
    height = State()
    weight = State()
    goal = State()
    experience = State()
    place = State()
    days = State()
    body_photo = State()
    exercise_video = State()
    exercise_info = State()

class CaloriesForm(StatesGroup):
    gender = State()
    age = State()
    height = State()
    weight = State()
    activity = State()
    goal = State()



class AIForm(StatesGroup):
    question = State()

class BodyAnalysisForm(StatesGroup):
    photo = State()

class ExerciseVideoForm(StatesGroup):
    video = State()
    
@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()

    if message.from_user is None:
        return

    add_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
    )

    text = (message.text or "").strip()
    payload = ""
    if text.startswith("/start"):
        parts = text.split(maxsplit=1)
        if len(parts) > 1:
            payload = parts[1].strip()

    if payload.startswith("partner_"):
        partner_code = payload.replace("partner_", "", 1)
        cursor.execute(
            "SELECT user_id FROM users WHERE partner_code = ?",
            (partner_code,),
        )
        partner = cursor.fetchone()
        if partner and partner[0] != message.from_user.id:
            cursor.execute(
                "UPDATE users SET referred_by = ? WHERE user_id = ? AND referred_by IS NULL",
                (partner[0], message.from_user.id),
            )
            conn.commit()

    if message.from_user.id == ADMIN_ID:
        await message.answer(
            "👑 Админ-панель активна\n\n"
            "Выберите раздел ниже:",
            reply_markup=admin_menu,
        )
        return

    status = get_subscription_status(message.from_user.id)

    if status["active"]:
        if status["days_left"] <= 3:
            await message.answer(
                "⏳ <b>Подписка скоро закончится</b>\n\n"
                f"План: <b>{status['plan']}</b>\n"
                f"Осталось дней: <b>{status['days_left']}</b>\n\n"
                "Обновите подписку, чтобы продолжить пользоваться ботом.",
                parse_mode="HTML",
            )
        await message.answer(
            "Добро пожаловать! 👋\n\n"
            "Выберите раздел ниже:",
            reply_markup=user_main_menu,
        )
        return

    await message.answer(
        "❌ <b>Доступ к боту закрыт</b>\n\n"
        "Подписка не активна или просрочена.\n\n"
        "💵 Пользователь: <b>$10/месяц</b>\n"
        "🏢 Бизнес: <b>$50/месяц</b>\n\n"
        "Выберите подходящий тариф в разделе подписки.",
        parse_mode="HTML",
        reply_markup=main_menu,
    )


@dp.message(F.text == "❌ Отмена")
async def cancel(message: Message, state: FSMContext):
    await state.clear()

    await message.answer(
        "Действие отменено.",
        reply_markup=main_menu,
    )


@dp.message(F.text == "💼 Бизнес")
async def business_section(message: Message):
    back_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="◀️ Назад")],
        ],
        resize_keyboard=True,
    )
    await message.answer(
        "💼 Бизнес-раздел\n\n"
        "Здесь можно управлять услугами, клиентами, подписками и финансами.",
        reply_markup=back_keyboard,
    )


@dp.message(F.text == "📦 Услуги")
async def services_section(message: Message):
    back_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="◀️ Назад")],
        ],
        resize_keyboard=True,
    )
    await message.answer(
        "📦 Услуги\n\n"
        "Тарифы, пакеты, записи, абонементы и доступ к программам.",
        reply_markup=back_keyboard,
    )


@dp.message(F.text == "📊 Статистика")
async def statistics_section(message: Message):
    await message.answer(
        "📊 Статистика\n\n"
        "Показатели активности, прогресс, обучение и результаты пользователей.",
        reply_markup=user_main_menu,
    )


@dp.message(F.text == "⚙️ Настройки")
async def settings_section(message: Message):
    await message.answer(
        "⚙️ Настройки",
        reply_markup=user_settings_menu,
    )


@dp.message(F.text == "🆘 Поддержка")
async def support_section(message: Message):
    back_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="◀️ Назад")],
        ],
        resize_keyboard=True,
    )
    await message.answer(
        "🆘 Поддержка\n\n"
        "Напишите нам, и мы поможем разобраться с вопросом.\n\n"
        "Telegram: @YurchikBond\n"
        "ID: 1679392581",
        reply_markup=back_keyboard,
    )


@dp.message(F.text == "📞 Контакты")
async def contacts_section(message: Message):
    back_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="◀️ Назад")],
        ],
        resize_keyboard=True,
    )
    await message.answer(
        "📞 Контакты\n\n"
        "Telegram: @YurchikBond\n"
        "ID: 1679392581",
        reply_markup=back_keyboard,
    )


@dp.message(F.text == "🧾 Профиль")
async def profile_section(message: Message):
    await message.answer(
        "🧾 Профиль\n\n"
        f"Имя: {message.from_user.first_name if message.from_user else 'Пользователь'}\n"
        f"ID: {message.from_user.id if message.from_user else '—'}",
        reply_markup=user_settings_menu,
    )


@dp.message(F.text == "🔔 Уведомления")
async def notifications_section(message: Message):
    await message.answer(
        "🔔 Уведомления\n\n"
        "Уведомления включены. Вы будете получать обновления и напоминания.",
        reply_markup=user_settings_menu,
    )


@dp.message(F.text == "💬 Изменить имя")
async def change_name_section(message: Message):
    await message.answer(
        "💬 Изменить имя\n\n"
        "Напишите новое имя, которое хотите использовать в боте.",
        reply_markup=user_settings_menu,
    )


@dp.message(F.text == "🌐 Язык")
async def language_section(message: Message):
    await message.answer(
        "🌐 Язык\n\n"
        "Выбранный язык: русский",
        reply_markup=user_settings_menu,
    )


@dp.message(F.text == "◀️ Назад")
async def back_to_main_from_settings(message: Message):
    await message.answer(
        "◀️ Назад в главное меню",
        reply_markup=user_main_menu,
    )


# --------------------------------------------------
# ПРОГРАММА ТРЕНИРОВОК
# --------------------------------------------------

def split_message(text: str, max_length: int = 4000) -> list[str]:
    parts = []
    current_part = ""

    for line in text.split("\n"):
        new_line = line + "\n"

        if len(current_part) + len(new_line) > max_length:
            parts.append(current_part.strip())
            current_part = new_line
        else:
            current_part += new_line

    if current_part.strip():
        parts.append(current_part.strip())

    return parts

@dp.message(F.text == "💪 Программа тренировок")
async def workout_start(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(WorkoutForm.height)

    await message.answer(
        "💪 Начинаем составлять программу.\n\n"
        "Напиши свой рост в сантиметрах.\n"
        "Например: 180",
        reply_markup=cancel_menu,
    )


@dp.message(WorkoutForm.height)
async def workout_height(message: Message, state: FSMContext):
    try:
        height = int(message.text)
    except (TypeError, ValueError):
        await message.answer("Напиши рост числом. Например: 180")
        return

    if not 120 <= height <= 230:
        await message.answer("Укажи реальный рост от 120 до 230 см.")
        return

    await state.update_data(height=height)
    await state.set_state(WorkoutForm.weight)

    await message.answer(
        "Теперь напиши свой вес в килограммах.\n"
        "Например: 85"
    )
    


@dp.message(WorkoutForm.weight)
async def workout_weight(message: Message, state: FSMContext):
    try:
        weight = float(message.text.replace(",", "."))
    except (TypeError, ValueError):
        await message.answer("Напиши вес числом. Например: 85")
        return

    if not 35 <= weight <= 300:
        await message.answer("Укажи реальный вес от 35 до 300 кг.")
        return

    await state.update_data(weight=weight)
    await state.set_state(WorkoutForm.goal)

    await message.answer(
    "🎯 Выбери свою цель:",
    reply_markup=goal_keyboard
)
@dp.message(F.text == "💪 Программа тренировок")
async def workout_start(message: Message, state: FSMContext):
    await state.clear()

    await state.set_state(WorkoutForm.height)

    await message.answer(
        "💪 Давай составим для тебя индивидуальную программу тренировок!\n\n"
        "📏 Напиши свой рост в сантиметрах.\n\n"
        "Например: 180",
        reply_markup=cancel_menu,
    )


@dp.message(WorkoutForm.goal)
async def workout_goal(message: Message, state: FSMContext):
    goal = message.text

    if goal not in [
        "🔥 Похудение",
        "💪 Набор мышечной массы",
        "⚖️ Поддержание формы",
    ]:
        await message.answer(
            "🎯 Выбери цель кнопками.",
            reply_markup=goal_keyboard
        )
        return

    await state.update_data(goal=goal)
    await state.set_state(WorkoutForm.experience)

    await message.answer(
        "🏋️ Какой у тебя опыт тренировок?",
        reply_markup=experience_keyboard
    )
@dp.message(WorkoutForm.experience)
async def workout_experience(message: Message, state: FSMContext):
    experience = message.text

    if experience not in [
        "🟢 Новичок",
        "🟡 Средний",
        "🔴 Продвинутый",
    ]:
        await message.answer(
            "🏋️ Выбери опыт кнопками.",
            reply_markup=experience_keyboard,
        )
        return

    await state.update_data(experience=experience)

    await state.set_state(WorkoutForm.place)

    await message.answer(
        "📍 Где ты тренируешься?",
        reply_markup=place_keyboard,
    )
@dp.message(WorkoutForm.place)
async def workout_place(message: Message, state: FSMContext):
    place = message.text

    if place not in [
        "🏋️ Тренажерный зал",
        "🏠 Дом",
    ]:
        await message.answer(
            "📍 Выбери вариант кнопками.",
            reply_markup=place_keyboard,
        )
        return

    await state.update_data(place=place)

    await state.set_state(WorkoutForm.days)

    await message.answer(
        "📅 Сколько раз в неделю ты планируешь тренироваться?",
        reply_markup=days_keyboard,
    )
@dp.message(WorkoutForm.days)
async def workout_days(message: Message, state: FSMContext):
    try:
        days = int(message.text)
    except ValueError:
        await message.answer("Введите количество тренировок числом от 2 до 6.")
        return

    if days < 2 or days > 6:
        await message.answer("Количество тренировок должно быть от 2 до 6.")
        return

    await state.update_data(days=days)

    data = await state.get_data()

    user_id = message.from_user.id

    # Сохраняем настройки пользователя.
    user_workout_settings[user_id] = {
        "goal": data["goal"],
        "experience": data["experience"],
        "place": data["place"],
        "days": days,
    }

    # Первая версия программы.
    user_program_versions[user_id] = 0

    program = create_workout_program(
        goal=data["goal"],
        experience=data["experience"],
        place=data["place"],
        days=days,
        variation=0,
    )

    for part in split_message(program):
        await message.answer(part)

    await message.answer(
        "✅ Программа создана.\n\n"
        "Через 2–3 месяца нажмите «🔄 Изменить программу», "
        "чтобы получить новый набор упражнений.",
        reply_markup=main_menu,
    )

    await state.clear()

    await message.answer(
        f"✅ Данные сохранены!\n\n"
        f"📏 Рост: {data['height']} см\n"
        f"⚖️ Вес: {data['weight']} кг\n"
        f"🎯 Цель: {data['goal']}\n"
        f"🏋️ Опыт: {data['experience']}\n"
        f"📍 Место: {data['place']}\n"
        f"📅 Дней в неделю: {days}\n\n"
        f"⏳ Сейчас составляю программу..."
    )
    print(data)
    program = create_workout_program(
    goal=data["goal"],
    experience=data["experience"],
    place=data["place"],
    days=days,
)
    await message.answer(
        "✅ Твоя программа готова!\n\n"
        f"Рост: {data['height']} см\n"
        f"Вес: {data['weight']} кг\n"
        f"Цель: {data['goal']}\n"
        f"Опыт: {data['experience']}\n"
        f"Тренировок: {days}\n\n"
        f"{program}",
        reply_markup=main_menu,
    )
   
    await state.clear()

   
# --------------------------------------------------
# РАСЧЁТ КАЛОРИЙ
# --------------------------------------------------

@dp.message(F.text == "🥗 Рассчитать калории")
async def calories_start(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(CaloriesForm.gender)

    await message.answer(
        "🥗 Начинаем расчёт калорий.\n\n"
        "Укажи пол: мужчина или женщина.",
        reply_markup=cancel_menu,
    )
@dp.message(F.text == "🥗 Рассчитать калории")
async def calories_start(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(CaloriesForm.gender)

    await message.answer(
        "🥗 Начинаем расчёт калорий.\n\n"
        "Укажи пол: мужчина или женщина.",
        reply_markup=cancel_menu,
    )


@dp.message(CaloriesForm.gender)
async def calories_gender(message: Message, state: FSMContext):
    gender = (message.text or "").lower().strip()

    if gender not in ["мужчина", "женщина"]:
        await message.answer(
            "Напиши: мужчина или женщина."
        )
        return

    await state.update_data(gender=gender)
    await state.set_state(CaloriesForm.age)

    await message.answer(
        "Сколько тебе лет?"
    )

@dp.message(CaloriesForm.age)
async def calories_age(message: Message, state: FSMContext):
    try:
        age = int(message.text)
    except (TypeError, ValueError):
        await message.answer("Напиши возраст числом.")
        return

    if not 14 <= age <= 100:
        await message.answer("Укажи возраст от 14 до 100 лет.")
        return

    await state.update_data(age=age)
    await state.set_state(CaloriesForm.height)

    await message.answer("Укажи рост в сантиметрах.")


@dp.message(CaloriesForm.height)
async def calories_height(message: Message, state: FSMContext):
    try:
        height = int(message.text)
    except (TypeError, ValueError):
        await message.answer("Напиши рост числом.")
        return

    if not 120 <= height <= 230:
        await message.answer("Укажи рост от 120 до 230 см.")
        return

    await state.update_data(height=height)
    await state.set_state(CaloriesForm.weight)

    await message.answer("Укажи вес в килограммах.")


@dp.message(CaloriesForm.weight)
async def calories_weight(message: Message, state: FSMContext):
    try:
        weight = float(message.text.replace(",", "."))
    except (TypeError, ValueError):
        await message.answer("Напиши вес числом.")
        return

    if not 35 <= weight <= 300:
        await message.answer("Укажи вес от 35 до 300 кг.")
        return

    await state.update_data(weight=weight)
    await state.set_state(CaloriesForm.activity)

    await message.answer(
        "Выбери уровень активности:\n\n"
        "1 — почти нет тренировок\n"
        "2 — 1–3 тренировки в неделю\n"
        "3 — 3–5 тренировок в неделю\n"
        "4 — 6–7 тренировок в неделю"
    )


@dp.message(CaloriesForm.activity)
async def calories_activity(message: Message, state: FSMContext):
    try:
        activity = int(message.text)
    except (TypeError, ValueError):
        await message.answer("Напиши число от 1 до 4.")
        return

    if activity not in [1, 2, 3, 4]:
        await message.answer("Выбери уровень активности от 1 до 4.")
        return

    await state.update_data(activity=activity)
    await state.set_state(CaloriesForm.goal)

    await message.answer(
        "Какая цель?\n\n"
        "• похудение\n"
        "• поддержание\n"
        "• набор"
    )


@dp.message(CaloriesForm.goal)
@dp.message(CaloriesForm.goal)
async def calories_goal(message: Message, state: FSMContext):
    goal = message.text.lower().strip()

    if goal not in ["похудение", "поддержание", "набор"]:
        await message.answer(
            "Напиши: похудение, поддержание или набор."
        )
        return

    await state.update_data(goal=goal)

    data = await state.get_data()

    calories_result = calculate_calories(
        gender=data["gender"],
        age=data["age"],
        height=data["height"],
        weight=data["weight"],
        activity=data["activity"],
        goal=data["goal"],
    )

    protein_min = round(data["weight"] * 1.6)
    protein_max = round(data["weight"] * 2.0)

    await message.answer(
        f"✅ Результат расчёта:\n\n"
        f"Поддержание веса: {calories_result['maintenance']} ккал\n"
        f"Твоя цель: {calories_result['target']} ккал\n\n"
        f"Белок: примерно {protein_min}-{protein_max} г в день",
        reply_markup=main_menu,
    )

    await state.clear()

def calculate_calories(
    gender: str,
    age: int,
    height: int,
    weight: float,
    activity: int,
    goal: str,
):
    if gender == "мужчина":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    activity_factors = {
        1: 1.2,
        2: 1.375,
        3: 1.55,
        4: 1.725,
    }

    maintenance = round(bmr * activity_factors[activity])

    if goal == "похудение":
        target = maintenance - 400
    elif goal == "набор":
        target = maintenance + 300
    else:
        target = maintenance

    return {
        "maintenance": maintenance,
        "target": target,
    }
# //изменить программу//

@dp.message(F.text == "🔄 Изменить программу")
async def change_workout_program(message: Message):
    user_id = message.from_user.id

    settings = user_workout_settings.get(user_id)

    if settings is None:
        await message.answer(
            "У вас пока нет сохранённой программы.\n\n"
            "Сначала нажмите «💪 Программа тренировок» и создайте её.",
            reply_markup=main_menu,
        )
        return

    # Увеличиваем номер варианта.
    current_version = user_program_versions.get(user_id, 0)
    new_version = current_version + 1

    user_program_versions[user_id] = new_version

    program = create_workout_program(
        goal=settings["goal"],
        experience=settings["experience"],
        place=settings["place"],
        days=settings["days"],
        variation=new_version,
    )

    place_text = settings["place"]

    await message.answer(
        f"🔄 Создаю новую программу\n\n"
        f"📍 Место: {place_text}\n"
        f"📅 Тренировок: {settings['days']} в неделю\n"
        f"🆕 Вариант программы: №{new_version + 1}"
    )

    for part in split_message(program):
        await message.answer(part)

    await message.answer(
        "✅ Программа изменена. В неё добавлены другие упражнения.",
        reply_markup=main_menu,
    )
# --------------------------------------------------
# МОЙ ПРОГРЕСС
# --------------------------------------------------


   


# --------------------------------------------------
# СПРОСИТЬ ИИ
# --------------------------------------------------




@dp.message(F.text == "🤖 Спросить ИИ")
async def ask_ai(message: Message, state: FSMContext):
    await state.clear()

    await message.answer(
        "🤖 Выбери, что нужно сделать:",
        reply_markup=ai_menu,
    )
 

@dp.message(F.text == "📸 Анализ формы тела")

async def body_analysis_start(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(BodyAnalysisForm.photo)

    await message.answer(
        "📷 Отправь фотографию полностью в полный рост.\n\n"
        "Лучше:\n"
        "• хорошее освещение;\n"
        "• без верхней одежды;\n"
        "• вид спереди.",
        reply_markup=cancel_menu,
    )


    @dp.message(BodyAnalysisForm.photo, F.photo)
    async def body_analysis_photo(message: Message, state: FSMContext):
     await message.answer(
        "📸 Фотография получена!\n\n"
        "🔍 Анализирую форму тела..."
    )
    import base64

@dp.message(BodyAnalysisForm.photo, F.photo)
async def body_analysis_photo(message: Message, state: FSMContext):

    await message.answer("📸 Анализирую фотографию...")

    photo = message.photo[-1]

    file = await bot.get_file(photo.file_id)

    await bot.download_file(
        file.file_path,
        destination="body_photo.jpg",
    )

    with open("body_photo.jpg", "rb") as image:
        image_base64 = base64.b64encode(image.read()).decode("utf-8")

    response = client.responses.create(
        model="gpt-5",
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": """
                        Ты профессиональный фитнес-тренер.

                        Проанализируй фотографию человека.

                        Напиши:

                        1. Примерный процент жира.
                        2. Какие мышцы развиты лучше.
                        3. Какие мышцы отстают.
                        4. Что улучшить.
                        5. Дай рекомендации по тренировкам.
                        6. Дай рекомендации по питанию.

                        Не указывай точные медицинские диагнозы.
                        Всегда говори, что оценка приблизительная.
                                            """
                    },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{image_base64}"
                    }
                ]
            }
        ]
    )
    from aiogram.types import FSInputFile


    async def send_exercise_card(
          message: Message,
          exercise: dict,
        ):

          photo = FSInputFile(exercise["photo"])

          caption = f"""
        🏋️ {exercise["name"]}

        ━━━━━━━━━━━━━━

        💪 Основная мышца

        {", ".join(exercise["primaryMuscles"])}

        🔥 Дополнительные

        {", ".join(exercise["secondaryMuscles"])}

        ━━━━━━━━━━━━━━

        📊 Подходы

        {exercise["sets"]}

        🔁 Повторения

        {exercise["reps"]}

        ⏱ Отдых

        {exercise["rest"]}

        ━━━━━━━━━━━━━━

        ⚙️ Оборудование

        {exercise["equipment"]}

        📈 Сложность

        {exercise["difficulty"]}
        """

          await message.answer_photo(
              photo=photo,
              caption=caption,
              reply_markup=exercise_keyboard,
          )

    await message.answer(response.output_text)

    await state.clear()

    # Здесь позже подключим OpenAI

    await message.answer(
        "✅ Анализ завершён.\n"
        "Пока это тестовая версия.",
        reply_markup=main_menu,
    )

    await state.clear()
    
     

@dp.message(F.text == "🎥 Проверить технику упражнений")
async def start_video_analysis(
    message: Message,
    state: FSMContext,
):
    print("🔥 НАЖАТА КНОПКА ПРОВЕРИТЬ ТЕХНИКУ")

    await state.clear()
    await state.set_state(
        WorkoutForm.exercise_video
    )

    await message.answer(
        "🎥 Отправь видео упражнения.\n\n"
        "📌 Требования:\n"
        "• длительность до 60 секунд;\n"
        "• видно всё тело;\n"
        "• камера неподвижна."
    )

@dp.message(WorkoutForm.exercise_video, F.video)
async def receive_video(message: Message, state: FSMContext):

    video = message.video

    if video.duration > 60:
        await message.answer(
            "❌ Видео должно быть не длиннее 60 секунд."
        )
        return

    file = await message.bot.get_file(video.file_id)

    await message.bot.download_file(
        file.file_path,
        destination="videos/user_video.mp4"
    )
    await state.set_state(WorkoutForm.exercise_info)

    await message.answer(
        "✅ Видео получено.\n\n"
        "Теперь напиши:\n\n"
        "🏋️ Название упражнения\n"
        "Например:\n"
        "Жим лежа\n\n"
        "💪 Группа мышц\n"
        "Например:\n"
        "Грудь"
    )
@dp.message(WorkoutForm.exercise_info)
async def receive_exercise_info(message: Message, state: FSMContext):

    await state.update_data(
        exercise_info=message.text
    )

    await message.answer(
        "⏳ Анализирую технику..."
    )
    frames = extract_frames(
    "videos/user_video.mp4"
   )
    result = analyze_frames(
    message.text
    )
    await message.answer(result)

    # Здесь следующим этапом подключим OpenAI
    await state.clear()



@dp.message(F.text == "💬 Задать вопрос")
async def ai_question_start(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(AIForm.question)

    await message.answer(
    "📷 Отправь фотографию полностью в полный рост.\n\n"
    "Лучше:\n"
    "• хорошее освещение;\n"
    "• без верхней одежды;\n"
    "• вид спереди.\n\n"
    "После получения фотографии я проанализирую форму тела, "
    "примерный процент жира, сильные и слабые мышечные группы.",
    reply_markup=cancel_menu,
)

@dp.message(F.text == "🧠 Интересные факты")
async def facts_start(message: Message):

    await message.answer(
        "🧠 Выбери категорию интересных фактов.",
        reply_markup=facts_menu
    )

@dp.message(F.text == "🏠 Главное меню")
async def back_to_main(message: Message):
    await message.answer(
        "🏠 Вы вернулись в главное меню для обычного пользователя.",
        reply_markup=user_main_menu,
    )
    

@dp.message(AIForm.question)
async def ai_answer(message: Message, state: FSMContext):
    question = message.text.lower()

    answer = create_simple_ai_answer(question)

    await message.answer(
        f"🤖 Ответ Fitness AI:\n\n{answer}",
        reply_markup=main_menu,
    )


    await state.clear()


def create_simple_ai_answer(question: str) -> str:
    if "белок" in question:
        return (
            "Для роста и сохранения мышц обычно используют ориентир "
            "1,6–2 г белка на каждый килограмм массы тела в сутки."
        )

    if "похудение" in question or "жир" in question:
        return (
            "Для похудения нужен умеренный дефицит калорий. "
            "Начни с дефицита примерно 300–500 ккал и отслеживай вес."
        )

    if "грудь" in question:
        return (
            "Для груди используй жим лёжа, жим гантелей и отжимания. "
            "Старайся постепенно увеличивать рабочий вес или повторения."
        )

    if "бицепс" in question:
        return (
            "Для бицепса подойдут подъёмы штанги и сгибания с гантелями. "
            "Обычно достаточно 6–10 рабочих подходов в неделю."
        )

    if "пресс" in question:return (
            "Пресс укрепляют скручивания, подъёмы ног и планка. "
            "Но видимость пресса в основном зависит от процента жира."
        )

    if "кардио" in question:
        return (
            "Кардио можно выполнять 2–4 раза в неделю по 20–45 минут. "
            "Выбирай ходьбу, велосипед, бег или плавание."
        )

    return (
        "Пока я работаю в простом режиме и отвечаю на основные вопросы. "
        "Попробуй спросить про белок, похудение, грудь, бицепс, пресс "
        "или кардио."
    )
client = OpenAI(api_key=OPENAI_API_KEY)

with open(
    "data/exercises.json",
    "r",
    encoding="utf-8"
) as f:
    exercises = json.load(f)

def get_exercise(exercise_id: str):
    for exercise in exercises:
        if exercise["id"] == exercise_id:
            return exercise

    return None

print("KEY:", OPENAI_API_KEY)
from aiogram.fsm.context import FSMContext


import random

# М 
@dp.message(F.text == "💪 Мышцы")
async def muscles_fact(message: Message):

    await message.answer("🧠 Генерирую интересный факт...")

    fact = generate_fact("Мышцы человека")

    await message.answer(fact)
# Питание 
@dp.message(F.text == "🥗 Питание")
async def nutrition_fact(message: Message):

    await message.answer("🧠 Генерирую интересный факт...")

    fact = generate_fact("Спортивное питание")

    await message.answer(fact)
# Чемпион 
@dp.message(F.text == "🏆 Чемпионы")
async def champions_fact(message: Message):

    await message.answer("🧠 Генерирую интересный факт...")

    fact = generate_fact("Известные бодибилдеры")

    await message.answer(fact)


# Бодибилдинг 
@dp.message(F.text == "🏋️ Бодибилдинг")
async def bodybuilding_fact(message: Message):

    await message.answer("🧠 Генерирую интересный факт...")

    fact = generate_fact("Бодибилдинг")

    await message.answer(fact)

# организм 

@dp.message(F.text == "🧬 Организм")
async def body_fact(message: Message):

    await message.answer("🧠 Генерирую интересный факт...")

    fact = generate_fact("Организм человека")

    await message.answer(fact)
    # Миф или правда 
@dp.message(F.text == "❓ Миф или Правда")
async def myth_fact(message: Message):

    await message.answer("🧠 Проверяю...")

    fact = generate_fact(
        "Мифы фитнеса. Сначала напиши '❌ Миф' или '✅ Правда', затем кратко объясни."
    )

    await message.answer(fact)

    # Случайний факт 
@dp.message(F.text == "🎲 Случайный факт")
async def random_fact(message: Message):

    await message.answer("🎲 Подбираю интересный факт...")

    fact = generate_fact(
        "Любая тема: бодибилдинг, мышцы, питание, организм, чемпионы"
    )

    await message.answer(fact)

    photo = FSInputFile(exercise["photo"])

    caption = f"""
🏋️ {exercise["name"]}

━━━━━━━━━━━━━━

💪 Основная мышца

{", ".join(exercise["primaryMuscles"])}

🔥 Дополнительные мышцы

{", ".join(exercise["secondaryMuscles"])}

━━━━━━━━━━━━━━

📊 Подходы: {exercise["sets"]}

🔁 Повторения: {exercise["reps"]}

⏱ Отдых: {exercise["rest"]}

━━━━━━━━━━━━━━

⚙️ Оборудование

{exercise["equipment"]}

📈 Сложность

{exercise["difficulty"]}
"""
@dp.message(Command("help"))
async def help_command(message: Message):
    await message.answer(
        "❓ <b>Помощь Fitness AI</b>\n\n"
        "💪 Программа тренировок — создаёт персональный план\n"
        "🍽 Программа питания — составляет рацион\n"
        "📈 Мой прогресс — отслеживание результатов\n"
        "🎙 Голосовой фитнес-чат — вопросы голосом\n"
        "🤖 Спросить ИИ — вопросы о тренировках и питании\n\n"
        "🏠 Чтобы вернуться в главное меню, используйте /start",
        parse_mode="HTML",
        reply_markup=main_menu,
    )


async def set_bot_commands(bot):
    commands = [
        BotCommand(
            command="start",
            description="🏠 Главное меню"
        ),
        BotCommand(
            command="help",
            description="❓ Помощь"
        ),
    ]

    await bot.set_my_commands(commands)

async def main():
    print("Бот запущен")
    create_users_table()
    await set_bot_commands(bot)

    if not scheduler.running:
        scheduler.start()

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

