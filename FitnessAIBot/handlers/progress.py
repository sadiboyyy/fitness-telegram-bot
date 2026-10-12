import os
import random

from aiogram.types import FSInputFile
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup

from keyboards.menu import main_menu
from datetime import datetime
from pathlib import Path
from fitcoins import add_fitcoins
from achievements import unlock_achievement


router = Router()

PHOTO_DIR = Path("photos/progress")
PHOTO_DIR.mkdir(parents=True, exist_ok=True)

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

progress_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📏 Добавить замеры")],
        [KeyboardButton(text="📊 Посмотреть прогресс")],
        [KeyboardButton(text=" 📸 Мои фото прогресса")],
        [KeyboardButton(text="⚖️ Сравнить ДО и ПОСЛЕ")],
        [KeyboardButton(text="🏠 Главное меню")],

    ],
    resize_keyboard=True,
)


class ProgressForm(StatesGroup):
    biceps = State()
    chest = State()
    waist = State()
    weight = State()
    before_photo = State()

    
@router.message(F.text == "📈 Мой прогресс")
async def open_progress_menu(
    message: Message,
    state: FSMContext,
):
    await state.clear()

    gif = get_random_gif()

    if gif:
        await message.answer_animation(animation=gif)

    await message.answer(
        "🏋️ <b>Ваш фитнес-прогресс</b>\n\n"
        "Добро пожаловать в раздел отслеживания прогресса.\n\n"
        "Здесь вы можете:\n"
        "📏 Добавить новые замеры\n"
        "📊 Посмотреть историю\n"
        "📈 Посмотреть графики\n"
        "🏆 Следить за своими достижениями\n\n"
        "👇 Выберите действие:",
        parse_mode="HTML",
        reply_markup=progress_menu,

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

    created_at = datetime.now().strftime("%d.%m.%Y %H:%M")

    try:
        cursor.execute(
            """
            INSERT INTO progress (
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
                created_at,
                data["biceps"],
                data["chest"],
                data["waist"],
                weight,
            ),
        )

    except Exception as error:
        print("Ошибка сохранения замеров:", error)
       
        await message.answer(
            "❌ Не удалось сохранить замеры.\n\n"
            f"Ошибка: {error}"
        )
        return


    conn.commit()

    coins_added = add_fitcoins(
        user_id=message.from_user.id,
        amount=10,
        reason="Добавление замеров",
    )

    achievement = unlock_achievement(
        message.from_user.id,
        "FIRST_MEASURE",
    )

    if achievement:
        title, reward = achievement

        await message.answer(
            "🏆 <b>Новое достижение!</b>\n\n"
            f"{title}\n\n"
            f"🪙 +{reward} FitCoins",
            parse_mode="HTML",
        )

    cursor.execute(
        """
        SELECT biceps, chest, waist, weight
        FROM progress
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT 2
        """,
        (message.from_user.id,),
    )
    

    history = cursor.fetchall()

    analysis = ""

    if len(history) >= 2:
      current = history[0]
      previous = history[1]

      biceps_diff = current[0] - previous[0]
      chest_diff = current[1] - previous[1]
      waist_diff = current[2] - previous[2]
      weight_diff = current[3] - previous[3]

      analysis = "\n\n📈 <b>Изменения с прошлого замера</b>\n"

      if biceps_diff > 0:
          analysis += f"💪 Бицепс: +{biceps_diff:.1f} см\n"
      elif biceps_diff < 0:
          analysis += f"💪 Бицепс: {biceps_diff:.1f} см\n"
      else:
          analysis += "💪 Бицепс: без изменений\n"

      if chest_diff > 0:
          analysis += f"🫁 Грудь: +{chest_diff:.1f} см\n"
      elif chest_diff < 0:
          analysis += f"🫁 Грудь: {chest_diff:.1f} см\n"
      else:
          analysis += "🫁 Грудь: без изменений\n"

      if waist_diff > 0:
          analysis += f"📐 Талия: +{waist_diff:.1f} см\n"
      elif waist_diff < 0:
          analysis += f"📐 Талия: {waist_diff:.1f} см\n"
      else:
          analysis += "📐 Талия: без изменений\n"

      if weight_diff > 0:
          analysis += f"⚖️ Вес: +{weight_diff:.1f} кг\n"
      elif weight_diff < 0:
          analysis += f"⚖️ Вес: {weight_diff:.1f} кг\n"
      else:
          analysis += "⚖️ Вес: без изменений\n"


    await state.clear()

    coins_text = ""

    if coins_added:
     coins_text = "\n\n🪙 Получено: +10 FitCoins"

    await message.answer(
        "✅ <b>Замеры успешно сохранены!</b>\n\n"
        f"🕒 Дата и время: {created_at}\n"
        f"💪 Бицепс: {data['biceps']:g} см\n"
        f"🫁 Грудь: {data['chest']:g} см\n"
        f"📐 Талия: {data['waist']:g} см\n"
        f"⚖️ Вес: {weight:g} кг"
        f"{analysis}",
        f"{coins_text}",
        parse_mode="HTML",
        reply_markup=progress_menu,
    )

    await message.answer(
      "📸 Теперь отправьте фотографию формы «До».\n\n"
      "Лучше всего:\n"
      "• стоя прямо\n"
      "• при хорошем освещении\n"
      "• в полный рост или по пояс\n"
      "• без верхней одежды\n\n"
      "Эта фотография понадобится для сравнения прогресса."
    )
    await state.set_state(ProgressForm.before_photo)



@router.message(ProgressForm.before_photo, F.photo)
async def save_before_photo(
    message: Message,
    state: FSMContext,
):
    photo = message.photo[-1]

    file = await message.bot.get_file(photo.file_id)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = (
    f"{message.from_user.id}_"
    f"{timestamp}_before.jpg"
)

    destination = PHOTO_DIR / filename

    await message.bot.download_file(
        file.file_path,
        destination=destination,
    )

    await message.answer(
        "✅ Фото «ДО» успешно сохранено!\n\n"
        "📷 Через месяц вы сможете загрузить фотографию «ПОСЛЕ», "
        "и бот автоматически покажет изменения.",
        reply_markup=progress_menu,
    )

    await state.clear()

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
@router.message(ProgressForm.before_photo, F.photo)
async def save_before_photo(
    message: Message,
    state: FSMContext,
):
    photo = message.photo[-1]

    await message.answer(
        "✅ Фото «ДО» успешно сохранено!\n\n"
        "Через месяц вы сможете добавить фотографию «ПОСЛЕ» и бот автоматически покажет разницу.",
        reply_markup=progress_menu,
    )

    await state.clear()

@router.message(F.text == "📷 Мои фото прогресса")
async def my_progress_photos(message: Message):

    files = sorted(
        PHOTO_DIR.glob(f"{message.from_user.id}_*.jpg"),
        reverse=True,
    )

    if not files:
        await message.answer(
            "📷 У вас пока нет сохранённых фотографий."
        )
        return

    await message.answer(
        f"📸 Найдено фотографий: {len(files)}"
    )

    for photo in files:

        await message.answer_photo(
            FSInputFile(photo),
            caption=photo.stem,
        )

@router.message(F.text == "⚖️ Сравнить ДО и ПОСЛЕ")
async def compare_progress(
    message: Message,
):
    await message.answer(
        "🚧 Эта функция уже почти готова.\n\n"
        "В следующем обновлении бот автоматически:\n\n"
        "📷 покажет фото ДО и ПОСЛЕ;\n"
        "📊 сравнит замеры;\n"
        "🤖 сделает анализ изменений тела."
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