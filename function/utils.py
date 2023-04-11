
from data.API_connect import HeadHunterAPI, SuperJobAPI, Vacancy
from requests import get, post, put, delete

platforms=0
while not (platforms in  [1, 2, 3]):
    platforms = int(input('выберите платформу 1 - "HeadHunter", 2- "SuperJob", 3 - "HeadHunter"+"SuperJob"\n'))
    if platforms in [1, 2, 3]:
        print("платформа успешно введрена")
    else:
        print("ошибка ввода")

search_query = input('Введите поисковый запрос: ')
top_n = int(input("Введите количество вакансий для вывода в топ N: "))


# # Создание экземпляра класса для работы с вакансиями
vacancy = Vacancy(platforms,search_query,top_n)
ii=0
#Печать полученного списка
for i in vacancy.list:
    ii+=1
    print(i)
    if ii == int(top_n):
        break
