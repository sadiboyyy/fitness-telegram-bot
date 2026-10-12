@router.message(F.text == "🏠 Главное меню")
async def main_menu_handler(
    message: Message,
    state: FSMContext,
):
    await state.clear()

    await message.answer(
        "🏠 Вы вернулись в главное меню.",
        reply_markup=main_menu,
    )