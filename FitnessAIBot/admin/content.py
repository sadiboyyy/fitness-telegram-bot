@router.message(F.text == "🏋️ Контент")
async def admin_content(message: Message):

    if not is_admin(message):
        return

    await message.answer(
        "🏋️ <b>КОНТЕНТ</b>\n\n"
        "💪 Программы тренировок\n"
        "🍽 Питание\n"
        "🧘 Медитации\n"
        "🤸 Растяжка\n"
        "🏆 Достижения\n"
        "📚 Фитнес-факты\n"
        "🔔 Уведомления\n\n"
        "Позже сможем дать владельцу возможность менять контент без изменения кода.",
        parse_mode="HTML",
        reply_markup=admin_menu,
    )