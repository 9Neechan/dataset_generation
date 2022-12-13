import pandas as pd
import data as dt
import random


def main():
    buyers_list = []
    for id_c in range(dt.amount_of_buyers):
        visits = random.randint(5, 10)
        fio = dt.get_fio()
        card = dt.get_card(id_c)

        for i in range(visits):
            shop_name = dt.get_shop_name()
            time_date = dt.get_time_date()
            coordinates = dt.get_coordinates()
            basket, purchases = dt.get_purchases()
            price = dt.get_price()
            buyers_list.append([fio, shop_name, time_date, coordinates, basket, card, purchases, price])
            #print([fio, shop_name, time_date, coordinates, basket, card, purchases, price])

    dataset = pd.DataFrame.from_dict(buyers_list)
    dataset.columns = ['ФИО', 'Название магазина', 'Дата и время', 'Долгота и широта', 'Корзина',
                       'Номер карточки', 'Количество товаров', 'Стоимость']
    dataset.to_excel('dataset.xlsx', index=False)


if __name__ == '__main__':
    main()








