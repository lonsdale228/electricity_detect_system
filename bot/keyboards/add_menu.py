from aiogram import types

kb = [
    [types.KeyboardButton(text="🔙Повернутися")],
]
keyboard_back = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)


kb_main = [
    [types.KeyboardButton(text="💡Статус світла")]
]
keyboard_main = types.ReplyKeyboardMarkup(keyboard=kb_main, resize_keyboard=True)