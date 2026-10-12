from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
)

from database import (
    PROMO_CODE_YURA_BOND,
    activate_subscription,
    get_subscription_status,
)

router = Router()

PLAN_PRICES = {
    "user": 10.0,
    "business": 50.0,
}

PLAN_LABELS = {
    "user": "Пользователь",
    "business": "Бизнес",
}

plan_selection_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="👤 Пользователь — $10/месяц")],
        [KeyboardButton(text="🏢 Бизнес — $50/месяц")],
        [KeyboardButton(text="🎟 Ввести промокод")],
        [KeyboardButton(text="⬅ Назад")],
    ],
    resize_keyboard=True,
)

payment_method_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💳 Банковская карта"), KeyboardButton(text="₿ USDT")],
        [KeyboardButton(text="⭐ Telegram Stars")],
        [KeyboardButton(text="✅ Я оплатил")],
        [KeyboardButton(text="🎟 Yura Bond")],
        [KeyboardButton(text="⬅ Назад")],
    ],
    resize_keyboard=True,
)


class PaymentForm(StatesGroup):
    choosing_plan = State()
    waiting_promo = State()
    waiting_payment_method = State()


@router.message(F.text.in_({"💳 Купить на месяц", "💰 Подписка", "💳 Оплата", "💎 Подписка"}))
async def start_payment(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(PaymentForm.choosing_plan)
    await message.answer(
        "💳 <b>Выберите тариф</b>\n\n"
        "👤 Пользователь — <b>$10/месяц</b>\n"
        "🏢 Бизнес — <b>$50/месяц</b>\n\n"
        f"🎟 Промокод: <b>{PROMO_CODE_YURA_BOND}</b> — 50% скидка на первый месяц",
        parse_mode="HTML",
        reply_markup=plan_selection_keyboard,
    )


@router.message(F.text == "🎟 Ввести промокод", PaymentForm.choosing_plan)
async def enter_promo(message: Message, state: FSMContext):
    await state.set_state(PaymentForm.waiting_promo)
    await message.answer(
        "🎟 Введите промокод:\n\n"
        f"<b>{PROMO_CODE_YURA_BOND}</b>\n\n"
        "Скидка 50% применяется только на первый месяц и только для данного пользователя.",
        parse_mode="HTML",
    )


@router.message(F.text, PaymentForm.waiting_promo)
async def apply_promo(message: Message, state: FSMContext):
    promo_text = (message.text or "").strip()
    if promo_text.lower() != PROMO_CODE_YURA_BOND.lower():
        await message.answer(
            "❌ Промокод не найден или не подходит для вашего аккаунта.\n\n"
            f"Попробуйте: <b>{PROMO_CODE_YURA_BOND}</b>",
            parse_mode="HTML",
        )
        return

    await state.update_data(promo_code=PROMO_CODE_YURA_BOND)
    await state.set_state(PaymentForm.waiting_payment_method)
    await message.answer(
        "✅ Промокод применён. Скидка 50% активна на первый месяц.\n\n"
        "Теперь выберите способ оплаты:",
        parse_mode="HTML",
        reply_markup=payment_method_keyboard,
    )


@router.message(F.text == "👤 Пользователь — $10/месяц", PaymentForm.choosing_plan)
async def select_user_plan(message: Message, state: FSMContext):
    await state.update_data(plan="user")
    await state.set_state(PaymentForm.waiting_payment_method)
    await message.answer(
        "✅ Вы выбрали <b>Пользовательский тариф</b>\n\n"
        "Стоимость: <b>$10/месяц</b>\n"
        "Срок: <b>30 дней</b>\n\n"
        "Если у вас есть промокод, напишите: <b>Yura Bond</b>\n\n"
        "Или выберите способ оплаты:",
        parse_mode="HTML",
        reply_markup=payment_method_keyboard,
    )


@router.message(F.text == "🏢 Бизнес — $50/месяц", PaymentForm.choosing_plan)
async def select_business_plan(message: Message, state: FSMContext):
    await state.update_data(plan="business")
    await state.set_state(PaymentForm.waiting_payment_method)
    await message.answer(
        "✅ Вы выбрали <b>Бизнес-тариф</b>\n\n"
        "Стоимость: <b>$50/месяц</b>\n"
        "Срок: <b>30 дней</b>\n\n"
        "Если у вас есть промокод, напишите: <b>Yura Bond</b>\n\n"
        "Или выберите способ оплаты:",
        parse_mode="HTML",
        reply_markup=payment_method_keyboard,
    )


@router.message(F.text == "💳 Банковская карта", PaymentForm.waiting_payment_method)
async def select_card_payment(message: Message, state: FSMContext):
    data = await state.get_data()
    plan = data.get("plan")
    if not plan:
        await message.answer("Сначала выберите тариф.", reply_markup=plan_selection_keyboard)
        return

    price = PLAN_PRICES[plan]
    if data.get("promo_code"):
        price = round(price * 0.5, 2)

    await state.update_data(payment_method="card")
    await message.answer(
        "💳 <b>Оплата картой</b>\n\n"
        "Получатель: <b>Fitness AI</b>\n"
        f"Сумма: <b>${price}</b>\n"
        "Реквизиты: <code>1234 5678 9012 3456</code>\n\n"
        "После перевода нажмите <b>✅ Я оплатил</b>.",
        parse_mode="HTML",
        reply_markup=payment_method_keyboard,
    )


@router.message(F.text == "₿ USDT", PaymentForm.waiting_payment_method)
async def select_usdt_payment(message: Message, state: FSMContext):
    data = await state.get_data()
    plan = data.get("plan")
    if not plan:
        await message.answer("Сначала выберите тариф.", reply_markup=plan_selection_keyboard)
        return

    price = PLAN_PRICES[plan]
    if data.get("promo_code"):
        price = round(price * 0.5, 2)

    await state.update_data(payment_method="usdt")
    await message.answer(
        "₿ <b>Оплата USDT</b>\n\n"
        "Сеть: <b>TRC20</b>\n"
        f"Сумма: <b>${price}</b>\n"
        "Адрес: <code>TXL7A4r...Q9u2</code>\n\n"
        "После оплаты нажмите <b>✅ Я оплатил</b>.",
        parse_mode="HTML",
        reply_markup=payment_method_keyboard,
    )


@router.message(F.text == "⭐ Telegram Stars", PaymentForm.waiting_payment_method)
async def select_stars_payment(message: Message, state: FSMContext):
    data = await state.get_data()
    plan = data.get("plan")
    if not plan:
        await message.answer("Сначала выберите тариф.", reply_markup=plan_selection_keyboard)
        return

    price = PLAN_PRICES[plan]
    if data.get("promo_code"):
        price = round(price * 0.5, 2)

    await state.update_data(payment_method="stars")
    await message.answer(
        "⭐ <b>Оплата через Telegram Stars</b>\n\n"
        f"Сумма: <b>${price}</b>\n"
        "Нажмите кнопку оплаты в Telegram и после этого подтвердите платёж.",
        parse_mode="HTML",
        reply_markup=payment_method_keyboard,
    )


@router.message(F.text == "🎟 Yura Bond", PaymentForm.waiting_payment_method)
async def promo_shortcut(message: Message, state: FSMContext):
    await state.update_data(promo_code=PROMO_CODE_YURA_BOND)
    await message.answer(
        "✅ Промокод <b>Yura Bond</b> применён. Скидка 50% активна на первый месяц.",
        parse_mode="HTML",
    )


@router.message(F.text == "✅ Я оплатил", PaymentForm.waiting_payment_method)
async def confirm_payment(message: Message, state: FSMContext):
    data = await state.get_data()
    plan = data.get("plan")
    payment_method = data.get("payment_method", "manual")
    promo_code = data.get("promo_code")

    if not plan:
        await message.answer("Сначала выберите тариф.", reply_markup=plan_selection_keyboard)
        return

    expires_at = activate_subscription(
        message.from_user.id,
        plan,
        months=1,
        amount=PLAN_PRICES[plan],
        promo_code=promo_code,
    )
    status = get_subscription_status(message.from_user.id)

    await state.clear()
    await message.answer(
        "✅ <b>Оплата подтверждена</b>\n\n"
        f"Тариф: <b>{PLAN_LABELS[plan]}</b>\n"
        f"Метод оплаты: <b>{payment_method}</b>\n"
        f"Промокод: <b>{promo_code or 'без промокода'}</b>\n"
        f"Подписка активна до: <b>{expires_at}</b>\n\n"
        "Доступ к боту открыт.",
        parse_mode="HTML",
    )

    if status.get("active"):
        await message.answer("🎉 Подписка успешно активирована. Добро пожаловать!")


@router.message(F.text == "⬅ Назад")
async def back_from_payment(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("⬅ Вернулись в меню подписки.")