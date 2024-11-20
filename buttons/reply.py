from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📝Feedback qoldirish")
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
            KeyboardButton(text='Ha'),
        ],
        [
            KeyboardButton(text='/new'),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Kerakli bo\'limni tanlang'
)

feedback_verify = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Tasdiqlash'),
        ],
        [
            KeyboardButton(text='/new'),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Kerakli bo\'limni tanlang'
)
