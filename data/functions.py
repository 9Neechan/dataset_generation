import random
import datetime as dt
import pandas as pd
from faker import Faker

fake = Faker("ru_RU")

'''Входные данные для пользователя'''
# количество покупателей
amount_of_buyers = 10000
#  вероятность генерации пола покупателя
chance_women = 0.6  # 0.1 - 1
chance_men = 0.4  # 0.1 - 1
#  вероятность генерации платежных систем
chance_cash = 0.1  # 0.1 - 1
chance_mir = 0.3  # 0.1 - 1
chance_mastercard = 0.4  # 0.1 - 1
chance_visa = 0.2  # 0.1 - 1
#  вероятность генерации банка, выдавшего карту
chance_sber = 0.45
chance_tinkoff = 0.35
chance_otkrytie = 0.2


shop_name = ["Ситилинк", "М-Видео", "Эльдорадо", "Медиа-Маркт", "Юлмарт", "ТехноСила", "Евросеть", "re:Store", "Микробит", "Связной",
             "DNS", "Максимус", "Технопарк", "Giant Store", "PiterGSM", "Сотик", "GSM Butik", "Пульт.ру", "Kingstore", "HOLODILNIK",
             "Полюс", "BigGeek", "Корпорация Центр", "CStore", "LG", "iPort", "Electrolux", "Banggood", "Техпорт", "OLDI"]


categories = pd.read_excel('D:\\AllProjects\\PyCharmProjects\\dataGeneration2var\\categories.xlsx')
brands = pd.read_excel('D:\\AllProjects\\PyCharmProjects\\dataGeneration2var\\brands.xlsx')
categories = categories['Категория']
brands = brands["Бренд"]
cards = random.sample(range(100000000000, 999999999999), amount_of_buyers)


def get_shop_name():
    a = random.randrange(0, 30)
    return shop_name[a]


#  функция выводит корзину покупок: товар+бренд и их количество
def get_purchases():
    basket = []
    purchases = random.randint(5, 10)  # сколько покупок
    for i in range(purchases):
        k_c = random.randrange(0, len(categories))
        k_b = random.randrange(0, len(brands))
        #brand_list = brands[k_c].split(',')
        #out = categories[k_c] + '(' + brand_list[random.randrange(0, len(brand_list))] + ')'
        out = categories[k_c] + '(' + str(brands[k_b]) + ')'
        basket.append(out)
    return basket, purchases


def get_fio():
    name_gender = random.choices(('Ж', 'М'), weights=[chance_women, chance_men])[0]
    if name_gender == 'Ж':
        name = fake.name_female()
    else:
        name = fake.name_male()
    return name


def get_time_date():
    date = fake.date_between('-1y')
    hour = random.randint(9, 20)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    return str(date) + ' ' + str(dt.timedelta(hours=hour, minutes=minute, seconds=second))


def get_coordinates():  # генерирует координаты на территории СПБ
    d = fake.coordinate(30.925893, 0.153783)
    sh = fake.coordinate(59.925893, 0.1452085)
    return str(sh) + ' ' + str(d)


#  возвращает способ оплаты, номер карты, если способ оплаты по карте
def get_card(t):
    # Cash, Mir, Mastercard, Visa
    system = random.choices(('0', '2', '4', '5'), weights=[chance_cash, chance_mir, chance_mastercard, chance_visa])[0]
    unique_code = '{0}{1}{2}{3}{4}'.format(str(cards[t])[:4], " ", str(cards[t])[4:-4], " ", str(cards[t])[8:])
    # Sberbank, Tinkoff, Otkrytie
    if system == '0':
        return 'наличными'
    elif system == '2':
        bank = '200'
        return '{0}{1}{2}{3}'.format(system, bank, " ", unique_code)
    elif system == '4':
        bank = random.choices(('276', '377', '093'), weights=[chance_sber, chance_tinkoff, chance_otkrytie])[0]
        return '{0}{1}{2}{3}'.format(system, bank, " ", unique_code)
    elif system == '5':
        bank = random.choices(('336', '213', '323'), weights=[chance_sber, chance_tinkoff, chance_otkrytie])[0]
        return '{0}{1}{2}{3}'.format(system, bank, " ", unique_code)


def get_price():
    return random.randint(10000, 700000)


