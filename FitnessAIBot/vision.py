import os
import base64
from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def analyze_frames(exercise_name: str):

    content = [
        {
            "type": "input_text",
            "text":
            f"""
Ты профессиональный фитнес-тренер.

Пользователь выполняет упражнение:

{exercise_name}

Проанализируй технику.

Ответь строго по пунктам.

1. Что сделано правильно.

2. Какие ошибки.

3. Что может привести к травме.

4. Что исправить.

5. Оцени технику от 1 до 10.
"""
        }
    ]

    for filename in sorted(os.listdir("frames")):

        path = os.path.join("frames", filename)

        with open(path, "rb") as f:

            image = base64.b64encode(
                f.read()
            ).decode()

        content.append(
            {
                "type": "input_image",
                "image_url":
                f"data:image/jpeg;base64,{image}"
            }
        )

    response = client.responses.create(

        model="gpt-5",

        input=[
            {
                "role": "user",
                "content": content
            }
        ]

    )

    return response.output_text