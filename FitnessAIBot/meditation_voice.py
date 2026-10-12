import os
import subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed 

from openai import OpenAI

from pathlib import Path
import subprocess

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def create_meditation_voice(
    user_id: int,
    text: str,
    voice: str,
    goal: str,
    duration: int,
):
    """
    Создаёт голос медитации блоками
    и добавляет реальные паузы между блоками.
    """


    if voice == "male":
        openai_voice = "onyx"
    else:
        openai_voice = "shimmer"

    # --------------------------------
    # 2. Определяем папку
    # --------------------------------

    goal_folders = {
        "😌 Снять стресс": "stress",
        "🧠 Концентрация": "focus",
        "💤 Перед сном": "sleep",
        "💪 После тренировки": "recovery",
    }

    goal_folder = goal_folders.get(
        goal,
        "stress",
    )

    audio_dir = (
        Path("media")
        / "meditation"
        / voice
        / goal_folder
    )

    audio_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    # --------------------------------
    # 3. Разбиваем текст на фразы
    # --------------------------------

    phrases = [
        phrase.strip()
        for phrase in text.split("\n")
        if phrase.strip()
    ]

    print(
        f"Медитация: {len(phrases)} фраз"
    )

    # --------------------------------
    # 4. Объединяем фразы в блоки
    # --------------------------------

    BLOCK_SIZE = 6

    phrase_blocks = [
        phrases[i:i + BLOCK_SIZE]
        for i in range(
            0,
            len(phrases),
            BLOCK_SIZE,
        )
    ]

    print(
        f"Будет создано {len(phrase_blocks)} голосовых блоков"
    )

    generated_files = []

    # --------------------------------
    # 5. Генерируем голосовые блоки
    # --------------------------------

    # --------------------------------
    # 5. Генерируем до 5 блоков одновременно
    # --------------------------------

    def generate_block(index, block):
        block_text = "\n\n".join(block)

        block_path = (
            audio_dir
            / f"user_{user_id}_block_{index}.mp3"
        )

        print(
            f"🎙 Начинаю блок "
            f"{index + 1}/{len(phrase_blocks)}"
        )

        with client.audio.speech.with_streaming_response.create(
            model="gpt-4o-mini-tts",
            voice=openai_voice,
            input=block_text,
            instructions=(
                "Speak in Russian. "
                "Use a very calm, warm and soft meditation voice. "
                "Speak slowly and smoothly. "
                "Use gentle peaceful intonation. "
                "Pause naturally between sentences. "
                "Do not rush. "
                "Do not sound energetic. "
                "Sound like a professional guided meditation instructor."
            ),
        ) as response:

            response.stream_to_file(
                block_path
            )

        print(
            f"✅ Готов блок "
            f"{index + 1}/{len(phrase_blocks)}"
        )

        return (
            index,
            block_path,
            block_text,
        )

    # Максимум 5 запросов одновременно
    results = []

    with ThreadPoolExecutor(
        max_workers=5
    ) as executor:

        futures = [
            executor.submit(
                generate_block,
                index,
                block,
            )
            for index, block in enumerate(
                phrase_blocks
            )
        ]

        for future in as_completed(futures):
            result = future.result()
            results.append(result)

    # Важно!
    # Параллельные блоки заканчиваются
    # в случайном порядке.
    # Поэтому возвращаем правильный порядок.
    results.sort(
        key=lambda item: item[0]
    )

    generated_files = [
        (
            block_path,
            block_text,
        )
        for index, block_path, block_text
        in results
    ]
    # --------------------------------
    # 6. Создаём файл тишины
    # --------------------------------

    silence_dir = (
        Path("media")
        / "meditation"
        / "silence"
    )

    silence_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    silence_path = (
        silence_dir
        / "silence_10.mp3"
    )

    if not silence_path.exists():

        silence_command = [
            "ffmpeg",
            "-y",
            "-f",
            "lavfi",
            "-i",
            "anullsrc=r=24000:cl=mono",
            "-t",
            "10",
            "-c:a",
            "libmp3lame",
            "-b:a",
            "128k",
            str(silence_path),
        ]

        subprocess.run(
            silence_command,
            check=True,
        )

    # --------------------------------
    # 7. Создаём concat-файл
    # --------------------------------

    concat_file = (
        audio_dir
        / f"user_{user_id}_concat.txt"
    )

    with open(
        concat_file,
        "w",
        encoding="utf-8",
    ) as file:

        for block_path, block_text in generated_files:

            file.write(f"file '{block_path.resolve()}'\n"
            )

            file.write(
                f"file '{silence_path.resolve()}'\n"
            )

    # --------------------------------
    # 8. Склеиваем голос + паузы
    # --------------------------------

    output_path = (
        audio_dir
        / f"user_{user_id}.mp3"
    )

    command = [
        "ffmpeg",
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(concat_file),
        "-c:a",
        "libmp3lame",
        "-b:a",
        "192k",
        str(output_path),
    ]

    subprocess.run(
        command,
        check=True,
    )

    # --------------------------------
    # 9. Ограничиваем длительность
    # --------------------------------

    target_seconds = duration * 60

    trimmed_path = (
        audio_dir
        / f"user_{user_id}_final.mp3"
    )

    trim_command = [
        "ffmpeg",
        "-y",
        "-i",
        str(output_path),
        "-t",
        str(target_seconds),
        "-c:a",
        "libmp3lame",
        "-b:a",
        "192k",
        str(trimmed_path),
    ]

    subprocess.run(
        trim_command,
        check=True,
    )

    # --------------------------------
    # 10. Удаляем временные блоки
    # --------------------------------

    for block_path, block_text in generated_files:
        try:
            block_path.unlink()
        except Exception:
            pass

    try:
        concat_file.unlink()
    except Exception:
        pass

    # --------------------------------
    # 11. Возвращаем готовую медитацию
    # --------------------------------

    return str(trimmed_path)



def add_meditation_pauses(
    audio_files: list,
    user_id: int,
    pause_seconds: float = 6.0,
) -> str:
    pass
    """
    Склеивает голосовые фрагменты,
    добавляя настоящую тишину между ними.
    """

    output_dir = (
        Path("media")
        / "meditation"
        / "generated"
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    silence_path = (
        output_dir
        / f"silence_{user_id}.mp3"
    )

    # Создаём файл тишины нужной длины
    silence_command = [
        "ffmpeg",
        "-y",
        "-f",
        "lavfi",
        "-i",
        "anullsrc=r=24000:cl=mono",
        "-t",
        str(pause_seconds),
        "-c:a",
        "libmp3lame",
        "-b:a",
        "128k",
        str(silence_path),
    ]

    subprocess.run(
        silence_command,
        check=True,
    )

    # Создаём список:
    # фраза -> тишина -> фраза -> тишина...
    concat_file = (
        output_dir
        / f"concat_{user_id}.txt"
    )

    with open(
        concat_file,
        "w",
        encoding="utf-8",
    ) as file:

        for audio_file in audio_files:

            audio_absolute = Path(
                audio_file
            ).resolve()

            silence_absolute = (
                silence_path.resolve()
            )

            file.write(
                f"file '{audio_absolute}'\n"
            )

            file.write(
                f"file '{silence_absolute}'\n"
            )

    final_path = (
        output_dir
        / f"voice_with_pauses_{user_id}.mp3"
    )

    concat_command = [
        "ffmpeg",
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(concat_file),
        "-c:a",
        "libmp3lame",
        "-b:a",
        "192k",
        str(final_path),
    ]

    subprocess.run(
        concat_command,
        check=True,
    )

    return str(final_path)

def mix_meditation_audio(
    voice_path: str,
    music_path: str,
    user_id: int,
) -> str:
    """
    Смешивает голос медитации с фоновой музыкой.
    """

    output_dir = (
        Path("media")
        / "meditation"
        / "generated"
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = (
        output_dir
        / f"meditation_{user_id}.mp3"
    )

    command = [
        "ffmpeg",
        "-y",

        "-i",
        str(voice_path),

        "-stream_loop",
        "-1",
        "-i",
        str(music_path),

        "-filter_complex",
        (
            "[0:a]volume=1.5[voice];"
            "[1:a]volume=0.12[music];"
            "[voice][music]"
            "amix=inputs=2:duration=first:"
            "dropout_transition=2[a]"
        ),

        "-map",
        "[a]",

        "-c:a",
        "libmp3lame",

        "-b:a",
        "192k",

        str(output_path),
    ]

    result = subprocess.run(
            command,
            capture_output=True,
            text=True,
    )

    if result.returncode != 0:
        print("❌ FFMPEG ОШИБКА:")
        print(result.stderr)

        raise RuntimeError(
            f"FFmpeg завершился с кодом {result.returncode}"
        )

    print(
            f"🎵 Готовая медитация: {output_path}"
    )

    return str(output_path)