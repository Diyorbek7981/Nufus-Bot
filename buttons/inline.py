from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

gender = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='👱🏻‍♂️Erkak', callback_data='Erkak'),
            InlineKeyboardButton(text='👩Ayol', callback_data='Ayol'),
        ]
    ], resize_keyboard=True
)


def items_inline(data: list):
    markup = InlineKeyboardBuilder()
    for item in data:
        markup.button(text=f"{item['name']} / {item['name_ru']}",
                      callback_data=f"{item['id']}:{item['name']} / {item['name_ru']} ")
    markup.adjust(3, repeat=True)
    return markup.as_markup()
