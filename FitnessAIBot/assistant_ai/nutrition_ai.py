
import os
from openai import AsyncOpenAI

client = AsyncOpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)



async def create_nutrition_program(data: dict) -> str:
  prompt = f"""
Ты профессиональный диетолог и фитнес-тренер.

Составь персональную программу питания.

Данные пользователя:

🎯 Цель: {data["goal"]}
📏 Рост: {data["height"]} см
⚖️ Вес: {data["weight"]} кг
🎂 Возраст: {data["age"]}
👤 Пол: {data["gender"]}
🏋️ Тренировок в неделю: {data["workouts"]}
🚶 Активность: {data["activity"]}
🥗 Ограничения: {data["restrictions"]}
💰 Бюджет: {data["budget"]}$ в месяц
🍽 Приёмов пищи: {data["meals"]}
❤️ Любимые продукты: {data["favorite_foods"]}

Составь программу питания НА 7 ДНЕЙ.

Для каждого дня укажи:

📅 День недели

🍳 Завтрак

🥪 Перекус

🍲 Обед

🥛 Перекус

🍗 Ужин

Для каждого приёма пищи обязательно укажи:

• продукты;
• вес продуктов в граммах;
• примерные калории;
• белки;
• жиры;
• углеводы.

После семи дней добавь:

📊 Суточную норму:
- Калории
- Белки
- Жиры
- Углеводы

🛒 Общий список покупок на неделю.

💰 Стоимость питания:
- за день;
- за неделю;
- за месяц.

Используй обычные продукты, которые можно купить в Украине.

Ответ красиво оформи с эмодзи.
"""
  
  response = await client.responses.create(
        model="gpt-5",
        input=prompt,
    )

  return response.output_text
