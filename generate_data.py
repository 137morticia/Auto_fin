import pandas as pd
import random
import string
import os
from datetime import datetime

#создание папки дата, если она не существует
data_folder = 'data'
if not os.path.exists(data_folder):
    os.makedirs(data_folder)

#указываем категории и товары
categories = ['бытовая химия', 'текстиль', 'посуда', 'косметика', 'канцелярия', 'электроника', 'игрушки']
items = {
    'бытовая химия': ['Стиральный порошок', 'Средство для мытья полов', 'Отбеливатель', 'Кондиционер для белья'],
    'текстиль': ['Полотенце', 'Простыня', 'Наволочка', 'Скатерть'],
    'посуда': ['Тарелка', 'Кружка', 'Кастрюля', 'Сковорода'],
    'косметика': ['Тушь', 'Помада', 'Тени', 'Пудра'],
    'канцелярия': ['Ручка', 'Карандаш', 'Тетрадь', 'Линейка'],
    'электроника': ['Наушники', 'Клавиатура', 'USB-кабель', 'Компьютерная мышь'],
    'игрушки': ['Мяч', 'Кукла', 'Конструктор', 'Пазл'],
}

#генерация случайного количества касс от 1 до 5 для 9 магазинов
shops_cashes = {shop: random.randint(1, 5) for shop in range(1, 10)}

#создание множества с чеками
existing_doc_ids = set()

#генерация чеков
def generate_unique_doc_id(existing_ids):
    while True:
        doc_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        if doc_id not in existing_ids:
            break
    existing_ids.add(doc_id)
    return doc_id

today = datetime.today()
#цикл для создания csv файлов по каждому магазину и кассе
res_data = []
for shop, num_cashes in shops_cashes.items():
    for cash in range(1, num_cashes + 1):
        num_items = random.randint(1, 5)  # количество разных товаров в чеке
        for _ in range(num_items):
            category = random.choice(categories)
            item = random.choice(items[category])
            amount = random.randint(1, 30)
            price = random.uniform(10, 130)
            discount = random.randint(0, 30)
            doc_id = generate_unique_doc_id(existing_doc_ids)
            res_data.append({
                'date': today.strftime("%Y-%m-%d"),
                'shop': shop,
                'cash': cash,
                'doc_id': doc_id,
                'item': item,
                'category': category,
                'amount': amount,
                'price': round(price, 2),
                'discount': round(discount, 2),
            })

        df = pd.DataFrame(res_data) # Конвертация данных в DataFrame
        df.to_csv(os.path.join(data_folder, f'{shop}_{cash}.csv'), index=False, encoding='utf-8') # Сохранение в файл CSV





