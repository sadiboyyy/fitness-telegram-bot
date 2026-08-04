
from email.mime import message

from aiogram import  Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Bot
import os
from aiogram.types import FSInputFile

from keyboards.menu import main_menu
from assistant_ai.voice_ai import (
    speech_to_text,
    fitness_voice_answer,
    text_to_speech, 
)

router = Router()

class VoiceChatForm(StatesGroup):
   waiting_voice = State()
   

@router.message(F.text == "🎙 Голосовой фитнес-чат")
async def start_voice_chat(
    message: Message,
    state: FSMContext
):
    await state.clear()
    await state.set_state(VoiceChatForm.waiting_voice)

    await message.answer(
        "🎙 Голосовой фитнес-чат\n\n"
        "Отправьте мне голосовое сообщение.\n\n"
        "Я отвечаю только на вопросы по:\n\n"
        "💪 тренировкам\n"
        "🏋️ упражнениям\n"
        "🥗 питанию\n"
        "⚖️ похудению\n"
        "📈 набору мышечной массы\n"
        "💊 спортивным добавкам\n"
        "😴 восстановлению\n\n"
        "⏱ Максимальная длительность голосового сообщения — 60 секунд.\n\n"
        "Для выхода нажмите «🏠 Главное меню».",
    )

@router.message(
    VoiceChatForm.waiting_voice,
    F.text == "🏠 Главное меню"
)
async def exit_voice_chat(
    message: Message,
    state: FSMContext
):
    await state.clear()

    await message.answer(
        "🏠 Вы вернулись в главное меню.",
        reply_markup=main_menu
    )


@router.message(
    VoiceChatForm.waiting_voice,
    F.voice
)
async def receive_voice(
    message: Message,
    state: FSMContext,
    bot: Bot
):
    voice = message.voice

    if voice.duration > 60:
      await message.answer(
        "❌ Голосовое сообщение должно быть не длиннее 60 секунд."
      )
      return

    os.makedirs("voice", exist_ok=True)

    telegram_file = await bot.get_file(voice.file_id)

    user_voice_path = "voice/user_voice.ogg"

    await bot.download_file(
       telegram_file.file_path,
       destination=user_voice_path
    )

    await message.answer("🎤 Распознаю речь...")

    question = await speech_to_text(user_voice_path)

    await message.answer("🤖 Думаю над ответом...")

    answer = await fitness_voice_answer(question)

    await message.answer("🔊 Озвучиваю ответ...")

    voice_path = await text_to_speech(answer)

    voice_file = FSInputFile(voice_path)

    await message.answer_voice(
    voice=voice_file
)

class VoiceChatForm(StatesGroup):
    waiting_voice = State()