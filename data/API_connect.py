import json
import os
from abc import ABC, abstractmethod
import time
from requests import get, post, put, delete





class Engine(ABC):
    @abstractmethod
    def get_vacancies(self):
        pass

    @abstractmethod
    def get_page(self, page=0):
        pass
class Vacancy ():
    """"Класс Vacancy"""

    list = []

    def __init__(self, platforms,search_query,top_n):

        self.platforms = platforms  # платформа 1 - "HeadHunter", 2- "SuperJob", 3 - "HeadHunter"+"SuperJob"
        self.search_query =search_query #  поисковый запрос
        self.top_n = top_n # количество листов вакансий для вывода
        self.vacancy = self.get_vacancies()

        pass

    def get_vacancies(self):


        if self.platforms in [1, 3]: # загрузка платформы 1 - "HeadHunter"
            hh_vacancy = HeadHunterAPI(self.search_query,self.top_n)
            file1 = hh_vacancy.file
            f= open(file1, mode='r', encoding='utf-8')
            data = json.load(f)
            f.close()

            for i in data:
                for ii in i.get('items'):
                    try:
                        self.list.append({
                                "payment_from": int(ii.get("salary", {}).get("from")),  # Сумма оклада от
                                "payment_to": int(ii.get("salary", {}).get("to")),  # Сумма оклада до
                                "currency": ii.get("salary", {}).get("currency"), # Валюта. Список возможных значений:  rub — рубль  uah — гривна  uzs — сум
                                "platforms":"HeadHunter", # платформа ["HeadHunter", "SuperJob"]
                                 "profession":ii.get("name"), # название вакансии
                                 "candidat":ii.get("snippet",{}).get("requirement"), # 	Требования к кандидату
                                 "work": ii.get("snippet",{}).get("responsibility"), # Должностные обязанности
                                 "compensation": ii.get("working_days"), # Условия работы
                                 "profession_url":ii.get("url") # ссылка на вакансию
                                                                   })
                    except:
                       pass


        if self.platforms in [2, 3]: # загрузка платформы 2- "SuperJob"
            sj_vacancy = SuperJobAPI(self.search_query,self.top_n)
            file2 = sj_vacancy.file
            f = open(file2, mode='r', encoding='utf-8')
            data = json.load(f)
            f.close()
            for i in data:
                for ii in i.get('objects'):
                    try:
                        self.list.append({
                                 "payment_from": int(ii.get("payment_from")),  # Сумма оклада от
                                 "payment_to": int(ii.get("payment_to")),  # Сумма оклада до
                                 "currency": ii.get("currency"), # Валюта. Список возможных значений:  rub — рубль  uah — гривна  uzs — сум
                                 "platforms": "SuperJob", # платформа ["HeadHunter", "SuperJob"]
                                 "profession": ii.get("profession"), # название вакансии
                                 "candidat": ii.get("candidat"), # 	Требования к кандидату
                                 "work": ii.get("work"), # Должностные обязанности
                                 "compensation": ii.get("compensation"), # Условия работы
                                 "profession_url": ii.get("profession_url") # ссылка на вакансию

                                 })

                    except:
                        pass

        # self.list = sorted(self.list, reverse=True, key= itemgetter ("payment_from"))

        return self.list

    def __repr__(self):
        return f'Vacancy({self.search_query}, {self.top_n})'

    def __str__(self):
        return f'{self.search_query}, {self.top_n}'

class SuperJobAPI (Engine):
    """"Класс SuperJobAPI"""
    list = []

    def __init__(self, vacancy, top_n):
        self.vacancy = vacancy
        self.file = '../data/get_SJ.json'
        self.url = 'https://api.superjob.ru/2.0/vacancies'
        self.pages = int(-1 * top_n // 1 * -1)
        self.job_list = self.get_vacancies()

        pass

    def get_page(self, page=0):
        """
          метод для получения страницы со списком вакансий.
          Аргументы: page - Индекс страницы, начинается с 0. Значение по умолчанию 0, т.е. первая страница
          """

        # Справочник для параметров GET-запроса
        par = {
            "keywords": self.vacancy, # ключевое слово для поиска
            "page": page
        }
        # API_KEY скопирован из гугла и вставлен в переменные окружения
        api_key: str = os.environ['SUPERJOB_API_KEY']
        headers = {"X-Api-App-Id": api_key} # передаем API_KEY в шапку запроса
        req = get(self.url, headers=headers, params=par)  # Посылаем запрос к API
        data = req.json()  # Декодируем его ответ, чтобы Кириллица отображалась корректно
        # проверка на наличие данных на странице
        if data.get('objects', {})[0].get('id') is not None:
            self.list.append(data)
        req.close()
        return data


    def get_vacancies(self):
        """переноса агруженных данных в файл json"""

        for page in range(0, self.pages):

            # делаем обращение к функции get_page
            r_page = self.get_page(page)

            # Проверка на наличие данных на странице
            if r_page.get('objects', {})[0].get('id') is None:
                break

            # Необязательная задержка, но чтобы не нагружать сервисы hh, оставим. 5 сек мы может подождать
            time.sleep(0.5)

        # Создаем новый документ, записываем в него ответ запроса, после закрываем
        f = open(self.file, mode='w', encoding='utf8')
        f.write(json.dumps(self.list, ensure_ascii=False))
        f.close()

        print('Вакансии SuperJob сохранены в файл')
        return json.dumps(self.list, ensure_ascii=False)



class HeadHunterAPI (Engine):
    """"Класс HeadHunterAPI"""
    list = []

    def __init__(self, vacancy, top_n):
        self.vacancy = vacancy
        self.file = '../data/get_HH.json'
        self.url ='https://api.hh.ru/vacancies'
        self.pages = int(-1 * top_n // 1 * -1)
        self.job_list = self.get_vacancies()

        pass

    def get_page(self, page = 0):
        """
          метод для получения страницы со списком вакансий.
          Аргументы: page - Индекс страницы, начинается с 0. Значение по умолчанию 0, т.е. первая страница
          """
        # Справочник для параметров GET-запроса
        par = {
            'text': self.vacancy, # Текст фильтра. В имени должно быть слово job_title
            'area': '1', # Поиск ощуществляется по вакансиям htubjyf 113 (1 - город Москва)
            'per_page': '20', # Кол-во вакансий на 1 странице
            'page': page # Индекс страницы поиска на HH
               }

        req = get(self.url, params=par)  # Посылаем запрос к API
        data = req.json()  # Декодируем его ответ, чтобы Кириллица отображалась корректно
        # проверка на наличие данных на странице
        if  data.get('items',{})[0].get('id') is not None:
            self.list.append(data)
        req.close()
        return data


    def get_vacancies(self):
        """переноса агруженных данных в файл json"""

        for page in range(0, self.pages):

            # Преобразуем текст ответа запроса в справочник Python
            r_page = self.get_page(page)

            # Проверка на наличие данных на странице
            if r_page.get('items',{})[0].get('id') is None:
                break



            # Необязательная задержка, но чтобы не нагружать сервисы hh, оставим. 5 сек мы может подождать
            time.sleep(0.5)

        # Создаем новый документ, записываем в него ответ запроса, после закрываем
        f = open(self.file, mode='w', encoding='utf8')
        f.write(json.dumps(self.list, ensure_ascii=False))
        f.close()


        print('Вакансии HeadHunter сохранены в файл')
        return json.dumps(self.list, ensure_ascii=False)


