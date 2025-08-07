from aiogram import Router, types, F
from models import get_user, add_balance, get_user_transactions
from keyboards import wallet_menu, deposit_methods_keyboard, withdraw_methods_keyboard
from messages import (
    wallet_main, deposit_choose_method, withdraw_choose_method,
    deposit_success, withdraw_success, not_enough_funds,
    history_title, transaction_line
)

router = Router()

@router.message(F.text == "Кошелёк")
async def wallet_entry(message: types.Message):
    user = get_user(message.from_user.id)
    await message.answer(wallet_main(user["balance"]), reply_markup=wallet_menu())

@router.message(F.text == "Пополнить баланс")
async def wallet_deposit(message: types.Message):
    await message.answer(deposit_choose_method(), reply_markup=deposit_methods_keyboard())

@router.callback_query(F.data.startswith("deposit_"))
async def deposit_method_chosen(callback_query: types.CallbackQuery):
    tx = add_balance(callback_query.from_user.id, 1000.0, "deposit", "Тестовое пополнение")
    await callback_query.message.answer(deposit_success(tx["amount"]))

@router.message(F.text == "Вывести средства")
async def wallet_withdraw(message: types.Message):
    await message.answer(withdraw_choose_method(), reply_markup=withdraw_methods_keyboard())

@router.callback_query(F.data.startswith("withdraw_"))
async def withdraw_method_chosen(callback_query: types.CallbackQuery):
    user = get_user(callback_query.from_user.id)
    if user["balance"] < 100:
        await callback_query.message.answer(not_enough_funds())
    else:
        tx = add_balance(callback_query.from_user.id, -100.0, "withdraw", "Тестовый вывод")
        await callback_query.message.answer(withdraw_success(-tx["amount"]))

@router.message(F.text == "История операций")
async def wallet_history(message: types.Message):
    txs = get_user_transactions(message.from_user.id, limit=10)
    if not txs:
        await message.answer("Нет операций.")
    else:
        text = history_title() + "\n" + "\n".join([transaction_line(tx) for tx in txs])
        await message.answer(text)