from aiogram import Router, types, F
from keyboards import main_menu
from models import get_user_card, save_user_card

router = Router()

@router.message(F.text == "/start")
async def cmd_start(message: types.Message):
    user_card = get_user_card(message.from_user.id)
    if not user_card:
        await message.answer("Пожалуйста, укажите номер вашей банковской карты, куда будут перечисляться деньги за продажу звёзд:")
    else:
        await message.answer(
            "Привет! Используй кнопки меню для работы с ботом.",
            reply_markup=main_menu()
        )

@router.message(F.text.regexp(r"^\d{16,19}$"))
async def handle_card(message: types.Message):
    user_card = get_user_card(message.from_user.id)
    if not user_card:
        save_user_card(message.from_user.id, message.text)
        await message.answer("Карта успешно сохранена! Теперь вы можете пользоваться ботом.", reply_markup=main_menu())