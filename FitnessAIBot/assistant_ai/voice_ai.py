import os
from openai import AsyncOpenAI
from pathlib import Path

client = AsyncOpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


async def fitness_voice_answer(question: str) -> str:
    response = await client.responses.create(
        model="gpt-5",
        input=f"""
Ты профессиональный фитнес-тренер.

Отвечай ТОЛЬКО на темы:

- тренировки
- упражнения
- питание
- похудение
- набор массы
- восстановление
- спортивные добавки

Если вопрос не относится к фитнесу — ответь:

"Я отвечаю только на вопросы по фитнесу."

Вопрос пользователя:

{question}
"""
    )

    return response.output_text

from pathlib import Path


async def speech_to_text(audio_path: str) -> str:
    with open(audio_path, "rb") as audio_file:
        transcript = await client.audio.transcriptions.create(
            model="gpt-4o-mini-transcribe",
            file=audio_file,
        )

    return transcript.text
import os


async def text_to_speech(text: str) -> str:
    os.makedirs("voice", exist_ok=True)

    output_path = "voice/assistant_answer.mp3"

    async with client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=text,
    ) as response:
        await response.stream_to_file(output_path)

    return output_path