
from data.API_connect import HeadHunterAPI, SuperJobAPI, Vacancy
from operator import *

# Фильтрация типов платформ
platforms=0
while not (platforms in  [1, 2, 3]):
    platforms = int(input('выберите платформу 1 - "HeadHunter", 2- "SuperJob", 3 - "HeadHunter"+"SuperJob"\n'))
    if platforms in [1, 2, 3]:
        print("платформа успешно введена")
    else:
        print("ошибка ввода")

search_query = input('Введите поисковый запрос: ')
top_n = int(input("Введите количество вакансий для вывода в топ N: "))



# # Создание экземпляра класса для работы с вакансиями
vacancy = Vacancy(platforms,search_query,top_n)

# Настраиваемая сортировка по полям  "payment_from" и "payment_to"
payment=0
while not (payment in  [1, 2, 3]):
    payment = int(input('выберите сортировку по параметру\n "payment_from": 1 - уменьшение, 2- увеличение\n  "payment_to": 3 - уменьшение, 4- увеличение\n  5- без сортировки \n'))
    if payment == 1:
        print("сортировка 'payment_from' на уменьшение")
        vacancy.list = sorted(vacancy.list, reverse=True, key=itemgetter("payment_from"))
    elif payment == 2:
        print("сортировка 'payment_from' на увеличение")
        vacancy.list = sorted(vacancy.list, reverse=False, key=itemgetter("payment_from"))
    elif payment == 3:
        print("сортировка 'payment_to' на уменьшение")
        vacancy.list = sorted(vacancy.list, reverse=True, key=itemgetter("payment_to"))
    elif payment == 4:
        print("сортировка 'payment_to' на увеличение")
        vacancy.list = sorted(vacancy.list, reverse=False, key=itemgetter("payment_to"))
    elif payment == 5:
        print("без сортировки")
    else:
        print("ошибка ввода")

# Фильтрация по ключевым словам в поле 'profession'
profession = input('Введите слово содержащаеся в разделе "profession" (если значение не введено фильтрация не производится): \n')



ii=0
#Печать полученного списка
for i in vacancy.list:
    if len(profession)>0:
        if profession not in i.get('profession'):
            continue

    ii+=1
    print(i)
    if ii == int(top_n):
        break
