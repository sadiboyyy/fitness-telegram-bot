from datetime import datetime

from aiogram import F, Router
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
)

from database import conn, cursor
from keyboards.menu import main_menu


router = Router()


subscription_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="👤 Пользователь — $10/месяц")],
        [KeyboardButton(text="🏢 Бизнес — $50/месяц")],
        [KeyboardButton(text="📋 Что входит в подписку")],
        [KeyboardButton(text="👤 Моя подписка")],
        [KeyboardButton(text="🏠 Главное меню")],
    ],
    resize_keyboard=True,
)
def register_user(message: Message) -> None:
    user = message.from_user

    cursor.execute(
        """
        INSERT OR IGNORE INTO users (
            user_id,
            username,
            first_name,
            registered_at,
            subscription_type,
            subscription_until
        )
        VALUES (?, ?, ?, ?, 'free', NULL)
        """,
        (
            user.id,
            user.username,
            user.first_name,
            datetime.now().strftime("%d.%m.%Y %H:%M"),
        ),
    )

    cursor.execute(
        """
        UPDATE users
        SET username = ?, first_name = ?
        WHERE user_id = ?
        """,
        (
            user.username,
            user.first_name,
            user.id,
        ),
    )

    cursor.execute(
        """
        INSERT OR IGNORE INTO fitcoins (
            user_id,
            balance
        )
        VALUES (?, 0)
        """,
        (user.id,),
    )

    cursor.execute(
        """
        INSERT OR IGNORE INTO workout_streaks (
            user_id,
            current_streak,
            best_streak,
            total_workouts
        )
        VALUES (?, 0, 0, 0)
        """,
        (user.id,),
    )

    conn.commit()

def is_premium(user_id: int) -> bool:

    cursor.execute(
        """
        SELECT
            subscription_type,
            subscription_until
        FROM users
        WHERE user_id = ?
        """,
        (user_id,),
    )

    result = cursor.fetchone()

    if result is None:
        return False

    subscription_type, subscription_until = result

    if subscription_type != "premium":
        return False

    try:
        expires = datetime.strptime(
            subscription_until,
            "%d.%m.%Y",
        )

        if expires >= datetime.now():
            return True

    except Exception:
        return False

    cursor.execute(
        """
        UPDATE users
        SET subscription_type='free'
        WHERE user_id=?
        """,
        (user_id,),
    )

    conn.commit()

    return False   

from datetime import datetime, timedelta


def activate_premium(user_id: int, days: int):
    expires = (
        datetime.now() + timedelta(days=days)
    ).strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        """
        UPDATE users
        SET
            subscription_type = 'user',
            subscription_until = ?,
            payment_status = 'paid'
        WHERE user_id = ?
        """,
        (
            expires,
            user_id,
        ),
    )

    conn.commit()


def activate_business_plan(user_id: int, days: int = 30):
    expires = (
        datetime.now() + timedelta(days=days)
    ).strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        """
        UPDATE users
        SET
            subscription_type = 'business',
            subscription_until = ?,
            payment_status = 'paid'
        WHERE user_id = ?
        """,
        (
            expires,
            user_id,
        ),
    )

    conn.commit()

@router.message(F.text == "🛠 Активировать Premium (тест)")
async def activate_test(
    message: Message,
):

    activate_premium(
        message.from_user.id,
        30,
    )

    await message.answer(
        "🎉 Premium успешно активирован!\n\n"
        "📅 Срок действия: 30 дней.\n\n"
        "Теперь вам доступны все Premium-функции.",
        reply_markup=subscription_keyboard,
    ) 



@router.message(F.text == "💎 Подписка")
async def premium_page(message: Message):

    register_user(message)

    await message.answer(
        "💎 <b>FITNESS AI — ТАРИФЫ</b>\n\n"
        "👤 <b>Обычный пользователь:</b> $10 / месяц\n"
        "🏢 <b>Бизнес-аккаунт:</b> $50 / месяц\n\n"
        "✅ Пользователь получает доступ ко всем функциям для клиента\n"
        "✅ Бизнес получает доступ к управлению и аренде бота\n\n"
        "Выберите план ниже:",
        parse_mode="HTML",
        reply_markup=subscription_keyboard,
    )


@router.message(F.text == "👤 Пользователь — $10/месяц")
async def buy_user_subscription(message: Message):
    register_user(message)

    cursor.execute(
        """
        UPDATE users
        SET subscription_type = 'user',
            subscription_until = ?,
            payment_status = 'paid'
        WHERE user_id = ?
        """,
        ((datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S"), message.from_user.id),
    )
    conn.commit()

    await message.answer(
        "✅ <b>План пользователя активирован</b>\n\n"
        "💵 Стоимость: <b>$10/месяц</b>\n"
        "📅 Срок: <b>30 дней</b>\n\n"
        "Доступ к боту открыт.",
        parse_mode="HTML",
        reply_markup=subscription_keyboard,
    )


@router.message(F.text == "🏢 Бизнес — $50/месяц")
async def buy_business_subscription(message: Message):
    register_user(message)

    cursor.execute(
        """
        UPDATE users
        SET subscription_type = 'business',
            subscription_until = ?,
            payment_status = 'paid'
        WHERE user_id = ?
        """,
        ((datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S"), message.from_user.id),
    )
    conn.commit()

    await message.answer(
        "✅ <b>Бизнес-план активирован</b>\n\n"
        "💵 Стоимость: <b>$50/месяц</b>\n"
        "📅 Срок: <b>30 дней</b>\n\n"
        "Для бизнеса доступ к админскому управлению и аренде бота открыт.",
        parse_mode="HTML",
        reply_markup=subscription_keyboard,
    )


@router.message(F.text == "📋 Что входит в подписку")
async def show_subscription_features(message: Message):
    await message.answer(
        "📋 <b>Что входит в подписку</b>\n\n"
        "👤 Пользователь: доступ к основному функционалу\n"
        "🏢 Бизнес: доступ к управлению ботом, подписками, рассылкой и клиентской работе\n\n"
        "💳 Оплата проверяется автоматически по сроку подписки\n"
        "⚠️ После просрочки доступ к боту будет закрыт\n"
        "🔔 За 3 дня до конца подписки бот присылает напоминание.",
        parse_mode="HTML",
        reply_markup=subscription_keyboard,
    )


@router.message(F.text == "👤 Моя подписка")
async def my_subscription(message: Message):
    register_user(message)
    cursor.execute(
        "SELECT subscription_type, subscription_until, payment_status FROM users WHERE user_id = ?",
        (message.from_user.id,),
    )
    row = cursor.fetchone()

    if not row:
        await message.answer("Подписка не найдена", reply_markup=subscription_keyboard)
        return

    plan, expires_at, payment_status = row
    if plan == "free":
        status = "❌ Нет активной подписки"
    elif payment_status == "paid" and expires_at:
        status = f"✅ Активна: {plan} до {expires_at}"
    else:
        status = "❌ Подписка просрочена"

    await message.answer(
        f"👤 <b>Моя подписка</b>\n\n{status}",
        parse_mode="HTML",
        reply_markup=subscription_keyboard,
    )


@router.message(F.text == "🆓 Бесплатный тариф")
async def show_free_plan(message: Message):
    register_user(message)

    await message.answer(
        "🆓 <b>Fitness AI Free — $0</b>\n\n"
        "В бесплатный тариф входит:\n\n"
        "✅ базовая программа тренировок;\n"
        "✅ расчёт нормы калорий;\n"
        "✅ сохранение замеров;\n"
        "✅ история прогресса;\n"
        "✅ напоминания о тренировках;\n"
        "✅ ежедневные задания;\n"
        "✅ FitCoins за активность;\n"
        "✅ до 5 текстовых вопросов ИИ в день;\n"
        "✅ до 3 голосовых вопросов в день.\n\n"
        "Некоторые продвинутые функции будут доступны "
        "только в Premium.",
        parse_mode="HTML",
        reply_markup=subscription_keyboard,
    )

@router.message(F.text == "📋 Что входит в Premium")
async def premium_features(message: Message):

    await message.answer(

        "💎 <b>Premium открывает:</b>\n\n"

        "🤖 Безлимитные вопросы ИИ\n"

        "🎙 Голосовой AI-тренер\n"

        "📸 Анализ тела\n"

        "🍽 Анализ еды по фотографии\n"

        "🏋 Проверка техники упражнений\n"

        "📈 Красивые графики прогресса\n"

        "📷 Фото До / После\n"

        "🧘 Медитации\n"

        "🤸 Растяжка\n"

        "🔥 Серии тренировок\n"

        "🎯 Ежедневные задания\n"

        "🪙 Удвоенные FitCoins\n"

        "📅 Календарь тренировок\n"

        "🎵 Музыка для восстановления",

        parse_mode="HTML",
        reply_markup=subscription_keyboard,
    )

@router.message(F.text == "💎 Premium — $9.99/месяц")
async def show_premium_plan(message: Message):
    register_user(message)

    await message.answer(
        "💎 <b>Fitness AI Premium</b>\n\n"
        "💵 Стоимость: <b>$9.99 в месяц</b>\n\n"
        "В Premium входит:\n\n"
        "♾ расширенный доступ к ИИ;\n"
        "🎙 голосовой фитнес-ассистент;\n"
        "🥗 персональные планы питания;\n"
        "📸 анализ еды по фотографии;\n"
        "🏋️ анализ техники упражнений;\n"
        "📈 графики и автоматический анализ прогресса;\n"
        "📷 хранение и сравнение фото «до/после»;\n"
        "📅 календарь тренировок;\n"
        "🔥 серии тренировок;\n"
        "🏆 достижения и награды;\n"
        "🪙 больше способов получать FitCoins;\n"
       "🧘 Медитации\n"
        "🤸 Растяжка\n"
        "🎵 Музыка для восстановления",
        "🎯 Ежедневные задания\n",
        parse_mode="HTML",
        reply_markup=subscription_keyboard,
    )

@router.message(F.text == "💎 Купить на год")
async def buy_year(message: Message):

    await message.answer(

        "💰 Premium на год\n\n"

        "Стоимость:\n"

        "$79.99\n\n"

        "Вы экономите около 33% по сравнению с ежемесячной оплатой.\n\n",

        reply_markup=subscription_keyboard,
    )

@router.message(F.text == "👤 Моя подписка")
async def show_my_subscription(message: Message):
    register_user(message)

    cursor.execute(
        """
        SELECT
            subscription_type,
            subscription_until
        FROM users
        WHERE user_id = ?
        """,
        (message.from_user.id,),
    )

    result = cursor.fetchone()

    if result is None:
        await message.answer(
            "❌ Не удалось получить информацию о подписке."
        )
        return

    subscription_type, subscription_until = result

    if subscription_type == "premium":
        until_text = subscription_until or "не указана"

        await message.answer(
            "💎 <b>Ваша подписка: Premium</b>\n\n"
            f"📅 Активна до: {until_text}",
            parse_mode="HTML",
            reply_markup=subscription_keyboard,
        )
    else:
        await message.answer(
            "🆓 <b>Ваша подписка: Free</b>\n\n"
            "Для доступа ко всем функциям можно перейти "
            "на Premium за $9.99 в месяц.",
            parse_mode="HTML",
            reply_markup=subscription_keyboard,
        )
async def premium_required(message: Message):
    await message.answer(
        "🔒 <b>Эта функция доступна только в Premium</b>\n\n"

        "Получите полный доступ к Fitness AI:\n\n"

        "🤖 Безлимитный AI\n"
        "🍽 Анализ еды по фото\n"
        "📷 Фото До / После\n"
        "📈 Красивые графики\n"
        "🎙 Голосовой тренер\n"
        "🧘 Медитации\n"
        "🤸 Растяжка\n"
        "🪙 Удвоенные FitCoins\n"
        "📅 Календарь тренировок\n"
        "🏆 Достижения\n\n"

        "💵 Стоимость:\n"
        "<b>$9.99 / месяц</b>\n"
        "<b>$79.99 / год</b>",

        parse_mode="HTML",
        reply_markup=subscription_keyboard,
    )

@router.message(F.text == "🏠 Главное меню")
async def subscription_main_menu(message: Message):
    await message.answer(
        "🏠 Вы вернулись в главное меню.",
        reply_markup=main_menu,
    )
