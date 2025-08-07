from aiogram import Router, types

router = Router()

@router.message()
async def fallback(message: types.Message):
    await message.answer("Я не понимаю это сообщение. Используй команды или кнопки меню.")