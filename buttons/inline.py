from aiogram.utils.keyboard import InlineKeyboardBuilder


def items_inline(data: list):
    markup = InlineKeyboardBuilder()
    for item in data:
        markup.button(text=f"{item['name']} / {item['name_ru']}",
                      callback_data=f"{item['id']}:{item['name']} / {item['name_ru']} ")
    markup.adjust(1, repeat=True)
    return markup.as_markup()
