from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from buttons.reply import menu, phone, check
from buttons.inline import items_inline
from states import SignupStates
from aiogram.fsm.context import FSMContext
from config import ADMIN, API
import requests
import json

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    text1 = f'👋🏻 Assalomu alaykum, {message.from_user.full_name} bizning mahsulot haqida o\'z fikringizni qoldiring'
    text2 = f'👋🏻 Здравствуйте, {message.from_user.full_name} оставьте свое мнение о нашем товаре'
    await message.answer(text1, reply_markup=menu)
    await message.answer(text2, reply_markup=menu)


@router.message(F.text == '📝 Fikr qoldirish / Оставить комментарий')
async def signup(message: Message, state: FSMContext):
    res = requests.get(url=f"{API}/users/{message.from_user.id}")
    if res.status_code == 404:
        await message.answer(f"❗ Fikr va mulohazalaringizni qoldirish uchun botda ro'yxatdan o'ting,\n\n"
                             f"❗ Зарегистрируйтесь в боте, чтобы оставить свой отзыв")
        await message.answer(f'👤 Ismingizni kiriting / Введите свое имя')
        await state.set_state(SignupStates.name)
    else:
        iteam = requests.get(url=f"{API}/items/").json()
        await message.answer(f"👕 Harid qilgan mahsulotingiz / Купленный товар",
                             reply_markup=items_inline(iteam))
        await state.set_state(SignupStates.items)


@router.message(Command("help"))
async def state_name(message: Message):
    res = requests.get(url=f"{API}/users/{ADMIN}").json()
    await message.answer(
        f"👨🏻‍💻 Yordam uchun Adminga murojaat qiling,\nОбратитесь к администратору за помощью\nhttps://t.me/{res['username']}")


@router.message(Command("stop"))
async def state_name(message: Message, state: FSMContext):
    curent = await state.get_state()
    if curent == None:
        await message.answer('🔍 To\'xtatish uchun ma\'lumot mavjud emas / Нет информации, чтобы остановить',
                             reply_markup=menu)
    else:
        await message.answer(f"❌ Jarayon bekor qilindi / Процесс отменен", reply_markup=menu)
        await state.clear()


@router.message(Command("new"))
async def state_name(message: Message, state: FSMContext):
    curent = await state.get_state()

    res = requests.get(url=f"{API}/users/{message.from_user.id}")
    iteam = requests.get(url=f"{API}/items/").json()
    if res.status_code == 404:
        if curent == None:
            await message.answer(f"❗ Fikr va mulohazalaringizni qoldirish uchun botda ro'yxatdan o'ting,\n\n"
                                 f"❗ Зарегистрируйтесь в боте, чтобы оставить свой отзыв")
            await message.answer(f'👤 Ismingizni kiriting / Введите свое имя', reply_markup=menu)
            await state.set_state(SignupStates.name)
        else:
            await state.clear()
            await message.answer(f'👤 Ismingizni kiriting / Введите свое имя', reply_markup=menu)
            await state.set_state(SignupStates.name)

    else:
        if curent == None:
            await message.answer(f"👕 Harid qilgan mahsulotingiz / Купленный товар",
                                 reply_markup=items_inline(iteam))
            await state.set_state(SignupStates.items)
        else:
            await state.clear()
            await message.answer(f"📝 Ma'lumotlarni kiriting / Введите информацию", reply_markup=menu)
            await message.answer(f"👕 Harid qilgan mahsulotingiz / Купленный товар", reply_markup=items_inline(iteam))
            await state.set_state(SignupStates.items)


@router.message(SignupStates.name)
async def state_name(message: Message, state: FSMContext):
    if 4 <= len(message.text) <= 50:
        if not any(digit in message.text for digit in '0123456789'):
            await state.update_data(name=message.text)
            await message.answer(f"✅ Qabul qilindi / Принято\n👤 {message.text}")
            await message.answer(f"📅 Yoshingizni kiriting / Введите свой возраст")
            await state.set_state(SignupStates.age)
        else:
            await message.answer("❌ Ismda raqamlar bo\'lishi mumkunemas / Невозможно иметь цифры в имени")
    else:
        await message.answer("❌ Kiritgan ma'lumotingiz uzunligi xato / Длина введенной вами информации неверна")


@router.message(SignupStates.age)
async def state_name(message: Message, state: FSMContext):
    if message.text.isdigit() and 4 < int(message.text) < 150:
        await state.update_data(age=message.text)
        await message.answer(f"✅ Qabul qilindi / Принято\n📅 {message.text}")
        await message.answer(f"📞 Telefon raqamingizni jo'nating / Отправьте свой номер телефона", reply_markup=phone)
        await state.set_state(SignupStates.phone)
    else:
        await message.answer(
            "❌ Yoshni to'g'ri kiriting (4 va 150 oralig\'ida)\nВведите правильный возраст (от 4 до 150 лет)")


@router.message(SignupStates.phone)
async def state_name(message: Message, state: FSMContext):
    if message.contact:
        await state.update_data(phone=message.contact.phone_number)
        await message.answer(f"✅ Qabul qilindi / Принято\n📞 {message.contact.phone_number}")

        data = await state.get_data()

        user = (f"{message.from_user.mention_html('👤📝 Ma`lumotlar / Информация:')}\n\n"
                f"👤 Ism / Имя: {data.get('name')}\n"
                f"📅 Yosh / Возраст: {data.get('age')}\n"
                f"📱 Telegram / Телеграм: @{message.from_user.username}\n"
                f"📞 Telefon raqam / Номер телефона: {data.get('phone')}\n")

        await message.answer(user, parse_mode='HTML', reply_markup=check)
        await message.answer(f"Ma\'lumotlarni tasdiqlaysizmi?\nTasdiqlash: Yes\nBoshidan boshlash: /new ni tanlang")
        await message.answer(f"Подтвердите информацию?\nПодтвердите: Yes\nНачать заново: /new")

        await state.set_state(SignupStates.verify)

    else:
        await message.answer("❌ Contact ma'lumotini yuboring")


@router.message(SignupStates.verify)
async def state_name(message: Message, state: FSMContext):
    if message.text.lower() == 'yes':
        data = await state.get_data()

        api_data = {
            'name': data.get('name'),
            'username': message.from_user.username,
            'age': data.get('age'),
            'phone': data.get('phone'),
            'telegram_id': message.from_user.id,
        }

        postResponse = requests.post(url=f"{API}/create_user/", data=api_data)
        iteam = requests.get(url=f"{API}/items/").json()

        if postResponse.status_code in [200, 201]:
            json.dumps(postResponse.json(), indent=4)
            await message.answer(f"✅ Ro'yxatdan o'tdingiz / Вы зарегистрированы", reply_markup=menu)
            await message.answer(f"👕 Harid qilgan mahsulotingiz / Купленный товар",
                                 reply_markup=items_inline(iteam))
            await state.set_state(SignupStates.items)
        else:
            txt = (f"❌ Ma'lumotlaringiz saqlanmadi / Ваши данные не были сохранены \n\n"
                   f"🗑 Jarayonni bekor qilish / Отменить процесс: /stop \n"
                   f"🔄 Jarayonni boshidan boshlash / Начать процесс с начала: /new \n")
            await message.answer(txt, reply_markup=check)
    else:
        txt = (f"✔️ Ma\'lumotlarni tasdiqlash / Проверка данных: Yes \n"
               f"🗑 Jarayonni bekor qilish / Отменить процесс: /stop \n"
               f"🔄 Jarayonni boshidan boshlash / Начать процесс с начала: /new \n")
        await message.answer(txt, reply_markup=check)


# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

@router.callback_query(SignupStates.items)
async def state_name(call: CallbackQuery, state: FSMContext):
    await state.update_data(items=call.data)
    mes = call.data.split(':')[1]
    await call.message.answer(f"✅ Qabul qilindi / Принято\n👕 {mes}")
    await call.message.answer(f"📝 Fikr va mulohazalaringizni qoldiring,\nОставьте свои комментарии и отзывы",
                              reply_markup=menu)
    await call.answer(cache_time=4)

    await state.set_state(SignupStates.feedback)


@router.message(SignupStates.feedback)
async def state_name(message: Message, state: FSMContext, bot: Bot):
    if message.text is not None:
        data = requests.get(url=f"{API}/users/{message.from_user.id}").json()
        await state.update_data(feedback=message.text)
        data_st = await state.get_data()
        mes = data_st.get('items').split(':')[1]
        mes_id = data_st.get('items').split(':')[0]

        feed = (f"{message.from_user.mention_html('👤📝 User ma`lumotlari: ')}\n"
                f"👤 Ism: {data['name']}\n"
                f"📅 Yosh: {data['age']}\n"
                f"📱 Telegram: @{message.from_user.username}\n"
                f"📞 Telefon raqam: {data['phone']}\n"
                f"👕 Mahsulot: {mes}\n"
                f"📝 Feedback: {data_st.get('feedback')}\n"
                )

        save_fb = {
            'user': int(data['id']),
            'text': data_st.get('feedback'),
            'items': int(mes_id),
        }

        postResponse = requests.post(url=f"{API}/feedback_create/", data=save_fb)

        if postResponse.status_code in [200, 201]:
            json.dumps(postResponse.json(), indent=4)
            await message.answer(f"✅ Qabul qilindi / Принято\n📝 {message.text}")
            await message.answer(f"📝 Fikr va mulohazalaringiz uchun rahmat.",
                                 reply_markup=menu)
            await message.answer(f"📝 Спасибо за Ваши комментарии и предложения.",
                                 reply_markup=menu)
            await bot.send_message(ADMIN, f"📝 Yangi ma'lumot:\n\n{feed}", parse_mode='HTML')
            await state.clear()
        else:
            txt = (f"❌ Ma'lumotlaringiz saqlanmadi / Ваши данные не были сохранены \n\n"
                   f"🗑Jarayonni bekor qilish / Отменить процесс: /stop \n"
                   f"🔄Jarayonni boshidan boshlash / Начать процесс с начала: /new \n")
            await message.answer(txt, reply_markup=check)

    else:
        await message.answer(f"❌ Matnli ma'lumot yuboring / Отправить текстовое сообщение")
