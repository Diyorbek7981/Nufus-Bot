from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart, and_f
from buttons.reply import menu, phone, check, feedback_verify
from buttons.inline import gender, rate
from states import SignupStates
from aiogram.fsm.context import FSMContext
from config import ADMIN, API
import requests
import json

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(
        f'👋🏻Assalomu alaykum {message.from_user.full_name} \n🫡bizning xizmatlar xaqida fikringizni qoldiring',
        reply_markup=menu)


@router.message(F.text == '📝Feedback qoldirish')
async def signup(message: Message, state: FSMContext):
    res = requests.get(url=f"{API}/users/{message.from_user.id}")
    if res.status_code == 404:
        await message.answer(f"❗ Fikr-mulohazalaringizni qoldirish uchun botda ro'yhatdan o'ting")
        await message.answer(f'👤To\'liq Ismingizni kiriting')
        await state.set_state(SignupStates.name)
    else:
        await message.answer(f"📝Fikr-mulohazalaringizni qoldiring")
        await state.set_state(SignupStates.feedback)


@router.message(Command("stop"))
async def state_name(message: Message, state: FSMContext):
    curent = await state.get_state()
    if curent == None:
        await message.answer('🔍To\'xtatish uchun ma\'lumot mavjud emas', reply_markup=menu)
    else:
        await message.answer(f"❌ Jarayon bekor qilindi", reply_markup=menu)
        await state.clear()


@router.message(Command("new"))
async def state_name(message: Message, state: FSMContext):
    curent = await state.get_state()

    res = requests.get(url=f"{API}/users/{message.from_user.id}")
    if res.status_code == 404:
        if curent == None:
            await message.answer(f"❗ Fikr-mulohazalaringizni qoldirish uchun botda ro'yhatdan o'ting")
            await message.answer(f'👤To\'liq Ismingizni kiriting', reply_markup=menu)
            await state.set_state(SignupStates.name)
        else:
            await state.clear()
            await message.answer(f'👤To\'liq Ismingizni kiriting', reply_markup=menu)
            await state.set_state(SignupStates.name)

    else:
        if curent == None:
            await message.answer(f"📝Fikr-mulohazalaringizni qoldiring", reply_markup=menu)
            await state.set_state(SignupStates.feedback)
        else:
            await state.clear()
            await message.answer(f"📝Fikr-mulohazalaringizni qoldiring", reply_markup=menu)
            await state.set_state(SignupStates.feedback)


@router.message(SignupStates.name)
async def state_name(message: Message, state: FSMContext):
    if 4 <= len(message.text) <= 50:
        if not any(digit in message.text for digit in '0123456789'):
            await state.update_data(name=message.text)
            await message.answer(f"✅Ism qabul qilindi\n👤{message.text}")
            await message.answer(f"👱🏻‍♂️/👩Jinsingizni ko'rsating", reply_markup=gender)
            await state.set_state(SignupStates.gender)
        else:
            await message.answer("❌ Ismda raqamlar bo\'lishi mumkunemas")
    else:
        await message.answer("❌ Kiritgan malumotingiz uzunligi xato")


@router.callback_query(SignupStates.gender)
async def state_name(call: CallbackQuery, state: FSMContext):
    if call.data == 'Erkak':
        await state.update_data(gender=call.data)
        await call.message.answer(f"✅Jins qabul qilindi\n👱‍♂️{call.data}")
        await call.message.answer(f"📅Yoshingizni kiriting")
        await state.set_state(SignupStates.age)
    elif call.data == 'Ayol':
        await state.update_data(gender=call.data)
        await call.message.answer(f"✅Jins qabul qilindi\n👩{call.data}")
        await call.message.answer(f"📅Yoshingizni kiriting")
        await state.set_state(SignupStates.age)
    else:
        await call.message.answer(f"❌To'g'ri malumot kiriting", reply_markup=gender)


@router.message(SignupStates.age)
async def state_name(message: Message, state: FSMContext):
    if message.text.isdigit() and 4 < int(message.text) < 150:
        await state.update_data(age=message.text)
        await message.answer(f"✅Yosh qabul qilindi\n📅{message.text}")
        await message.answer(f"📞Telefon raqamingizni jo'nating", reply_markup=phone)
        await state.set_state(SignupStates.phone)
    else:
        await message.answer("❌ Yoshni to'g'ri kiriting")


@router.message(and_f(SignupStates.phone, F.contact))
async def state_name(message: Message, state: FSMContext):
    if message.contact:
        await state.update_data(phone=message.contact.phone_number)
        await message.answer(f"✅Telefon raqam qabul qilindi\n📞{message.contact.phone_number}")

        data = await state.get_data()

        user = (f"{message.from_user.mention_html('👤📝User malumotlari:')}\n"
                f"👤Ism: {data.get('name')}\n"
                f"👱🏻‍♂️/👩Jinsi: {data.get('gender')}\n"
                f"📅Yosh: {data.get('age')}\n"
                f"📱Telegram: @{message.from_user.username}\n"
                f"📞Telefon raqam: {data.get('phone')}\n")

        await message.answer(f"{user} \n\nHa yoki /new ni tanlang", parse_mode='HTML',
                             reply_markup=check)

        await state.set_state(SignupStates.verify)

    else:
        await message.answer("❌ Contact malumotini yuboring")


@router.message(SignupStates.verify)
async def state_name(message: Message, bot: Bot, state: FSMContext):
    if message.text.lower() == 'ha':
        data = await state.get_data()

        user = (f"{message.from_user.mention_html('👤📝User malumotlari:')}\n"
                f"👤Ism: {data.get('name')}\n"
                f"👱🏻‍♂️/👩Jinsi: {data.get('gender')}\n"
                f"📅Yosh: {data.get('age')}\n"
                f"📱Telegram: @{message.from_user.username}\n"
                f"📞Telefon raqam: {data.get('phone')}\n")

        api_data = {
            'name': data.get('name'),
            'username': message.from_user.username,
            'age': data.get('age'),
            'phone': data.get('phone'),
            'gender': data.get('gender'),
            'telegram_id': message.from_user.id,
        }

        postResponse = requests.post(url=f"{API}/create_user/", data=api_data)

        if postResponse.status_code in [200, 201]:
            json.dumps(postResponse.json(), indent=4)
            await message.answer(user + f"\n\n📝Malumotlaringiz saqlandi", parse_mode='HTML', reply_markup=menu)
            await message.answer(f"📝Fikr va mulihazalaringiz qoldiring")
            await state.set_state(SignupStates.feedback)
        else:
            txt = (f"❌ Malumotlaringiz saqlanmadi \n\n"
                   f"🗑Arizani bekor qilish: /stop \n"
                   f"🔄Arizani boshidan boshlash: /new \n")
            await message.answer(txt, reply_markup=check)
    else:
        txt = (f"✔️Arizani tasdiqlash: Ha \n"
               f"🗑Arizani bekor qilish: /stop \n"
               f"🔄Arizani boshidan boshlash: /new \n")
        await message.answer(txt, reply_markup=check)


# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

@router.message(SignupStates.feedback)
async def state_name(message: Message, state: FSMContext):
    await state.update_data(feedback=message.text)
    await message.answer(f"✅Fikr va mulihazalaringiz qabul qilindi\n📝{message.text}")
    await message.answer(f"🌟 Hizmatimizni baholang", reply_markup=rate)

    await state.set_state(SignupStates.rate)


@router.callback_query(SignupStates.rate)
async def state_name(call: CallbackQuery, state: FSMContext):
    await state.update_data(rate=call.data)
    await call.message.answer(f"✅Qabul qilindi\n🌟{call.data}")
    await call.message.answer(f"📝Malumotlaringiz saqlansinmi", reply_markup=feedback_verify)

    await state.set_state(SignupStates.verify_fb)


@router.message(SignupStates.verify_fb)
async def state_name(message: Message, bot: Bot, state: FSMContext):
    if message.text.lower() == 'tasdiqlash':
        data = requests.get(url=f"{API}/users/{message.from_user.id}").json()
        data_st = await state.get_data()

        feed = (f"{message.from_user.mention_html('👤📝User malumotlari:')}\n"
                f"👤Ism: {data['name']}\n"
                f"👱🏻‍♂️/👩Jinsi: {data['gender']}\n"
                f"📅Yosh: {data['age']}\n"
                f"📱Telegram: @{message.from_user.username}\n"
                f"📞Telefon raqam: {data['phone']}\n"
                f"📝Feedback: {data_st.get('feedback')}\n"
                f"🌟Rate: {data_st.get('rate')}⭐")

        save_fb = {
            'user': int(data['id']),
            'text': data_st.get('feedback'),
            'rate': data_st.get('rate'),
        }

        postResponse = requests.post(url=f"{API}/feedback_create/", data=save_fb)

        if postResponse.status_code in [200, 201]:
            json.dumps(postResponse.json(), indent=4)
            await message.answer(f"📝Malumotlaringiz Adminga yuborildi fikr qoldirganingiz uchun rahmat",
                                 reply_markup=menu)
            await bot.send_message(ADMIN, f"📝Yangi malumot:\n\n{feed}", parse_mode='HTML')
            await state.clear()
        else:
            txt = (f"❌ Malumotlaringiz saqlanmadi \n\n"
                   f"🗑Arizani bekor qilish: /stop \n"
                   f"🔄Arizani boshidan boshlash: /new \n")
            await message.answer(txt, reply_markup=check)
    else:
        txt = (f"✔️Arizani tasdiqlash: Ha \n"
               f"🗑Arizani bekor qilish: /stop \n"
               f"🔄Arizani boshidan boshlash: /new \n")
        await message.answer(txt, reply_markup=check)
