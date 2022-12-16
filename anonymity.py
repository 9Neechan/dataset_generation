import pandas as pd
from pycanon import anonymity
from sklearn.utils import shuffle

'''Входные данные для контрольного примера'''
card_parameter = 1  # сколько первых цифр карты оставить в анонимизированном датасете (от 1 до 4)
price_parameter = 745000  # диапазон цены (> или < заданного значения)
shuffle_parameter = 1  # любое целое число
k_counter = 3  # параметр k-anonymity, который хотим достичь

dataset = pd.read_excel('D:\\AllProjects\\PyCharmProjects\\dataGeneration2var\\dataset.xlsx')
dataset["Дата и время"] = dataset["Дата и время"].astype('datetime64[ns]')


#  функция реализует локальное обобщение для даты
def hide_date(t):
    if 9 <= t <= 11:
        return "осень"
    elif 3 <= t <= 5:
        return "весна"
    elif 6 <= t <= 8:
        return "лето"
    else:
        return "зима"


def hide_coordinates(a):
    return "Санкт-Петербург"


def hide_card(mask):
    for j in range(4 - card_parameter):
        mask += '*'
    return mask + ' **** **** ****'


def hide_price(price):
    if price < price_parameter:
        return "<" + str(price_parameter)
    else:
        return ">" + str(price_parameter)


def main():
    # Удаление атрибутов
    dataset.drop(columns=["ФИО", "Корзина"], axis=1, inplace=True)
    # Локальное обобщение
    dataset['Дата и время'] = dataset['Дата и время'].apply(lambda z: hide_date(z.month)).astype('string')
    dataset['Долгота и широта'] = dataset['Долгота и широта'].apply(lambda z: hide_coordinates(z)).astype('string')
    # Маскеризация
    dataset['Номер карточки'] = dataset['Номер карточки'].apply(lambda z: hide_card(z[:card_parameter]) if z != "наличными" else z).astype('category')
    # Микро-агрегация
    dataset['Стоимость'] = dataset['Стоимость'].apply(lambda z: hide_price(z)).astype('string')
    # Перемешивание
    dataset['Название магазина'] = shuffle(dataset['Название магазина'], random_state=shuffle_parameter).reset_index(drop=True)

    # считаем k-anonymity
    len_datadet = len(dataset['Название магазина'])
    QI = ['Название магазина', 'Дата и время', 'Долгота и широта', 'Номер карточки', 'Количество товаров', 'Стоимость']
    k_initial, k_arr = anonymity.k_anonymity(dataset, QI)
    count_rows = 0
    for i in range(len(k_arr)):
        if len(k_arr[i]) < k_counter:
            dataset.drop(k_arr[i], inplace=True)
            count_rows += len(k_arr[i])
    k_final, k_arr = anonymity.k_anonymity(dataset, QI)
    final_rows = dataset.size // len(dataset.columns)

    # Outputting information
    print("%d строк было удалено, чтобы достичь k-anonymity==%d" % (count_rows, k_final))
    print("%d первоначальный размер дата-сета" % len_datadet)
    print("%d текущий размер дата-сета" % final_rows)
    print("Процент повреждения данных: %.2f" % float(100 - 100 / len_datadet * final_rows) + "%")

    dataset.to_excel('anonym_dataset.xlsx', index=False)


if __name__ == '__main__':
    main()