from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📝 Fikr qoldirish / Оставить комментарий")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Kerakli bo\'limni tanlang'
)

phone = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Contact ulashish', request_contact=True),
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Contact ulashish tugmasi orqali'
)

check = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Yes'),
        ],
        [
            KeyboardButton(text='/new'),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Kerakli bo\'limni tanlang'
)
