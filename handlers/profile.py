from aiogram import Router, types, F
from models import get_user_profile
from keyboards import profile_menu
from messages import profile_message

router = Router()

@router.message(F.text == "Профиль")
async def profile_entry(message: types.Message):
    profile = get_user_profile(message.from_user.id)
    await message.answer(profile_message(profile), reply_markup=profile_menu())