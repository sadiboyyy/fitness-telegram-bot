import os
import re
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup

from keyboards.menu import main_menu
from apscheduler.triggers.cron import CronTrigger
from scheduler import scheduler


router = Router()


class ReminderForm(StatesGroup):
    days = State()
    time = State()


reminder_days_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Пн"),
            KeyboardButton(text="Вт"),
            KeyboardButton(text="Ср"),
        ],
        [
            KeyboardButton(text="Чт"),
            KeyboardButton(text="Пт"),
            KeyboardButton(text="Сб"),
        ],
        [
            KeyboardButton(text="Вс"),
        ],
        [
            KeyboardButton(text="✅ Продолжить"),
        ],
        [
            KeyboardButton(text="🏠 Главное меню"),
        ],
    ],
    resize_keyboard=True,
)


@router.message(F.text == "⏰ Напоминания о тренировках")
async def start_reminder_setup(
    message: Message,
    state: FSMContext,
):
    await state.clear()
    await state.update_data(selected_days=[])

    await state.set_state(ReminderForm.days)

    await message.answer(
        "⏰ Настройка напоминаний\n\n"
        "Выберите дни тренировок.\n"
        "Можно нажать несколько дней по очереди.\n\n"
        "Когда закончите, нажмите «✅ Продолжить».",
        reply_markup=reminder_days_keyboard,
    )


@router.message(
    ReminderForm.days,
    F.text.in_({"Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"}),
)
async def select_reminder_day(
    message: Message,
    state: FSMContext,
):
    data = await state.get_data()
    selected_days = data.get("selected_days", [])

    day = message.text

    if day not in selected_days:
        selected_days.append(day)

        await state.update_data(selected_days=selected_days)

        await message.answer(
            f"✅ Добавлен день: {day}\n\n"
            f"Выбрано: {', '.join(selected_days)}"
        )
    else:
        selected_days.remove(day)

        await state.update_data(selected_days=selected_days)

        selected_text = ", ".join(selected_days) or "ничего"

        await message.answer(
            f"❌ День {day} удалён.\n\n"
            f"Выбрано: {selected_text}"
        )


@router.message(
    ReminderForm.days,
    F.text == "✅ Продолжить",
)
async def request_reminder_time(
    message: Message,
    state: FSMContext,
):
    data = await state.get_data()
    selected_days = data.get("selected_days", [])

    if not selected_days:
        await message.answer(
            "❌ Сначала выберите хотя бы один день."
        )
        return

    await state.set_state(ReminderForm.time)

    await message.answer(
        "🕐 Введите время напоминания в формате ЧЧ:ММ.\n\n"
        "Например:\n"
        "18:30"
    )



@router.message(ReminderForm.time)

async def save_reminder_time(
    message: Message,
    state: FSMContext,
):
    time_text = message.text.strip()

    if not re.fullmatch(r"([01]\d|2[0-3]):([0-5]\d)", time_text):
        await message.answer(
            "❌ Неверный формат времени.\n\n"
            "Введите время так:\n"
            "18:30"
        )
        return

    data = await state.get_data()

    selected_days = data["selected_days"]

    await state.update_data(
        reminder_time=time_text
  )
    hour, minute = map(int, time_text.split(":"))

    for day in selected_days:
        scheduler.add_job(
            send_workout_reminder,
            trigger=CronTrigger(
                day_of_week=DAY_MAP[day],
                hour=hour,
                minute=minute,
            ),
            kwargs={
                "bot": message.bot,
                "chat_id": message.chat.id,
            },
            id=f"{message.chat.id}_{day}",
            replace_existing=True,
          )

    await message.answer(
            "✅ Напоминание настроено!\n\n"
            f"📅 Дни: {', '.join(selected_days)}\n"
            f"🕒 Время: {time_text}\n\n"
            "Следующий этап — автоматическая отправка уведомлений.",
            reply_markup=main_menu
    )

    await state.clear()


DAY_MAP = {
    "Пн": "mon",
    "Вт": "tue",
    "Ср": "wed",
    "Чт": "thu",
    "Пт": "fri",
    "Сб": "sat",
    "Вс": "sun",
}


async def send_workout_reminder(bot, chat_id):
     await bot.send_message(
        chat_id,
        "💪 Пора на тренировку!\n\n"
        "Не откладывай тренировку.\n"
        "Даже одна хорошая тренировка делает тебя сильнее. 🔥"
    )

@router.message(F.text == "🏠 Главное меню")
async def reminder_back_to_menu(
    message: Message,
    state: FSMContext,
):
    await state.clear()

    await message.answer(
        "🏠 Вы вернулись в главное меню.",
        reply_markup=main_menu,
    )