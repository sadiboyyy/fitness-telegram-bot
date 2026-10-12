from pathlib import Path
import random
from pathlib import Path
import random
import subprocess

from openai import OpenAI


client = OpenAI()


BASE_DIR = Path(__file__).resolve().parent

AUDIO_DIR = BASE_DIR / "media" / "stretching"
GENERATED_DIR = AUDIO_DIR / "generated"

GENERATED_DIR.mkdir(parents=True, exist_ok=True)


STRETCHING_EXERCISES = {

    # ==================================================
    # ВСЁ ТЕЛО
    # ==================================================

    "🧘 Всё тело": [

        {
            "text": (
                "Начинаем с шеи. Сядь или встань ровно. "
                "Медленно наклони голову вправо. "
                "Плечи оставь расслабленными."
            ),
            "seconds": 30,
            "level": 1,
        },

        {
            "text": (
                "Теперь медленно наклони голову влево. "
                "Не дави на голову рукой. "
                "Почувствуй мягкое растяжение шеи."
            ),
            "seconds": 30,
            "level": 1,
        },

        {
            "text": (
                "Переходим к плечам. "
                "Выпрями правую руку перед собой "
                "и мягко прижми её к груди левой рукой."
            ),
            "seconds": 30,
            "level": 2,
        },

        {
            "text": (
                "Теперь поменяй сторону. "
                "Левую руку прижми к груди. "
                "Плечо держи расслабленным."
            ),
            "seconds": 30,
            "level": 2,
        },

        {
            "text": (
                "Подними правую руку вверх, согни её в локте "
                "и заведи ладонь за спину. "
                "Другой рукой мягко направляй локоть назад."
            ),
            "seconds": 30,
            "level": 2,
        },

        {
            "text": (
                "Поменяй руку. "
                "Не прогибай поясницу и продолжай спокойно дышать."
            ),
            "seconds": 30,
            "level": 2,
        },

        {
            "text": (
                "Соедини руки за спиной и осторожно отведи их назад. "
                "Раскрой грудную клетку и опусти плечи."
            ),
            "seconds": 35,
            "level": 2,
        },

        {
            "text": (
                "Поставь ноги немного шире плеч. "
                "Медленно наклони корпус вперёд. "
                "Колени можешь слегка согнуть."
            ),
            "seconds": 40,
            "level": 3,
        },

        {
            "text": (
                "Перенеси вес к правой ноге, слегка согни её, "
                "а левую оставь прямой. "
                "Почувствуй растяжение внутренней поверхности бедра."
            ),
            "seconds": 35,
            "level": 3,
        },

        {
            "text": (
                "Теперь плавно перенеси вес на левую сторону. "
                "Правую ногу оставь прямой."
            ),
            "seconds": 35,
            "level": 3,
        },

        {
            "text": (
                "Согни правую ногу назад и аккуратно "
                "подтяни стопу к ягодице. "
                "Колени держи рядом."
            ),
            "seconds": 30,
            "level": 3,
        },

        {
            "text": (
                "Поменяй ногу. "
                "Сохраняй корпус ровным и не тяни стопу слишком сильно."
            ),
            "seconds": 30,
            "level": 3,
        },

        {
            "text": (
                "Сделай спокойный выпад правой ногой вперёд. "
                "Мягко опускай таз вниз, растягивая переднюю "
                "поверхность левого бедра."
            ),
            "seconds": 35,
            "level": 3,
        },

        {
            "text": (
                "Поменяй стороны. "
                "Левая нога впереди, таз плавно направляй вниз."
            ),
            "seconds": 35,
            "level": 3,
        },

        {
            "text": (
                "Сядь на пол и выпрями ноги перед собой. "
                "Медленно наклоняй корпус вперёд. "
                "Не пытайся любой ценой достать руками до стоп."
            ),
            "seconds": 40,
            "level": 2,
        },

        {
            "text": (
                "Соедини стопы перед собой и разведи колени в стороны. "
                "Выпрями спину и слегка наклонись вперёд."
            ),
            "seconds": 40,
            "level": 2,
        },

        {
            "text": (
                "Встань на четвереньки. "
                "Медленно округли спину и опусти голову. "
                "Затем плавно вернись в нейтральное положение."
            ),
            "seconds": 35,
            "level": 2,
        },

        {
            "text": ("Из положения на четвереньках медленно "
                "отведи таз назад к пяткам. "
                "Руки вытяни вперёд."
            ),
            "seconds": 45,
            "level": 2,
        },

        {
            "text": (
                "Ляг на спину и подтяни оба колена к груди. "
                "Обхвати их руками и расслабь поясницу."
            ),
            "seconds": 40,
            "level": 1,
        },

        {
            "text": (
                "Оставаясь на спине, вытяни руки в стороны "
                "и аккуратно опусти согнутые колени вправо. "
                "Плечи старайся не отрывать от пола."
            ),
            "seconds": 35,
            "level": 1,
        },

        {
            "text": (
                "Теперь медленно переведи колени на левую сторону. "
                "Дыши глубоко и расслабь мышцы спины."
            ),
            "seconds": 35,
            "level": 1,
        },
    ],


    # ==================================================
    # НОГИ
    # ==================================================

    "🦵 Ноги": [

        {
            "text": (
                "Поставь правую ногу впереди. "
                "Левую отведи назад и мягко опускай таз вниз."
            ),
            "seconds": 40,
            "level": 1,
        },

        {
            "text": (
                "Поменяй положение ног. "
                "Двигайся плавно и не допускай боли."
            ),
            "seconds": 40,
            "level": 1,
        },

        {
            "text": (
                "Выпрями правую ногу перед собой. "
                "Медленно наклони корпус к ней."
            ),
            "seconds": 35,
            "level": 1,
        },

        {
            "text": (
                "Поменяй ногу и повтори наклон. "
                "Не округляй спину слишком сильно."
            ),
            "seconds": 35,
            "level": 1,
        },

        {
            "text": (
                "Стоя согни правую ногу и подтяни стопу к ягодице. "
                "Колени держи рядом."
            ),
            "seconds": 30,
            "level": 1,
        },

        {
            "text": (
                "Теперь растяни переднюю поверхность левого бедра. "
                "Корпус сохраняй вертикальным."
            ),
            "seconds": 30,
            "level": 2,
        },

        {
            "text": (
                "Поставь ноги широко. "
                "Согни правое колено и плавно перенеси вес вправо."
            ),
            "seconds": 35,
            "level": 2,
        },

        {
            "text": (
                "Перенеси вес на левую ногу. "
                "Правую оставь прямой."
            ),
            "seconds": 35,
            "level": 2,
        },

        {
            "text": (
                "Сядь на пол. Соедини стопы вместе "
                "и позволь коленям опуститься в стороны."
            ),
            "seconds": 40,
            "level": 2,
        },

        {
            "text": (
                "Сядь и широко разведи прямые ноги. "
                "Медленно наклоняй корпус вперёд."
            ),
            "seconds": 40,
            "level": 3,
        },

        {
            "text": (
                "Из положения сидя потянись корпусом "
                "к правой ноге. Не делай рывков."
            ),
            "seconds": 35,
            "level": 3,
        },

        {
            "text": (
                "Теперь плавно потянись к левой ноге."
            ),
            "seconds": 35,
            "level": 3,
        },

        {
            "text": (
                "Встань лицом к опоре. "
                "Поставь правую ногу назад и прижми пятку к полу. "
                "Растягиваем икроножную мышцу."
            ),
            "seconds": 30,
            "level": 3,
        },

        {
            "text": (
                "Поменяй ноги и растяни левую икроножную мышцу."
            ),
            "seconds": 30,
            "level": 3,
        },

        {
            "text": (
                "Ляг на спину. Подними правую ногу вверх "
                "и аккуратно подтяни её к себе, удерживая бедро руками."
            ),
            "seconds": 35,
            "level": 3,
        },

        {
            "text": (
                "Теперь подними левую ногу "
                "и повтори растяжение задней поверхности бедра."
            ),
            "seconds": 35,
            "level": 3,
        },
    ],
    # ==================================================
    # СПИНА
    # ==================================================

    "🧍 Спина": [

        {
            "text": (
                "Встань на четвереньки. "
                "Медленно округли спину и направь подбородок к груди."
            ),
            "seconds": 30,
            "level": 1,
        },

        {
            "text": (
                "Теперь плавно верни позвоночник "
                "в нейтральное положение."
            ),
            "seconds": 25,
            "level": 1,
        },

        {
            "text": (
                "Отведи таз назад к пяткам. "
                "Руки вытяни далеко вперёд и расслабь спину."
            ),
            "seconds": 45,
            "level": 1,
        },

        {
            "text": (
                "Из положения на четвереньках проведи правую руку "
                "под левой и мягко опусти правое плечо к полу."
            ),
            "seconds": 35,
            "level": 2,
        },

        {
            "text": (
                "Вернись и выполни движение другой рукой. "
                "Левую руку проведи под правой."
            ),
            "seconds": 35,
            "level": 1,
        },

        {
            "text": (
                "Сядь ровно. Поверни корпус вправо, "
                "не двигая таз."
            ),
            "seconds": 30,
            "level": 3,
        },

        {
            "text": (
                "Теперь медленно поверни корпус влево."
            ),
            "seconds": 30,
            "level": 2,
        },

        {
            "text": (
                "Ляг на спину и подтяни колени к груди. "
                "Расслабь поясницу."
            ),
            "seconds": 40,
            "level": 1,
        },

        {
            "text": (
                "Лёжа на спине, опусти согнутые колени вправо. "
                "Руки расположи в стороны."
            ),
            "seconds": 35,
            "level": 2,
        },

        {
            "text": (
                "Теперь переведи колени на левую сторону."
            ),
            "seconds": 35,
            "level": 2,
        },

        {
            "text": (
                "Сядь на пятки и потянись руками вперёд, "
                "удлиняя позвоночник."
            ),
            "seconds": 40,
            "level": 3,
        },

        {
            "text": (
                "Встань и сцепи руки перед собой. "
                "Мягко округли верхнюю часть спины, "
                "выталкивая ладони вперёд."
            ),
            "seconds": 30,
            "level": 2,
        },

        {
            "text": (
                "Теперь сцепи руки за спиной. "
                "Осторожно отведи плечи назад и раскрой грудную клетку."
            ),
            "seconds": 30,
            "level": 3,
        },

        {
            "text": (
                "Стоя медленно наклони корпус вперёд. "
                "Полностью расслабь шею, плечи и руки."
            ),
            "seconds": 40,
            "level": 3,
        },

        {
            "text": (
                "Медленно выпрямись. "
                "Сделай глубокий вдох и расслабь плечи."
            ),
            "seconds": 25,
            "level": 3,
        },
    ],


    # ==================================================
    # ПЛЕЧИ И РУКИ
    # ==================================================

    "💪 Плечи и руки": [

        {
            "text": (
                "Выпрями правую руку перед собой "
                "и прижми её к груди."
            ),
            "seconds": 30,
            "level": 1,
        },

        {
            "text": (
                "Теперь поменяй руку."
            ),
            "seconds": 30,
            "level": 1,
        },

        {
            "text": (
                "Подними правую руку вверх, согни локоть "
                "и опусти ладонь за спину."
            ),
            "seconds": 30,
            "level": 1,
        },

        {
            "text": (
                "Поменяй руку и растяни левый трицепс."
            ),
            "seconds": 30,
            "level": 1,
        },

        {
            "text": (
                "Вытяни правую руку перед собой ладонью вверх. "
                "Другой рукой осторожно направь пальцы вниз."
            ),
            "seconds": 25,
            "level": 1,
        },

        {
            "text": (
                "Поменяй руку и мягко растяни предплечье."
            ),
            "seconds": 25,
            "level": 2,
        },

        {
            "text": (
                "Вытяни правую руку ладонью вниз "
                "и осторожно потяни пальцы на себя."
            ),
            "seconds": 25,
            "level": 2,
        },

        {
            "text": (
                "Теперь повтори растяжение другой рукой."
            ),
            "seconds": 25,
            "level": 2,
        },

        {
            "text": (
                "Соедини руки за спиной и осторожно "
                "отведи их назад."
            ),
            "seconds": 35,
            "level": 2,
        },

        {
            "text": (
                "Сцепи пальцы перед собой, разверни ладони наружу "
                "и потяни руки вперёд."
            ),
            "seconds": 30,
            "level": 3,
        },

        {
            "text": (
                "Подними сцепленные руки над головой "
                "и мягко потянись вверх."
            ),
            "seconds": 30,
            "level": 3,
        },

        {
            "text": (
                "Опусти руки и сделай несколько "
                "медленных круговых движений плечами назад."
            ),
            "seconds": 25,
            "level": 3,
        },

        {
            "text": (
                "Теперь сделай спокойные круговые движения "
                "плечами вперёд."
            ),
            "seconds": 25,
            "level": 2,
        },

        {
            "text": (
                "Расслабь руки и слегка встряхни кисти. "
                "Плечи полностью расслаблены."
            ),
            "seconds": 25,
            "level": 3,
        },
    ],


    # ==================================================
    # ПОСЛЕ ТРЕНИРОВКИ
    # ==================================================

    "🏋️ После тренировки": [

        {
            "text": (
                "Начинаем восстановительную растяжку. "
                "Выпрями правую руку и мягко прижми её к груди."
            ),
            "seconds": 30,
            "level": 1,
        },

        {
            "text": "Поменяй руку и расслабь плечо.",
            "seconds": 30,
            "level": 1,
        },

        {
            "text": (
                "Подними правую руку и согни её за головой. "
                "Мягко растяни трицепс."
            ),
            "seconds": 30,
            "level": 1,
        },

        {
            "text": "Теперь поменяй руку.",
            "seconds": 30,
            "level": 1,
        },

        {
            "text": (
                "Соедини руки за спиной и мягко раскрой грудную клетку."
            ),
            "seconds": 35,
            "level": 1,
        },

        {
            "text": (
                "Поставь ноги на ширине плеч "
                "и плавно наклонись вперёд."
            ),
            "seconds": 40,
            "level": 1,
        },

        {
            "text": (
                "Согни правую ногу и подтяни стопу к ягодице."
            ),
            "seconds": 30,
            "level": 2,
        },

        {
            "text": "Теперь поменяй ногу.",
            "seconds": 30,
            "level": 2,
        },

        {
            "text": (
                "Сделай выпад правой ногой вперёд "
                "и мягко растяни сгибатели бедра."
            ),
            "seconds": 35,
            "level": 2,
        },

        {
            "text": "Поменяй стороны.",
            "seconds": 35,
            "level": 1,
        },

        {
            "text": (
                "Сядь на пол, выпрями ноги "
                "и медленно наклонись вперёд."
            ),
            "seconds": 40,
            "level": 1,
        },

        {
            "text": (
                "Соедини стопы и мягко разведи колени в стороны."
            ),
            "seconds": 40,
            "level": 1,
        },

        {
            "text": (
                "Перейди на четвереньки и медленно округли спину."
            ),
            "seconds": 30,
            "level": 3,
        },

        {
            "text": (
                "Отведи таз назад к пяткам "
                "и расслабь позвоночник."
            ),
            "seconds": 45,
            "level": 3,
        },

        {
            "text": (
                "Ляг на спину и подтяни колени к груди. "
                "Спокойно дыши."
            ),
            "seconds": 40,
            "level": 3,
        },
    ],
    
}


def build_stretching_script(goal: str, duration: int, level: str):
    exercises = STRETCHING_EXERCISES.get(
        goal,
        STRETCHING_EXERCISES["🧘 Всё тело"],
    )

    # Оставляем часть времени на голосовые инструкции.
# Примерно 25% аудио занимает голос,
# остальное — выполнение упражнений.

    target_seconds = int(
        duration * 60 * 0.72
    )

    script = []
    current_seconds = 0

    # Для более продвинутого уровня немного увеличиваем удержание.
    level_multiplier = {
        "🌱 Новичок": 0.8,
        "💪 Средний": 1.0,
        "🔥 Продвинутый": 1.2,
    }.get(level, 1.0)

    available_exercises = exercises.copy()
    random.shuffle(available_exercises)

    exercise_index = 0

    while current_seconds < target_seconds:

        # Если прошли весь список,
        # перемешиваем упражнения заново.
        if exercise_index >= len(available_exercises):
            available_exercises = exercises.copy()
            random.shuffle(available_exercises)
            exercise_index = 0

        exercise = available_exercises[exercise_index]
        exercise_index += 1

        seconds = int(
            exercise["seconds"] * level_multiplier
        )

        seconds = max(seconds, 20)

        # Не выходим слишком сильно
        # за необходимую длительность.
        remaining_seconds = (
            target_seconds - current_seconds
        )

        if seconds > remaining_seconds:
            seconds = remaining_seconds

        # Последнее удержание не делаем
        # бессмысленно коротким.
        if seconds < 15:
            break

        script.append(
            {
                "text": exercise["text"],
                "seconds": seconds,
            }
        )

        current_seconds += seconds

    return script

def build_stretching_script(
    goal: str,
    duration: int,
    level: str,
):
    """
    Создаёт программу растяжки с учётом:
    - цели;
    - продолжительности;
    - уровня пользователя.
    """

    exercises = STRETCHING_EXERCISES.get(
        goal,
        STRETCHING_EXERCISES["🧘 Всё тело"],
    )

    # --------------------------------
    # Уровень пользователя
    # --------------------------------

    level_numbers = {
        "🌱 Новичок": 1,
        "💪 Средний": 2,
        "🔥 Продвинутый": 3,
    }

    user_level = level_numbers.get(
        level,
        1,
    )

    # --------------------------------
    # Фильтруем упражнения
    # --------------------------------

    if user_level == 1:

        # Новичку только простые
        allowed_exercises = [
            exercise
            for exercise in exercises
            if exercise.get("level", 1) == 1
        ]

    elif user_level == 2:

        # Среднему простые + средние
        allowed_exercises = [
            exercise
            for exercise in exercises
            if exercise.get("level", 1) <= 2
        ]

    else:

        # Продвинутому доступны все
        allowed_exercises = exercises.copy()

    # Защита на случай ошибки в базе
    if not allowed_exercises:
        allowed_exercises = exercises.copy()

    # --------------------------------
    # Время удержания
    # --------------------------------

    if user_level == 1:
        min_seconds = 20
        max_seconds = 30

    elif user_level == 2:
        min_seconds = 30
        max_seconds = 45

    else:
        min_seconds = 40
        max_seconds = 60

    # Часть общего времени оставляем
    # под голосовые инструкции.
    target_seconds = int(
        duration * 60 * 0.72
    )

    script = []
    current_seconds = 0

    # Перемешиваем один раз
    available_exercises = (
        allowed_exercises.copy()
    )

    random.shuffle(
        available_exercises
    )

    exercise_index = 0

    # --------------------------------
    # Собираем тренировку
    # --------------------------------

    while current_seconds < target_seconds:

        # Если упражнения закончились,
        # начинаем новый круг.
        if exercise_index >= len(
            available_exercises
        ):
            available_exercises = (
                allowed_exercises.copy()
            )

            random.shuffle(
                available_exercises
            )

            exercise_index = 0

        exercise = (
            available_exercises[
                exercise_index
            ]
        )

        exercise_index += 1

        base_seconds = exercise.get(
            "seconds",
            30,
        )

        # Ограничиваем время согласно уровню
        seconds = max(
            min_seconds,
            min(
                base_seconds,
                max_seconds,
            ),
        )

        remaining_seconds = (
            target_seconds
            - current_seconds
        )

        if remaining_seconds < 15:
            break

        if seconds > remaining_seconds:
            seconds = remaining_seconds

        script.append(
            {
                "text": exercise["text"],
                "seconds": seconds,
                "level": exercise.get(
                    "level",
                    1,
                ),
            }
        )

        current_seconds += seconds

    print(
        f"Уровень: {level} | "
        f"Упражнений: {len(script)} | "
        f"Удержания: {current_seconds} сек."
    )

    return script


def create_stretching_voice(
    user_id: int,
    script: list,
    duration: int,
    voice: str = "female",
):
    """
    Создаёт голосовые инструкции для растяжки
    и добавляет паузы для выполнения упражнений.
    """

    if voice == "male":
        openai_voice = "onyx"
    else:
        openai_voice = "shimmer"

    output_dir = (
        Path("media")
        / "stretching"
        / "generated"
        / str(user_id)
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    generated_files = []

    # -----------------------------
    # Вступление
    # -----------------------------

    intro_text = (
        "Начинаем растяжку. "
        "Выполняй все движения плавно и спокойно. "
        "Не растягивай мышцы через боль. "
        "Дыши ровно и не задерживай дыхание."
    )

    intro_path = output_dir / "intro.mp3"

    with client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice=openai_voice,
        input=intro_text,
        instructions=(
            "Speak in Russian. "
            "Sound like a calm professional stretching instructor. "
            "Speak clearly and slowly. "
            "Use a supportive fitness coach tone."
        ),
    ) as response:

        response.stream_to_file(
            intro_path
        )

    generated_files.append(
        {
            "type": "voice",
            "path": intro_path,
        }
    )

    # -----------------------------
    # Упражнения
    # -----------------------------

    for index, exercise in enumerate(script):

        text = exercise["text"]
        seconds = exercise["seconds"]

        exercise_path = (
            output_dir
            / f"exercise_{index}.mp3"
        )

        print(
            f"Создаю инструкцию "
            f"{index + 1}/{len(script)}"
        )

        with client.audio.speech.with_streaming_response.create(
            model="gpt-4o-mini-tts",
            voice=openai_voice,
            input=text,
            instructions=(
                "Speak in Russian. "
                "Sound like a professional stretching coach. "
                "Speak calmly and clearly. "
                "Explain the movement naturally. "
                "Do not rush."
            ),
        ) as response:

            response.stream_to_file(
                exercise_path
            )

        generated_files.append(
            {
                "type": "voice",
                "path": exercise_path,
            }
        )

        generated_files.append(
            {
                "type": "silence",
                "seconds": seconds,
            }
        )

    # -----------------------------
    # Завершение
    # -----------------------------

    outro_text = (
        "Растяжка завершена. "
        "Медленно расслабь мышцы. "
        "Сделай глубокий вдох и спокойный выдох. "
        "Отличная работа."
    )

    outro_path = output_dir / "outro.mp3"

    with client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice=openai_voice,
        input=outro_text,
        instructions=(
            "Speak in Russian. "
            "Use a calm and positive fitness instructor voice."
        ),
    ) as response:

        response.stream_to_file(
            outro_path
        )

    generated_files.append(
        {
            "type": "voice",
            "path": outro_path,
        }
    )

    # -----------------------------
    # Создаём тишину
    # -----------------------------

    silence_dir = (
        Path("media")
        / "stretching"
        / "silence"
    )

    silence_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    for item in generated_files:

        if item["type"] != "silence":
            continue

        seconds = item["seconds"]

        silence_path = (
            silence_dir
            / f"silence_{seconds}.mp3"
        )

        if not silence_path.exists():

            command = [
                "ffmpeg",
                "-y",
                "-f",
                "lavfi",
                "-i",
                "anullsrc=r=24000:cl=mono",
                "-t",
                str(seconds),
                "-c:a",
                "libmp3lame",
                "-b:a",
                "128k",
                str(silence_path),
            ]

            subprocess.run(
                command,
                check=True,
            )

        item["path"] = silence_path

    # -----------------------------
    # Создаём concat-файл
    # -----------------------------

    concat_file = (
        output_dir
        / "concat.txt"
    )

    with open(
        concat_file,
        "w",
        encoding="utf-8",
    ) as file:

        for item in generated_files:

            path = item["path"].resolve()

            file.write(
                f"file '{path}'\n"
            )

    # -----------------------------
    # Склеиваем голос и паузы
    # -----------------------------

    voice_output = (
        output_dir
        / "stretching_voice.mp3"
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
        str(voice_output),
    ]

    subprocess.run(
        command,
        check=True,
    )

    return str(voice_output)
    
def mix_stretching_audio(
    voice_path: str,
    user_id: int,
    duration: int,
) -> str:
    """
    Накладывает фоновую музыку на голосовую тренировку.
    Музыка играет постоянно, в том числе во время пауз.
    """

    output_dir = (
        Path("media")
        / "stretching"
        / "generated"
        / str(user_id)
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    music_dir = (
        Path("media")
        / "stretching"
        / "music"
    )

    music_files = list(
        music_dir.glob("*.mp3")
    )

    if not music_files:
        raise FileNotFoundError(
            f"В папке нет MP3 музыки: {music_dir}"
        )

    # Случайно выбираем одну мелодию
    music_path = random.choice(
        music_files
    )

    print(
        f"🎵 Музыка для растяжки: {music_path}"
    )

    output_path = (
        output_dir
        / "stretching_final.mp3"
    )

    target_seconds = duration * 60

    command = [
        "ffmpeg",
        "-y",

        # Голос + паузы
        "-i",
        str(voice_path),

        # Музыку зацикливаем
        "-stream_loop",
        "-1",
        "-i",
        str(music_path),

        "-filter_complex",
        (
            "[0:a]volume=1.0[voice];"
            "[1:a]volume=0.12[music];"
            "[voice][music]"
            "amix=inputs=2:duration=first:"
            "dropout_transition=2[a]"
        ),

        "-map",
        "[a]",

        # Максимальная длительность
        "-t",
        str(target_seconds),

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

    return str(output_path)