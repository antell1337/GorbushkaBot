from aiogram import types, Dispatcher
from create_bot import dp
from keyboards import client_kb
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from db import requests


# состояния-------------------\

class FSMBuy(StatesGroup):  # Покупка
    product = State()
    model = State()
    params = State()


# ----------------------------|


class FSMSell(StatesGroup):  # Продажа
    product = State()
    model = State()
    params = State()
    price = State()


# ----------------------------|


class FSMMyoffers(StatesGroup):  # Мои офферы
    offers = State()


# ----------------------------/


# Скрипты -------------------\
def to_row(data):
    params = ''
    for param in data['params']:
        params = params + data[param] + ' '
    return f"{data['modelName']} {params}- {data['price']} р. от {data['user']} "


def generate_row(tuple_):
    rowlist = list(tuple_)
    if type(rowlist[0]) is int:
        rowlist.pop(0)
    size = len(rowlist)
    params = ' '.join(list([i for i in rowlist[:size - 2]]))
    price = rowlist[size - 2]
    user = rowlist[size - 1]
    return f'{params} - {price} р. от {user}'


def find_offers_by_data(data):
    ofr = dict()
    ofr['product'] = data['productName']
    ofr['model'] = data['modelName']
    ofr['params'] = {}
    for i in data['params']:
        ofr['params'][i] = data[i]
    offers = requests.find_offers(ofr)
    return list([list(offer) for offer in offers])


def create_offer_by_data(data):
    ofr = dict()
    ofr['product'] = data['productName']
    ofr['model'] = data['modelName']
    ofr['user'] = data['user']
    ofr['params'] = {}
    for i in data['params']:
        ofr['params'][i] = data[i]
    ofr['price'] = data['price']
    requests.add_offer(ofr)


# ---------------------------/


# Сообщения ------------------------------------------\
start_message = '''Привет!
Это бот для всех продавцов и покупателей Горбушки. 
Здесь вы можете предложить свои товары всем пользователям бота или же посмотреть чужие предложения и договориться о покупке с продавцами.

Если заметите ошибку или есть предложения по улучшению бота - пишите @Antell1337

Сейчас бот работает бесплатно для всех. Если бот помог вам найти хорошую цену или редкую позицию - поддержите проект!
+79023156277 - Тинькофф.
Деньги пойдут на оплату серверов'''


# ----------------------------------------------------/


# хэндлеры ---------------------------------------------------------------------------------------------------------\\\
# Домашняя страница ------------------------------------------------------------------------------------------------\
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    if requests.check_user(message.from_user.id, message.from_user.username, message.chat.id):
        await message.answer("Ваш личный кабинет был успешно создан")
    await message.answer(start_message, reply_markup=client_kb.inline_start_kb)


@dp.callback_query_handler(text='home btn', state='*')
async def process_callback_back_btn(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(start_message, reply_markup=client_kb.inline_start_kb)
    await state.finish()
    await callback.message.delete_reply_markup()
    await callback.answer()


# Продать ---------------------------------------------------------------------------------------------------------\
@dp.callback_query_handler(text='sell btn')
async def process_callback_sell_btn(callback: types.CallbackQuery):
    await FSMSell.product.set()
    await callback.message.answer('Выберите товар который хотите продать.', reply_markup=client_kb.product_kb())
    await callback.message.delete_reply_markup()
    await callback.answer()


# ----------------------------------------------------------------------------------------------------------------|


@dp.callback_query_handler(state=FSMSell.product)
async def process_callback_product_btn(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['productName'], data['productId'] = callback.data.split('; ')
        data['user'] = '@' + callback.from_user.username
    await FSMSell.next()
    await callback.message.answer('Выберите модель.', reply_markup=client_kb.model_kb(data['productId']))
    await callback.message.delete_reply_markup()
    await callback.answer()


# ----------------------------------------------------------------------------------------------------------------|


@dp.callback_query_handler(state=FSMSell.model)
async def process_callback_model_btn(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if 'paramIter' not in data.keys():
            data['modelId'], data['modelName'], param_str = callback.data.split('///')
            data['params'] = param_str.split('; ')
            data['paramIter'] = 0
        else:
            data[data['params'][data['paramIter']]] = callback.data
            data['paramIter'] += 1
        await callback.message.answer(f"Выберите {data['params'][data['paramIter']]}",
                                      reply_markup=client_kb.param_kb(data['productName'],
                                                                      data['modelId'],
                                                                      data['params'][data['paramIter']]
                                                                      )
                                      )
    if data['paramIter'] == len(data['params']) - 1:
        await FSMSell.next()
    await callback.message.delete_reply_markup()


# ----------------------------------------------------------------------------------------------------------------|


@dp.callback_query_handler(state=FSMSell.params)
async def process_callback_params_btn(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data[data['params'][data['paramIter']]] = callback.data
    await callback.message.answer('Введите сумму - ТОЛЬКО цифры. (Например - 123000)')
    await FSMSell.next()
    await callback.message.delete_reply_markup()


# ----------------------------------------------------------------------------------------------------------------|


@dp.message_handler(state=FSMSell.price)
async def process_callback_price_msg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text
    create_offer_by_data(data)
    await message.answer(f'Готово! Ваше предложение:\n{to_row(data)}', reply_markup=client_kb.home_kb)


# ----------------------------------------------------------------------------------------------------------------/
# Купить ---------------------------------------------------------------------------------------------------------\
@dp.callback_query_handler(text='buy btn')
async def process_callback_sell_btn(callback: types.CallbackQuery):
    await FSMBuy.product.set()
    await callback.message.answer('Выберите товар который хотите купить.', reply_markup=client_kb.product_kb())
    await callback.message.delete_reply_markup()
    await callback.answer()


# ----------------------------------------------------------------------------------------------------------------|


@dp.callback_query_handler(state=FSMBuy.product)
async def process_callback_buy_product_btn(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['productName'], data['productId'] = callback.data.split('; ')
        data['user'] = '@' + callback.from_user.username
    await FSMBuy.next()
    await callback.message.answer('Выберите модель.', reply_markup=client_kb.model_kb(data['productId']))
    await callback.message.delete_reply_markup()
    await callback.answer()


# ----------------------------------------------------------------------------------------------------------------|


@dp.callback_query_handler(state=FSMBuy.model)
async def process_callback_buy_model_btn(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if 'paramIter' not in data.keys():
            data['modelId'], data['modelName'], param_str = callback.data.split('///')
            data['params'] = param_str.split('; ')
            data['paramIter'] = 0
        else:
            data[data['params'][data['paramIter']]] = callback.data
            data['paramIter'] += 1
        await callback.message.answer(f"Выберите {data['params'][data['paramIter']]}",
                                      reply_markup=client_kb.param_kb(data['productName'],
                                                                      data['modelId'],
                                                                      data['params'][data['paramIter']],
                                                                      add_any=True
                                                                      )
                                      )
    if data['paramIter'] == len(data['params']) - 1:
        await FSMBuy.next()
    await callback.message.delete_reply_markup()


# ----------------------------------------------------------------------------------------------------------------|


@dp.callback_query_handler(state=FSMBuy.params)
async def process_callback_buy_params_btn(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data[data['params'][data['paramIter']]] = callback.data
    offers = sorted(find_offers_by_data(data), key=lambda offer_price: int(offer_price[-2]))
    offers_str = ''
    for offer in offers:
        offers_str += generate_row(offer) + '\n'
    if offers_str == '':
        offers_str = 'К сожалению ничего не нашлось. Ваше предложение может стать первым!'
    await callback.message.answer(f'Вот предложение по вашему запросу:\n' + offers_str, reply_markup=client_kb.home_kb)
    await callback.message.delete_reply_markup()


# ----------------------------------------------------------------------------------------------------------------/


# Мои офферы -----------------------------------------------------------------------------------------------------\


@dp.callback_query_handler(text='my offers btn')
async def process_callback_offers_btn(callback: types.CallbackQuery, state: FSMContext):
    my_offers_str = ''
    offers = requests.find_offers_by_id('@' + callback.from_user.username)
    all_offers = []
    for product in offers.keys():
        for offer in offers[product]:
            all_offers.append([offer, product])
    if len(all_offers) > 0:
        await FSMMyoffers.offers.set()
        async with state.proxy() as data:
            data['offers'] = all_offers
        for i in range(len(all_offers)):
            my_offers_str = my_offers_str + f"{i + 1}. {generate_row(all_offers[i][0])}\n\n"
        await callback.message.answer(f'Вот ваши предложения:\n' + my_offers_str +
                                      'Для удаления сделок введите их номера ЧЕРЕЗ ЗАПЯТУЮ\n(пример: 1, 3, 4, 7, 10)',
                                      reply_markup=client_kb.home_kb)
    else:
        await callback.message.answer(f'Вы еще не создали ни одного предложения. Для создания предложения вернитесь в главное меню и нажмите кнопку продать товар.',
                                      reply_markup=client_kb.home_kb)
    await callback.message.delete_reply_markup()


# ----------------------------------------------------------------------------------------------------------------|


@dp.message_handler(state=FSMMyoffers.offers)
async def process_callback_delete_offers_btn(message: types.Message, state: FSMContext):
    offer_numbers = list([int(i) for i in message.text.split(',')])
    deleted_offers = ''
    async with state.proxy() as data:
        for i in offer_numbers:
            requests.delete_offer(data['offers'][i - 1])
            deleted_offers = deleted_offers + generate_row(data['offers'][i - 1][0]) + '\n\n'
    await message.delete()
    await message.answer(f'Удалены следущие предложения:\n\n {deleted_offers}', reply_markup=client_kb.home_kb)


# ----------------------------------------------------------------------------------------------------------------/


# добавляем хендлеры для работы
def register_handlers_client(dp_reg: Dispatcher):
    dp_reg.register_message_handler(process_start_command, commands=['start'])
