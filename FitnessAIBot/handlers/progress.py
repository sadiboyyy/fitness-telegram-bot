import os
import random

from aiogram.types import FSInputFile
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup

from keyboards.menu import main_menu
from datetime import datetime
from database import conn, cursor


router = Router()

def get_random_gif():

    gifs_folder = "assets/gifs"

    gifs = [
        file
        for file in os.listdir(gifs_folder)
        if file.endswith(".gif")
    ]

    if not gifs:
        return None

    gif = random.choice(gifs)

    path = os.path.join(gifs_folder, gif)
    print(path)
    print(os.path.getsize(path))
    return FSInputFile(path)



class ProgressForm(StatesGroup):
    biceps = State()
    chest = State()
    waist = State()
    weight = State()

    progress_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📏 Добавить замеры"),
        ],
        [
            KeyboardButton(text="📊 Посмотреть прогресс"),
        ],
        [
            KeyboardButton(text="🏠 Главное меню"),
        ],
    ],
    resize_keyboard=True,
)
@router.message(F.text == "📈 Мой прогресс")
async def open_progress_menu(
    message: Message,
    state: FSMContext,
):
    await state.clear()

    gif = get_random_gif()

    if gif:
       await message.answer_document(gif)

    await message.answer(
        "📈 <b>Мой прогресс</b>\n\n"
        "Выберите действие:",
        reply_markup=progress_menu,
        parse_mode="HTML",
    )
@router.message(F.text == "📏 Добавить замеры")
async def add_measurements(
    message: Message,
    state: FSMContext,
):
    await state.clear()

    await state.set_state(ProgressForm.biceps)

    await message.answer(
        "💪 Введите обхват бицепса в сантиметрах.\n\n"
        "Например: 39"
    )

@router.message(F.text == "📏 Добавить замеры")
async def add_measurements(
    message: Message,
    state: FSMContext,
):
    await state.set_state(ProgressForm.biceps)

    await message.answer(
        "💪 Введите обхват бицепса в сантиметрах.\n\n"
        "Например: 39"
    )
@router.message(F.text == "📊 Посмотреть прогресс")
async def show_progress(
    message: Message,
    state: FSMContext,
):
    await state.clear()

    cursor.execute(
        """
        SELECT date, biceps, chest, waist, weight
        FROM progress
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT 10
        """,
        (message.from_user.id,),
    )

    results = cursor.fetchall()

    if not results:
        await message.answer(
            "📊 У вас пока нет сохранённых замеров.\n\n"
            "Сначала нажмите «📏 Добавить замеры».",
            reply_markup=progress_menu,
        )
        return

    text = "📈 <b>Последние замеры</b>\n\n"

    for i, row in enumerate(results, start=1):
        date, biceps, chest, waist, weight = row

        text += (
            f"<b>{i}.</b> 📅 {date}\n"
            f"💪 {biceps:g} см\n"
            f"🫁 {chest:g} см\n"
            f"📐 {waist:g} см\n"
            f"⚖️ {weight:g} кг\n\n"
        )

    await message.answer(
        text,
        reply_markup=progress_menu,
        parse_mode="HTML",
    )

@router.message(ProgressForm.biceps)
async def save_biceps(
    message: Message,
    state: FSMContext,
):
    try:
        biceps = float(message.text.replace(",", "."))
    except (ValueError, AttributeError):
        await message.answer(
            "❌ Введите обхват бицепса числом.\n"
            "Например: 39 или 39.5"
        )
        return

    if biceps < 15 or biceps > 80:
        await message.answer(
            "❌ Укажите реалистичный обхват бицепса "
            "от 15 до 80 см."
        )
        return

    await state.update_data(biceps=biceps)
    await state.set_state(ProgressForm.chest)

    await message.answer(
        "🫁 Введите обхват груди в сантиметрах.\n\n"
        "Например: 105"
    )
@router.message(ProgressForm.chest)
async def save_chest(
    message: Message,
    state: FSMContext,
):
    try:
        chest = float(message.text.replace(",", "."))
    except (ValueError, AttributeError):
        await message.answer(
            "❌ Введите обхват груди числом.\n"
            "Например: 105 или 105.5"
        )
        return

    if chest < 50 or chest > 200:
        await message.answer(
            "❌ Укажите реалистичный обхват груди "
            "от 50 до 200 см."
        )
        return

    await state.update_data(chest=chest)
    await state.set_state(ProgressForm.waist)

    await message.answer(
        "📐 Введите обхват талии в сантиметрах.\n\n"
        "Например: 85"
    )
@router.message(ProgressForm.waist)
async def save_waist(
    message: Message,
    state: FSMContext,
):
    try:
        waist = float(message.text.replace(",", "."))
    except (ValueError, AttributeError):
        await message.answer(
            "❌ Введите обхват талии числом.\n"
            "Например: 85 или 85.5"
        )
        return

    if waist < 40 or waist > 200:
        await message.answer(
            "❌ Укажите реалистичный обхват талии "
            "от 40 до 200 см."
        )
        return

    await state.update_data(waist=waist)
    await state.set_state(ProgressForm.weight)

    await message.answer(
        "⚖️ Введите текущий вес в килограммах.\n\n"
        "Например: 85"
    )

@router.message(ProgressForm.weight)
async def save_weight(
    message: Message,
    state: FSMContext,
):
    try:
        weight = float(message.text.replace(",", "."))
    except (ValueError, AttributeError):
        await message.answer(
            "❌ Введите вес числом.\n"
            "Например: 85 или 84.5"
        )
        return

    if weight < 30 or weight > 300:
        await message.answer(
            "❌ Укажите реалистичный вес от 30 до 300 кг."
        )
        return

    await state.update_data(weight=weight)

    data = await state.get_data()

    today = datetime.now().strftime("%d.%m.%Y")

    cursor.execute(
        """
        INSERT INTO progress(
            user_id,
            date,
            biceps,
            chest,
            waist,
            weight
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
          (
              message.from_user.id,
              today,
              data["biceps"],
              data["chest"],
              data["waist"],
              weight,
          ),
    )

    conn.commit()


@router.message(F.text == "📊 Посмотреть прогресс")
async def show_progress(
    message: Message,
    state: FSMContext,
):
    await state.clear()

    gif = get_random_gif()

    if gif:
        await message.answer_animation(gif)

    cursor.execute(
        """
        SELECT
            date,
            biceps,
            chest,
            waist,
            weight
        FROM progress
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT 1
        """,
        (message.from_user.id,),
    )

    result = cursor.fetchone()

    if result is None:
        await message.answer(
            "📊 У вас пока нет сохранённых замеров."
        )
        return

    date, biceps, chest, waist, weight = result

    await message.answer(
        "📈 Последние замеры\n\n"
        f"📅 Дата: {date}\n"
        f"💪 Бицепс: {biceps:g} см\n"
        f"🫁 Грудь: {chest:g} см\n"
        f"📐 Талия: {waist:g} см\n"
        f"⚖️ Вес: {weight:g} кг",
        reply_markup=progress_menu,
    )

@router.message(F.text == "🏠 Главное меню")
async def progress_back_to_menu(
    message: Message,
    state: FSMContext,
):
    await message.answer(
        "🏠 Вы вернулись в главное меню.",
        reply_markup=main_menu,
    )