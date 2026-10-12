from aiogram import Router, F

from aiogram.types import ( 
    ReplyKeyboardMarkup,
      KeyboardButton, 
      InlineKeyboardMarkup,
      InlineKeyboardButton,
      CallbackQuery,
 ) 
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

router = Router()

nutrition_result_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🔄 Сгенерировать заново")
        ],
        [
            KeyboardButton(text="🛒 Список покупок")
        ],
        [
            KeyboardButton(text="📄 Рецепт блюд")
        ],
        [
            KeyboardButton(text="🏠 Главное меню")
        ],
    ],
    resize_keyboard=True
)
goal_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔥 Похудение")],
        [KeyboardButton(text="💪 Набор массы")],
        [KeyboardButton(text="⚖️ Поддержание")]
    ],
    resize_keyboard=True
)


gender_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="👨 Мужчина")],
        [KeyboardButton(text="👩 Женщина")]
    ],
    resize_keyboard=True
)


workouts_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="0-1")],
        [KeyboardButton(text="2-3")],
        [KeyboardButton(text="4-5")],
        [KeyboardButton(text="6-7")]
    ],
    resize_keyboard=True
)


activity_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🪑 Сидячий образ жизни")],
        [KeyboardButton(text="🚶 Небольшая активность")],
        [KeyboardButton(text="🏃 Активный образ жизни")],
        [KeyboardButton(text="💼 Очень активный")]
    ],
    resize_keyboard=True
)


restrictions_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Нет ограничений")],
        [KeyboardButton(text="Не ем свинину")],
        [KeyboardButton(text="Не ем рыбу")],
        [KeyboardButton(text="Вегетарианец")],
        [KeyboardButton(text="Другое")]
    ],
    resize_keyboard=True
)


meals_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="3")],
        [KeyboardButton(text="4")],
        [KeyboardButton(text="5")],
        [KeyboardButton(text="6")]
    ],
    resize_keyboard=True
)

class RecipeForm(StatesGroup):
    waiting_for_budget = State()
    waiting_for_goal = State()
    waiting_for_meals = State()


def recipe_budget_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="$200",
                    callback_data="recipe_budget_200"
                ),
                InlineKeyboardButton(
                    text="$300",
                    callback_data="recipe_budget_300"
                ),
                InlineKeyboardButton(
                    text="$400",
                    callback_data="recipe_budget_400"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="$500",
                    callback_data="recipe_budget_500"
                ),
                InlineKeyboardButton(
                    text="$600",
                    callback_data="recipe_budget_600"
                ),
                InlineKeyboardButton(
                    text="$700",
                    callback_data="recipe_budget_700"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="$800",
                    callback_data="recipe_budget_800"
                ),
                InlineKeyboardButton(
                    text="$900",
                    callback_data="recipe_budget_900"
                ),
                InlineKeyboardButton(
                    text="$1000",
                    callback_data="recipe_budget_1000"
                ),
            ],
        ]
    )


InlineKeyboardButton(
    text="🍽 Готовые рецепты",
    callback_data="nutrition_recipes"
)

keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🔄 Составить заново",
                callback_data="nutrition_again"
            )
        ],
        [
            InlineKeyboardButton(
                text="🛒 Список покупок",
                callback_data="shopping_list"
            )
        ],
        [
            InlineKeyboardButton(
                text="📄 Скачать PDF",
                callback_data="download_pdf"
            )
        ],
        [
            InlineKeyboardButton(
                text="🏠 Главное меню",
                callback_data="main_menu"
            )
        ]
    ]
)
RECIPES = [ 
    { 
      "name": "🍗 Курица с рисом и овощами", 
      "ingredients":[ 
        "Куриная грудка — 200 г",
          "Рис — 100 г",
            "Овощи — 150 г",
              "Оливковое масло — 5 г", 
            ],
          "recipe": ( "Отвари рис. Куриную грудку нарежь и обжарь "
                      "до готовности. Добавь овощи и готовь ещё 5–7 минут."
          ),
    },

    {
      "name": "🥚 Омлет с овощами",
      "ingredients": [
          "Яйца — 3 шт.",
          "Помидор — 1 шт.",
          "Болгарский перец — 100 г",
          "Сыр — 30 г",
      ],
      "recipe": (
          "Нарежь овощи и слегка обжарь. "
          "Взбей яйца, залей овощи и готовь под крышкой. "
          "В конце добавь сыр."
      ),
  },

  {
      "name": "🥣 Овсянка с бананом и творогом",
      "ingredients": [
          "Овсянка — 60 г",
          "Банан — 1 шт.",
          "Творог 5% — 150 г",
          "Корица — по вкусу",
      ],
      "recipe": (
          "Свари овсянку на воде или молоке. "
          "Добавь банан, творог и немного корицы."
      ),
  },

  {
      "name": "🐟 Хек с картофелем",
      "ingredients": [
          "Филе хека — 200 г",
          "Картофель — 250 г",
          "Овощи — 150 г",
          "Лимон — по вкусу",
      ],
      "recipe": (
          "Запеки хек с лимоном и специями около 20 минут. "
          "Картофель отвари или запеки. Подавай с овощами."
      ),
  },

  {
      "name": "🥩 Говядина с гречкой",
      "ingredients": [
          "Говядина — 180 г",
          "Гречка — 100 г",
          "Овощи — 150 г",
          "Оливковое масло — 5 г",
      ],
      "recipe": (
          "Отвари гречку. Говядину нарежь небольшими кусочками "
          "и приготовь на сковороде. Добавь овощи."
      ),
  },

  {
      "name": "🌯 ПП-лаваш с курицей",
      "ingredients": [
          "Лаваш — 1 шт.",
          "Куриная грудка — 150 г",
          "Огурец — 1 шт.",
          "Помидор — 1 шт.",
          "Греческий йогурт — 50 г",
      ],
      "recipe": (
          "Приготовь курицу. Нарежь овощи. "
          "Смажь лаваш йогуртом, добавь начинку и заверни."
      ),
  },

  {
      "name": "🥗 Салат с тунцом",
      "ingredients": [
          "Тунец в собственном соку — 150 г",
          "Яйца — 2 шт.",
          "Огурец — 1 шт.",
          "Помидоры — 150 г",
          "Зелень — по вкусу",
      ],
      "recipe": (
          "Отвари яйца. Нарежь овощи и яйца. "
          "Добавь тунец и зелень. Перемешай."
      ),
  },

  {
      "name": "🍝 Паста с курицей",
      "ingredients": [
          "Макароны из твёрдых сортов — 100 г",
          "Куриная грудка — 180 г",
          "Помидоры — 150 г",
          "Пармезан — 15 г",
      ],
      "recipe": (
          "Отвари пасту. Курицу нарежь и обжарь. "
          "Добавь помидоры, затем смешай с пастой "
          "и посыпь небольшим количеством сыра."
      ),
  },

  {
      "name": "🥞 ПП-сырники",
      "ingredients": [
          "Творог 5% — 200 г",
          "Яйцо — 1 шт.",
          "Овсяная мука — 30 г",
          "Подсластитель — по вкусу",
      ],
      "recipe": (
          "Смешай все ингредиенты. Сформируй небольшие сырники "
          "и приготовь на антипригарной сковороде "
          "или запеки в духовке."
      ),
  },

  {
      "name": "🍲 Индейка с гречкой и овощами",
      "ingredients": [
          "Филе индейки — 200 г",
          "Гречка — 100 г",
          "Брокколи — 100 г",
          "Морковь — 50 г",
      ],
      "recipe": (
          "Отвари гречку. Индейку нарежь и приготовь "
          "на сковороде. Добавь брокколи и морковь "
          "и туши до готовности."
      ),
  },

]

{
    "name": "🍗 Куриная грудка с гречкой и грибами",
    "ingredients": [
        "Куриная грудка — 180 г",
        "Гречка — 100 г",
        "Шампиньоны — 100 г",
        "Лук — 50 г",
    ],
    "recipe": (
        "Отвари гречку. Куриную грудку нарежь небольшими кусочками "
        "и обжарь до готовности. Добавь грибы и лук, "
        "туши ещё 7–10 минут. Подавай с гречкой."
    ),
},

{
    "name": "🐟 Лосось с рисом и брокколи",
    "ingredients": [
        "Филе лосося — 180 г",
        "Рис — 100 г",
        "Брокколи — 150 г",
        "Лимон — по вкусу",
    ],
    "recipe": (
        "Посоли и поперчи лосось, добавь лимон и запекай "
        "при 180°C около 15–20 минут. Отдельно приготовь рис "
        "и брокколи."
    ),
},

{
    "name": "🥩 Котлеты из индейки с картофелем",
    "ingredients": [
        "Фарш из индейки — 200 г",
        "Картофель — 250 г",
        "Яйцо — 1 шт.",
        "Лук — 50 г",
    ],
    "recipe": (
        "Смешай фарш с яйцом и мелко нарезанным луком. "
        "Сформируй котлеты и запеки или приготовь на антипригарной "
        "сковороде. Картофель отвари или запеки."
    ),
},

{
    "name": "🥗 Салат с курицей и авокадо",
    "ingredients": [
        "Куриная грудка — 150 г",
        "Авокадо — 1/2 шт.",
        "Огурец — 1 шт.",
        "Помидоры — 150 г",
        "Греческий йогурт — 50 г",
    ],
    "recipe": (
        "Приготовь куриную грудку и нарежь её. "
        "Нарежь овощи и авокадо. Смешай все ингредиенты "
        "и заправь греческим йогуртом."
    ),
},

{
    "name": "🍳 Яичница с курицей и овощами",
    "ingredients": [
        "Яйца — 3 шт.",
        "Куриная грудка — 100 г",
        "Помидор — 1 шт.",
        "Болгарский перец — 100 г",
    ],
    "recipe": (
        "Нарежь курицу и овощи, приготовь их на сковороде. "
        "Добавь яйца и готовь под крышкой до желаемой степени."
    ),
},

{
    "name": "🥣 Творожная запеканка",
    "ingredients": [
        "Творог 5% — 250 г",
        "Яйца — 2 шт.",
        "Овсяная мука — 30 г",
        "Банан — 1/2 шт.",
        "Подсластитель — по вкусу",
    ],
    "recipe": (
        "Смешай творог, яйца, овсяную муку и банан. "
        "Переложи массу в форму и запекай при 180°C "
        "около 30–35 минут."
    ),
},

{
    "name": "🌯 Тунец в лаваше",
    "ingredients": [
        "Лаваш — 1 шт.",
        "Тунец в собственном соку — 150 г",
        "Огурец — 1 шт.",
        "Помидор — 1 шт.",
        "Греческий йогурт — 50 г",
    ],
    "recipe": (
        "Смешай тунец с йогуртом. Нарежь овощи. "
        "Выложи всё на лаваш, заверни и слегка прогрей "
        "на сухой сковороде."
    ),
},

{
    "name": "🍝 Паста с тунцом и томатами",
    "ingredients": [
        "Паста из твёрдых сортов — 100 г",
        "Тунец — 150 г",
        "Помидоры — 150 г",
        "Чеснок — 1 зубчик",
    ],
    "recipe": (
        "Отвари пасту. На сковороде приготовь помидоры "
        "с чесноком, добавь тунец. Смешай с готовой пастой."
    ),
},

{
    "name": "🥞 Овсяноблин с творогом",
    "ingredients": [
        "Овсяные хлопья — 50 г",
        "Яйца — 2 шт.",
        "Творог — 100 г",
        "Банан — 1/2 шт.",
    ],
    "recipe": (
        "Измельчи овсянку, смешай с яйцами и приготовь "
        "блин на антипригарной сковороде. "
        "Добавь творог и банан, сложи пополам."
    ),
},

{
    "name": "🍲 Куриный суп с овощами",
    "ingredients": [
        "Куриная грудка — 180 г",
        "Картофель — 150 г",
        "Морковь — 70 г",
        "Лук — 50 г",
        "Зелень — по вкусу",
    ],
    "recipe": (
        "Отвари куриную грудку. Добавь картофель, морковь "
        "и лук. Вари до готовности овощей. "
        "В конце добавь зелень и специи."
    ),
},

@router.callback_query(F.data == "nutrition_recipes") 
async def nutrition_recipes( callback
: CallbackQuery, state: FSMContext, ):
    await callback.answer()

    await state.set_state(
        RecipeForm.waiting_for_budget
    )

    await callback.message.answer(
        "🍽 <b>Персональные рецепты</b>\n\n"
        "Сначала определим ваш бюджет на продукты.\n\n"
        "💰 Выберите бюджет на продукты в месяц:",
        reply_markup=recipe_budget_keyboard(),
        parse_mode="HTML",
    )

@router.callback_query( RecipeForm.waiting_for_budget, F.data.startswith("recipe_budget_") )
async def recipe_budget( callback: CallbackQuery, state: FSMContext, ):
  await callback.answer()

  budget = int(
      callback.data.replace("recipe_budget_", "")
  )

  await state.update_data(
      recipe_budget=budget
  )

  await state.set_state(
      RecipeForm.waiting_for_goal
  )

  keyboard = InlineKeyboardMarkup(
      inline_keyboard=[
          [
              InlineKeyboardButton(
                  text="🔥 Похудение",
                  callback_data="recipe_goal_cut"
              )
          ],
          [
              InlineKeyboardButton(
                  text="💪 Набор массы",
                  callback_data="recipe_goal_bulk"
              )
          ],
          [
              InlineKeyboardButton(
                  text="⚖️ Поддержание веса",
                  callback_data="recipe_goal_maintain"
              )
          ],
          [
              InlineKeyboardButton(
                  text="🏋️ Спортивное питание",
                  callback_data="recipe_goal_sport"
              )
          ],
      ]
  )

  await callback.message.answer(
      f"💰 Бюджет: <b>${budget}/месяц</b>\n\n"
      "🎯 Какая у вас цель?",
      reply_markup=keyboard,
      parse_mode="HTML",
  )

@router.callback_query( RecipeForm.waiting_for_goal, F.data.startswith("recipe_goal_") )
async def recipe_goal( callback: CallbackQuery, state: FSMContext, ):
    await callback.answer()

    goals = {
        "recipe_goal_cut": "Похудение",
        "recipe_goal_bulk": "Набор массы",
        "recipe_goal_maintain": "Поддержание веса",
        "recipe_goal_sport": "Спортивное питание",
    }

    goal = goals.get(callback.data)

    await state.update_data(
        recipe_goal=goal
    )

    await state.set_state(
        RecipeForm.waiting_for_meals
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🍽 3 раза",
                    callback_data="recipe_meals_3"
                ),
                InlineKeyboardButton(
                    text="🍽 4 раза",
                    callback_data="recipe_meals_4"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🍽 5 раз",
                    callback_data="recipe_meals_5"
                ),
                InlineKeyboardButton(
                    text="🍽 6 раз",
                    callback_data="recipe_meals_6"
                ),
            ],
        ]
    )

    await callback.message.answer(
        f"🎯 Цель: <b>{goal}</b>\n\n"
        "🍽 Сколько раз в день вы хотите питаться?",
        reply_markup=keyboard,
        parse_mode="HTML",
    ) 

@router.callback_query( 
    RecipeForm.waiting_for_meals,
    F.data.startswith("recipe_meals_") 
) 
async def recipe_meals( 
   callback: CallbackQuery,
   state: FSMContext, 
):
  await callback.answer()

  meals = int(
      callback.data.replace("recipe_meals_", "")
  )

  await state.update_data(
      recipe_meals=meals
  )

  data = await state.get_data()

  await callback.message.answer(
      "🤖 <b>Составляю персональное меню...</b>\n\n"
      f"💰 Бюджет: ${data['recipe_budget']}/месяц\n"
      f"🎯 Цель: {data['recipe_goal']}\n"
      f"🍽 Приёмов пищи: {meals}\n\n"
      "⏳ Подбираю продукты и рассчитываю примерную стоимость...",
      parse_mode="HTML",
  )

  try:
    program = await create_recipe_program(data)

  except Exception as e:
    
      print(f"Recipe AI error: {e}")

      await callback.message.answer(
          "❌ Не удалось создать рецепты.\n"
          "Попробуйте ещё раз немного позже."
      )

      await state.clear()
      return

  await state.clear()

  parts = []
  while len(program) > 4000: split_at = program.rfind("\n", 0, 4000)


  if split_at == -1:
      split_at = 4000

  parts.append(program[:split_at])
  program = program[split_at:].lstrip()

  if program: parts.append(program)

  for part in parts: 
      await callback.message.answer(
          part,
          parse_mode="HTML",
      )



async def create_recipe_program(data: dict) -> str: 
    """
     Создаёт персональную программу рецептов
     на основе бюджета, цели и данных пользователя. 
     """
   
    budget = data.get("recipe_budget", 200)
    goal = data.get("recipe_goal", "Поддержание веса")
    meals = data.get("recipe_meals", 3)

    age = data.get("age", "не указано")
    gender = data.get("gender", "не указано")
    height = data.get("height", "не указано")
    weight = data.get("weight", "не указано")
    activity = data.get("activity", "не указано")
    restrictions = data.get("restrictions", "нет")
    favorite_foods = data.get("favorite_foods", "не указано")

    prompt = f"""
    
    Ты профессиональный AI-диетолог и специалист по спортивному питанию.
    Составь персональную программу из 20 рецептов для пользователя.
    ДАННЫЕ ПОЛЬЗОВАТЕЛЯ:
    Возраст: {age} Пол: {gender} Рост: {height} см Вес: {weight} кг Активность: {activity}
    ЦЕЛЬ: {goal}
    КОЛИЧЕСТВО ПРИЁМОВ ПИЩИ: {meals} в день
    МЕСЯЧНЫЙ БЮДЖЕТ: ${budget}
    ОГРАНИЧЕНИЯ В ПИТАНИИ: {restrictions}
    ЛЮБИМЫЕ ПРОДУКТЫ: {favorite_foods}
    ГЛАВНЫЕ ТРЕБОВАНИЯ:
    Создай ровно 20 разных рецептов.
    Рецепты должны соответствовать цели пользователя:
    похудение
    набор массы
    поддержание веса
    спортивное питание.
    Учитывай месячный бюджет ${budget}.
    Используй доступные продукты и старайся не превышать месячный бюджет.
    Для каждого рецепта укажи:
    название;
    категорию приёма пищи;
    ингредиенты;
    количество каждого ингредиента;
    примерную стоимость ингредиентов;
    примерную стоимость одной порции;
    калории;
    белки;
    жиры;
    углеводы;
    способ приготовления.
    Используй количество приёмов пищи: {meals} в день.
    Сделай рецепты практичными и простыми для приготовления дома.
    Не используй продукты, которые пользователь указал как запрещённые.
    По возможности используй любимые продукты пользователя.
    В конце сделай:
    примерную стоимость одного дня;
    примерную стоимость недели;
    примерную стоимость месяца;
    примерное количество калорий в день;
    примерные БЖУ в день.
    ВАЖНО:
    Стоимость продуктов является ориентировочной. Не утверждай, что цены точные.
    Не пиши длинное вступление. Сразу начинай с рецептов.
    Формат:
    🍽 РЕЦЕПТ 1 Название
    🥣 Приём пищи: ...
    🛒 Ингредиенты: • продукт — количество — ~$стоимость
    💰 Стоимость порции: ~$X
    🔥 Калории: ~X ккал
    🥩 Белки: ~X г
    🥑 Жиры: ~X г
    🍚 Углеводы: ~X г
    👨‍🍳 Приготовление: ...
    ──────────────────
    После 20 рецептов:
    📊 ИТОГ
    💵 В день: ~$X
    💵 В неделю: ~$X
    💵 В месяц: ~$X
    🔥 Калории в день: ~X ккал
    🥩 Белки: ~X г
    🥑 Жиры: ~X г
    🍚 Углеводы: ~X г """

    response = await client.responses.create(
    model="gpt-5",
    input=prompt,
)

    return response.output_text





# Здесь следующим шагом подключим AI





@router.callback_query(F.data == "nutrition_back")
async def nutrition_back(callback: CallbackQuery):
    await callback.answer()

    await callback.message.answer(
        "🥗 Возвращаемся к программе питания."
    ) 





    
