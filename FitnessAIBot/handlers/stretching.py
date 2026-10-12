from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from aiogram.types import Message, FSInputFile

from audio_stretching import (
    build_stretching_script,
    create_stretching_voice,
    mix_stretching_audio, 
)

from keyboards.stretching import (
    stretching_goal_keyboard,
    stretching_duration_keyboard,
    stretching_level_keyboard,
)


stretching_router = Router()


class StretchingForm(StatesGroup):
    goal = State()
    duration = State()
    level = State()


@stretching_router.message(F.text == "🤸 Растяжка")
async def start_stretching(message: Message, state: FSMContext):
    await state.clear()

    await message.answer(
        "🤸 <b>Растяжка</b>\n\n"
        "Я помогу составить персональную программу растяжки.\n\n"
        "Что ты хочешь растянуть?",
        reply_markup=stretching_goal_keyboard,
        parse_mode="HTML",
    )

    await state.set_state(StretchingForm.goal)


@stretching_router.message(StretchingForm.goal)
async def stretching_goal(message: Message, state: FSMContext):

    allowed_goals = [
        "🧘 Всё тело",
        "🦵 Ноги",
        "🧍 Спина",
        "💪 Плечи и руки",
        "🏋️ После тренировки",
        "🌅 Утренняя растяжка",
    ]

    if message.text not in allowed_goals:
        await message.answer(
            "Выбери цель с помощью кнопок 👇",
            reply_markup=stretching_goal_keyboard,
        )
        return

    await state.update_data(goal=message.text)

    await message.answer(
        "⏱ Теперь выбери длительность растяжки:",
        reply_markup=stretching_duration_keyboard,
    )

    await state.set_state(StretchingForm.duration)


@stretching_router.message(StretchingForm.duration)
async def stretching_duration(message: Message, state: FSMContext):

    durations = {
        "4 минуты": 4,
        "7 минут": 7,
        "10 минут": 10,
       
    }

    if message.text not in durations:
        await message.answer(
            "Выбери длительность с помощью кнопок 👇",
            reply_markup=stretching_duration_keyboard,
        )
        return

    await state.update_data(
        duration=durations[message.text]
    )

    await message.answer(
        "⭐ Какой у тебя уровень растяжки?",
        reply_markup=stretching_level_keyboard,
    )

    await state.set_state(StretchingForm.level)

@stretching_router.message(StretchingForm.level)
async def stretching_level(
    message: Message,
    state: FSMContext,
):

    allowed_levels = [
        "🌱 Новичок",
        "💪 Средний",
        "🔥 Продвинутый",
    ]

    if message.text not in allowed_levels:
        await message.answer(
            "Выбери уровень с помощью кнопок 👇",
            reply_markup=stretching_level_keyboard,
        )
        return

    # Сохраняем уровень
    await state.update_data(
        level=message.text
    )

    # Получаем все выбранные параметры
    data = await state.get_data()

    goal = data["goal"]
    duration = data["duration"]
    level = data["level"]

    await message.answer(
        "🎧 Создаю персональную аудио-растяжку...\n\n"
        f"🎯 {goal}\n"
        f"⏱ {duration} минут\n"
        f"⭐ {level}\n\n"
        "Это может занять некоторое время."
    )

    try:

        # -----------------------------
        # Создаём сценарий
        # -----------------------------

        script = build_stretching_script(
            goal=goal,
            duration=duration,
            level=level,
        )

        print(
            f"Создан сценарий: "
            f"{len(script)} упражнений"
        )

        # -----------------------------
        # Генерируем голос + паузы
        # -----------------------------

        voice_path = create_stretching_voice(
            user_id=message.from_user.id,
            script=script,
            duration=duration,
        )

        print(
            f"Голос растяжки создан: "
            f"{voice_path}"
        )

        # -----------------------------
        # Накладываем музыку
        # -----------------------------

        final_path = mix_stretching_audio(
            voice_path=voice_path,
            user_id=message.from_user.id,
            duration=duration,
        )

        print(
            f"Готовая растяжка: "
            f"{final_path}"
        )

        # -----------------------------
        # Отправляем MP3
        # -----------------------------

        audio = FSInputFile(
            final_path
        )

        await message.answer_audio(
            audio=audio,
            title="Персональная растяжка",
            performer="Fitness AI",
            caption=(
                "🧘 <b>Твоя растяжка готова!</b>\n\n"
                f"🎯 {goal}\n"
                f"⏱ {duration} минут\n"
                f"⭐ {level}\n\n"
                "Выполняй движения плавно и без боли 💪"
            ),
            parse_mode="HTML",
        )

        await state.clear()

    except Exception as error:
        print(
            "❌ ОШИБКА РАСТЯЖКИ:",
            repr(error),
        )

        # Обязательно выходим из состояния растяжки
        await state.clear()

        error_text = str(error)

        if (
            "credit_balance_exhausted" in error_text
            or "no credits remaining" in error_text
        ):
            await message.answer(
                "⚠️ <b>Растяжка временно недоступна</b>\n\n"
                "Сервис генерации аудио сейчас временно "
                "не может создать тренировку.\n\n"
                "🛠 Попробуйте немного позже.",
                parse_mode="HTML",
            )
            return

        await message.answer(
            "⚠️ <b>Ошибка генерации растяжки</b>\n\n"
            "Не удалось создать аудиотренировку.\n"
            "Попробуйте немного позже. 🛠",
            parse_mode="HTML",
        )

        return