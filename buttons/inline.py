from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

gender = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='👱🏻‍♂️Erkak', callback_data='Erkak'),
            InlineKeyboardButton(text='👩Ayol', callback_data='Ayol'),
        ]
    ], resize_keyboard=True
)

rate = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='1️⃣', callback_data='1'),
            InlineKeyboardButton(text='2️⃣', callback_data='2'),
            InlineKeyboardButton(text='3️⃣', callback_data='3'),
            InlineKeyboardButton(text='4️⃣', callback_data='4'),
            InlineKeyboardButton(text='5️⃣', callback_data='5'),
        ]
    ], resize_keyboard=True
)
