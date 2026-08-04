from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def generate_fact(category):

    response = client.responses.create(
        model="gpt-5",
        input=f"""
Ты фитнес-эксперт.

Категория:

{category}

Придумай один интересный факт.

Требования:

• факт должен быть уникальным
• максимум 120 слов
• без повторов
• если возможно — удиви пользователя
• пиши простым языком
• добавь немного эмодзи
• не выдумывай сомнительные медицинские утверждения
"""
    )

    return response.output_text