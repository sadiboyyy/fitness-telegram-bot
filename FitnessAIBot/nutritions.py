from email import message

from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from assistant_ai.nutrition_ai import create_nutrition_program
from keyboards.nutrition import (
    nutrition_result_keyboard,
    goal_keyboard,
    gender_keyboard,
    workouts_keyboard,
    activity_keyboard,
    restrictions_keyboard,
    meals_keyboard,
)
from keyboards.menu import main_menu 


router = Router() 


class NutritionForm(StatesGroup):
    goal = State()
    height = State()
    weight = State()
    age = State()
    gender = State()
    workouts = State()
    activity = State()
    restrictions = State()
    budget = State()
    meals = State()
    favorite_foods = State()

@router.message(F.text.contains("Программа питания"))
async def nutrition_start(message: Message, state: FSMContext):
    await state.clear()

    await message.answer(
        "🍽 Составим для вас персональную программу питания.\n\n"
        "Для начала выберите вашу цель:",
        reply_markup=goal_keyboard
    )
    await state.set_state(NutritionForm.goal)


@router.message(NutritionForm.goal)
async def nutrition_goal(message: Message, state: FSMContext):
    await state.update_data(goal=message.text)

    await message.answer(
        "📏 Введите ваш рост (см):"
    )

    await state.set_state(NutritionForm.height)


@router.message(NutritionForm.height)
async def nutrition_height(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("❌ Введите рост числом.")
        return

    height = int(message.text)

    if height < 120 or height > 250:
        await message.answer("❌ Рост должен быть от 120 до 250 см.")
        return

    await state.update_data(height=height)

    await message.answer(
        "⚖️ Введите ваш вес (кг):"
    )

    await state.set_state(NutritionForm.weight)


@router.message(NutritionForm.weight)
async def nutrition_weight(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("❌ Введите вес числом.")
        return

    weight = int(message.text)

    if weight < 30 or weight > 300:
        await message.answer("❌ Введите корректный вес.")
        return

    await state.update_data(weight=weight)

    await message.answer(
        "🎂 Введите ваш возраст:"
    )

    await state.set_state(NutritionForm.age)


@router.message(NutritionForm.age)
async def nutrition_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("❌ Возраст должен быть числом.")
        return

    age = int(message.text)

    if age < 10 or age > 100:
        await message.answer("❌ Введите корректный возраст.")
        return

    await state.update_data(age=age)

    await message.answer(
        "👨 Выберите пол:",
        reply_markup=gender_keyboard
    )

    await state.set_state(NutritionForm.gender)

@router.message(NutritionForm.gender)
async def nutrition_gender(message: Message, state: FSMContext):
    await state.update_data(gender=message.text)

    await message.answer(
        "🏋️ Сколько раз в неделю вы тренируетесь?",
        reply_markup=workouts_keyboard
    )

    await state.set_state(NutritionForm.workouts)


@router.message(NutritionForm.workouts)
async def nutrition_workouts(message: Message, state: FSMContext):
    await state.update_data(workouts=message.text)

    await message.answer(
        "🚶 Выберите уровень вашей активности:",
        reply_markup=activity_keyboard
    )

    await state.set_state(NutritionForm.activity)


@router.message(NutritionForm.activity)
async def nutrition_activity(message: Message, state: FSMContext):
    await state.update_data(activity=message.text)

    await message.answer(
        "🚫 Есть ли у вас ограничения в питании?",
        reply_markup=restrictions_keyboard
    )

    await state.set_state(NutritionForm.restrictions)


@router.message(NutritionForm.restrictions)
async def nutrition_restrictions(message: Message, state: FSMContext):
    await state.update_data(restrictions=message.text)

    await message.answer(
        "💵 Какой у вас бюджет на питание в месяц?\n\n"
        "Введите сумму в долларах ($).\n\n"
        "Например: 100"
    )

    await state.set_state(NutritionForm.budget)


@router.message(NutritionForm.budget)
async def nutrition_budget(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("❌ Введите сумму числом.")
        return

    budget = int(message.text)

    if budget < 20:
        await message.answer("❌ Бюджет должен быть не менее 20$.")
        return

    await state.update_data(budget=budget)

    await message.answer(
        "🍽 Сколько приемов пищи в день вы предпочитаете?",
        reply_markup=meals_keyboard
    )

    await state.set_state(NutritionForm.meals)


@router.message(NutritionForm.meals)
async def nutrition_meals(message: Message, state: FSMContext):
    await state.update_data(meals=message.text)

    await message.answer(
        "❤️ Напишите продукты, которые вы любите.\n\n"
        "Например:\n"
        "Курица, яйца, рис, овсянка, бананы\n\n"
        "Если предпочтений нет, напишите:\n"
        "Нет"
    )

    await state.set_state(NutritionForm.favorite_foods)

    from assistant_ai.nutrition_ai import create_nutrition_program


@router.message(NutritionForm.favorite_foods)
async def nutrition_favorite_foods(message: Message, state: FSMContext):
    await state.update_data(favorite_foods=message.text)

    data = await state.get_data()

    await message.answer(
        "🤖 Составляю вашу персональную программу питания...\n"
        "⏳ Пожалуйста, подождите пару минут."
    )

    try:
        program = await create_nutrition_program(data)

        MAX_MESSAGE_LENGTH = 4000

        parts = [
            program[i:i + MAX_MESSAGE_LENGTH]
            for i in range(0, len(program), MAX_MESSAGE_LENGTH)
        ]
    
        for index, part in enumerate(parts):
            if index == len(parts) - 1:
                await message.answer(
                  part,
                  reply_markup=nutrition_result_keyboard
                )
            else:
                await message.answer(part)

        await state.clear()
    except Exception as e:
        print(e)
        await state.clear()
        await message.answer(
          f"❌ Ошибка:\n{e}"
        )

        
@router.message(F.text == "🔄 Сгенерировать заново")
async def regenerate_program(message: Message, state: FSMContext):
    await state.set_state(NutritionForm.goal)

    await message.answer(
        "🎯 Какая у вас цель?",
        reply_markup=goal_keyboard
    )


@router.message(F.text == "🛒 Список покупок")
async def shopping_list(message: Message):
    await message.answer(
        "🛒 Пока список покупок доступен внутри программы питания.\n"
        "Отдельный список появится в следующем обновлении."
    )


@router.message(F.text == "📄 Скачать PDF")
async def download_pdf(message: Message):
    await message.answer(
        "📄 Генерация PDF появится в следующем обновлении."
    )


@router.message(F.text == "🏠 Главное меню")
async def back_to_menu(
    message: Message,
    state: FSMContext,
):
    await state.clear()

    await message.answer(
        "🏠 Вы вернулись в главное меню.",
        reply_markup=main_menu,
    )


