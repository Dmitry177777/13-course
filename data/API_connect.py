import json
import os
# import datetime
from abc import ABC, abstractmethod
import time
from requests import get, post, put, delete
from operator import *
# import isodate



class Engine(ABC):
    @abstractmethod
    def get_vacancies(self):
        pass

    # @staticmethod
    # def get_connector(file_name):
    #     """ Возвращает экземпляр класса Connector """
    #     pass

class Vacancy ():
    """"Класс Vacancy"""

    list = []

    def __init__(self, platforms,search_query,top_n):

        self.platforms = platforms  # платформа 1 - "HeadHunter", 2- "SuperJob", 3 - "HeadHunter"+"SuperJob"
        self.search_query =search_query #  поисковый запрос
        self.top_n = top_n # количество вакансий для вывода
        self.vacancy = self.get_vacancies()


        # self.platforms = platform # платформа ["HeadHunter", "SuperJob"]
        # self.profession = '' # название вакансии
        # self.candidat = '' # 	Требования к кандидату
        # self.work = '' # Должностные обязанности
        # self.compensation = '' # Условия работы
        # self.profession_url = '' # ссылка на вакансию
        # self.payment_from = None #Сумма оклада от
        # self.payment_to =None #Сумма оклада до
        # self.currency = '' # Валюта. Список возможных значений:  rub — рубль  uah — гривна  uzs — сум
        pass

    def get_vacancies(self):

        if self.platforms in [1, 3]: # загрузка платформы 1 - "HeadHunter"
            hh_vacancy = HeadHunterAPI(self.search_query,self.top_n)
            file1 = hh_vacancy.file
            f= open(file1, mode='r', encoding='utf-8')
            data = json.load(f)
            f.close()
            for i in data:
                self.list.append({"platforms":"HeadHunter", # платформа ["HeadHunter", "SuperJob"]
                             "profession":i.get('items',{})[0].get("name"), # название вакансии
                             "candidat":i.get('items',{})[0].get("snippet",{}).get("requirement"), # 	Требования к кандидату
                             "work": i.get('items',{})[0].get("snippet",{}).get("responsibility"), # Должностные обязанности
                             "compensation": i.get('items',{})[0].get("working_days"), # Условия работы
                             "profession_url":i.get('items',{})[0].get("url"), # ссылка на вакансию
                             "payment_from":i.get('items',{})[0].get("salary",{}).get("from"), #Сумма оклада от
                             "payment_to":i.get('items',{})[0].get("salary",{}).get("to"), #Сумма оклада до
                             "currency":i.get('items',{})[0].get("salary",{}).get("currency") # Валюта. Список возможных значений:  rub — рубль  uah — гривна  uzs — сум
                             })



        if self.platforms in [2, 3]: # загрузка платформы 2- "SuperJob"
            sj_vacancy = SuperJobAPI(self.search_query,self.top_n)
            file2 = sj_vacancy.file
            f = open(file2, mode='r', encoding='utf-8')
            data = json.load(f)
            f.close()
            for i in data:
                self.list.append({"platforms": "SuperJob", # платформа ["HeadHunter", "SuperJob"]
                             "profession": i.get('objects',{})[0].get("profession"), # название вакансии
                             "candidat": i.get('objects',{})[0].get("candidat"), # 	Требования к кандидату
                             "work": i.get('objects',{})[0].get("work"), # Должностные обязанности
                             "compensation": i.get('objects',{})[0].get("compensation"), # Условия работы
                             "profession_url": i.get('objects',{})[0].get("profession_url"), # ссылка на вакансию
                             "payment_from": i.get('objects',{})[0].get("payment_from"), #Сумма оклада от
                             "payment_to": i.get('objects',{})[0].get("payment_to"), #Сумма оклада до
                             "currency": i.get('objects',{})[0].get("currency") # Валюта. Список возможных значений:  rub — рубль  uah — гривна  uzs — сум
                             })

        sorted(self.list, reverse=True, key= itemgetter ("payment_to"))

        return self.list



class SuperJobAPI (Engine):
    """"Класс SuperJobAPI"""
    list = []

    def __init__(self, vacancy, top_n):
        self.vacancy = vacancy
        self.file = '../data/get_SJ.json'
        self.url = 'https://api.superjob.ru/2.0/vacancies'
        self.pages = top_n
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
        data = req.content.decode()  # Декодируем его ответ, чтобы Кириллица отображалась корректно
        req.close()
        return data

    def get_vacancies(self):
        """переноса агруженных данных в файл json"""

        for page in range(0, self.pages):

            # Преобразуем текст ответа запроса в справочник Python
            r_page = json.loads(self.get_page(page))
            self.list.append(r_page)

            # Сохраняем файлы в папку {путь до текущего документа со скриптом}\docs\pagination
            # Определяем количество файлов в папке для сохранения документа с ответом запроса
            # Полученное значение используем для формирования имени документа

            # Проверка на последнюю страницу, если вакансий меньше 2000
            # if (r_page['pages'] - page) <= 1:
            #     break

            # Необязательная задержка, но чтобы не нагружать сервисы hh, оставим. 5 сек мы может подождать
            time.sleep(0.5)

        # Создаем новый документ, записываем в него ответ запроса, после закрываем
        f = open(self.file, mode='w', encoding='utf8')
        f.write(json.dumps(self.list, ensure_ascii=False))
        f.close()

        print('Старницы поиска собраны')
        return json.dumps(self.list, ensure_ascii=False)


class HeadHunterAPI (Engine):
    """"Класс HeadHunterAPI"""
    list = []

    def __init__(self, vacancy, top_n):
        self.vacancy = vacancy
        self.file = '../data/get_HH.json'
        self.url ='https://api.hh.ru/vacancies'
        self.pages = top_n
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
        data = req.content.decode()  # Декодируем его ответ, чтобы Кириллица отображалась корректно
        req.close()
        return data


    def get_vacancies(self):
        """переноса агруженных данных в файл json"""

        for page in range(0, self.pages):

            # Преобразуем текст ответа запроса в справочник Python
            r_page = json.loads(self.get_page(page))
            self.list.append(r_page)

            # Сохраняем файлы в папку {путь до текущего документа со скриптом}\docs\pagination
            # Определяем количество файлов в папке для сохранения документа с ответом запроса
            # Полученное значение используем для формирования имени документа

            # Проверка на последнюю страницу, если вакансий меньше 2000
            if (r_page['pages'] - page) <= 1:
                break

            # Необязательная задержка, но чтобы не нагружать сервисы hh, оставим. 5 сек мы может подождать
            time.sleep(0.5)

        # Создаем новый документ, записываем в него ответ запроса, после закрываем
        f = open(self.file, mode='w', encoding='utf8')
        f.write(json.dumps(self.list, ensure_ascii=False))
        f.close()


        print('Старницы поиска собраны')
        return json.dumps(self.list, ensure_ascii=False)


