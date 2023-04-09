import json
import os
# import datetime
from abc import ABC, abstractmethod
import time
from requests import get, post, put, delete

# import isodate

class Engine(ABC):
    @abstractmethod
    def get_vacancies(self, vacancy):
        pass

    # @staticmethod
    # def get_connector(file_name):
    #     """ Возвращает экземпляр класса Connector """
    #     pass

class SuperJobAPI (Engine):
    """"Класс HH"""
    list = []

    def __init__(self, vacancy):
        self.vacancy = vacancy
        self.file = '../data/get_SJ.json'
        self.url = 'https://api.superjob.ru/2.0/vacancies'
        self.pages = 10
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


class HeadHunterAPI (Engine):
    """"Класс HH"""
    list = []

    def __init__(self, vacancy):
        self.vacancy = vacancy
        self.file = '../data/get_HH.json'
        self.url ='https://api.hh.ru/vacancies'
        self.pages = 10
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


