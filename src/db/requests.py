import psycopg2
import os
from dotenv import load_dotenv


def create_connection(connection_string: str):
    new_connection = None
    try:
        new_connection = psycopg2.connect(connection_string)
        print("Connection to MySQL DB successful")
    except Exception as e:
        print(f"The error '{e}' occurred")
    return new_connection


load_dotenv()
connection = create_connection(os.getenv('DB_HOST'))


def request_data(query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        print(f"The error '{e}' occurred")


def submit_data(query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
    except Exception as e:
        print(f"The error '{e}' occurred")


def get_products():
    req1 = '''select * from product'''
    return request_data(req1)


def get_models(product_id):
    req2 = f'''select * from model where productId="{product_id}"'''
    return request_data(req2)


def get_param_options(name, param, model_id):
    np = name + param
    npc = np + 'Connection'
    req3 = f'''SELECT c.*
FROM {np} c
JOIN {npc} cc ON c.id = cc.paramId
WHERE cc.modelId = {model_id};'''
    return request_data(req3)


def add_offer(ofr):
    params_keys = ', '.join(ofr['params'].keys())
    values = [f'"{i}"' for i in ofr['params'].values()]
    params_values = ', '.join(values)
    req4 = f'''INSERT INTO {ofr['product']}Offer
(model, user, {params_keys}, price)
VALUES ("{ofr['model']}", "{ofr['user']}", {params_values}, {ofr['price']})'''
    submit_data(req4)


def find_offers(ofr):
    columns = ['model'] + list(ofr['params'].keys()) + ['price', 'user']
    conditions = [f'''model="{ofr['model']}"''']
    for key in ofr['params']:
        if ofr['params'][key] != 'None':
            conditions.append(f'''{key}="{ofr['params'][key]}"''')
    req5 = f'''select {', '.join(columns)} from {ofr['product']}Offer
where {' AND '.join(conditions)}'''
    return request_data(req5)


def to_row(data):
    params = ''
    for param in data['params']:
        params = params + data[param] + ' '
    return f"{data['productName']}\n{data['modelName']}\n{params}- {data['price']} р.\nот {data['user']} "


def find_offers_by_id(username):
    products = []
    for i in get_products():
        _id, product = i
        products.append(product)
    offers = {}
    for product in products:
        req = f'''select * from {product}Offer where user = "{username}"'''
        offers[product] = request_data(req)
    return offers


def delete_offer(offer_list):
    offer, product = offer_list
    req6 = f'''DELETE FROM {product}Offer WHERE id = {offer[0]} LIMIT 1;'''
    submit_data(req6)


def check_user(_id, username, chat_id):
    req7 = f"""SELECT user_id FROM Users WHERE user_id='{_id}';"""
    result = request_data(req7)
    if not result:
        req8 = f"""INSERT INTO Users (user_id, nickname, chat_id) VALUES('{_id}', '{username}', '{chat_id}');"""
        submit_data(req8)
    return not result
