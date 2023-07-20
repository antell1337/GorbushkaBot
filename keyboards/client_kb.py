from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, \
    InlineKeyboardMarkup
from db import requests


# клавиатура из листа кнопок
def generate_kb(buttons):
    kb = InlineKeyboardMarkup()
    for button in buttons:
        kb.add(button)
    kb.add(home_btn)
    return kb


# Клава отмены ------------------------------------------------\
back_btn = InlineKeyboardButton('Отмена 🔙', callback_data='back btn')
back_kb = InlineKeyboardMarkup().add(back_btn)
# -------------------------------------------------------------/

# Клава домой ------------------------------------------------\
home_btn = InlineKeyboardButton('Домой 🔙', callback_data='home btn')
home_kb = InlineKeyboardMarkup().add(home_btn)
# -------------------------------------------------------------/

# Стартовая клава ---------------------------------------------\
sell_btn = InlineKeyboardButton('Продать товар', callback_data='sell btn')
buy_btn = InlineKeyboardButton('Найти и купить товар', callback_data='buy btn')
offers_btn = InlineKeyboardButton('Мои сделки', callback_data='my offers btn')
inline_start_kb = InlineKeyboardMarkup().row(buy_btn, sell_btn).add(offers_btn)
# -------------------------------------------------------------/


# Продукты клава ---------------------------------------------\
def product_kb():
    buttons = []
    products = requests.get_products()
    for i in range(len(products)):
        _id, name = products[i]
        buttons.append(InlineKeyboardButton(name, callback_data=f'{name}; {_id}'))
    return generate_kb(buttons)
# -------------------------------------------------------------/


# Модели клава ---------------------------------------------\
def model_kb(id0):
    models = requests.get_models(id0)
    buttons = []
    for i in range(len(models)):
        model_id, product_id, name, param_str = models[i]
        buttons.append(InlineKeyboardButton(name, callback_data=f'{model_id}///{name}///{param_str}'))
    return generate_kb(buttons)
# -------------------------------------------------------------/


# Параметр клава ---------------------------------------------\
def param_kb(product_name, model_id, param, add_any=False):
    params = requests.get_param_options(product_name, param, model_id)
    buttons = []
    for i in range(len(params)):
        param_id, param_name = params[i]
        buttons.append(InlineKeyboardButton(param_name, callback_data=param_name))
    if add_any:
        buttons.append(InlineKeyboardButton('Любой', callback_data='None'))
    return generate_kb(buttons)
# -------------------------------------------------------------/
