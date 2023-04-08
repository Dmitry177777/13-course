import json
import os
# import datetime
from abc import ABC, abstractmethod

from requests import get, post, put, delete

# import isodate

class Engine(ABC):
    @abstractmethod
    def get_request(self):
        passpandas

    @staticmethod
    def get_connector(file_name):
        """ Возвращает экземпляр класса Connector """
        pass

class SuperJobAPI (Engine):
    """"Класс HH"""

    def __init__(self,  https_id='https://api.hh.ru//'):
        self.https_id = https_id
        self.response = HeadHunterAPI.get_service(https_id)
    pass


    @staticmethod
    def get_service(https):
        # API_KEY скопирован из гугла и вставлен в переменные окружения
        # api_key: str = os.getenv('API_KEY')

        response = get(https)

        return response

    def get_request(self):
        pass


class HeadHunterAPI (Engine):
    """"Класс HH"""

    def __init__(self,  https_id='https://api.hh.ru//'):
        self.https_id = https_id
        self.response = HeadHunterAPI.get_service(https_id)

        # number_of_pages = 100
        # # number_of_ads = number_of_pages * per_page
        # job_title = ["'Data Analyst' and 'data scientist'"]
        # for job in job_title:
        #     data = []
        #
        #     for i in range(number_of_pages):
        #         url = 'https://api.hh.ru/vacancies'
        #         par = {'text': job, 'area': '113', 'per_page': '10', 'page': i}
        #         r = get(url, params=par)
        #         e = r.json()
        #         data.append(e)
        #         #vacancy_details = data[0]['items'][0].keys()
        # self.data = data

        # self.channel = hh.channels().list(id=channel_id, part='snippet,statistics').execute()

        # par = {'per_page': '10', 'page': i}
        # requests.get(self.url, params=par)

        # self.kind = self.channel.get ('kind') # kind
        # #self.url = self.channel.get ("etag") # etag
        # self.pageInfo = self.channel.get ("pageInfo") # pageInfo
        # self.items = self.channel.get("items")  # items
        #
        # self.channel_id = channel_id # - id канала
        # self.title = self.channel.get('items',{})[0].get('snippet',{}).get('title')  # - название канала
        # self.description = self.channel.get('items',{})[0].get('snippet',{}).get('description') # - описание канала
        # self.url = f'https://www.youtube.com/channel/{channel_id}'   # - ссылка на канал
        # self.subscriberCount = self.channel.get('items',{})[0].get('statistics',{}).get('subscriberCount')  # - количество подписчиков
        # self.video_count = self.channel.get('items',{})[0].get('statistics',{}).get('videoCount') # - количество видео
        # self.viewCount = self.channel.get('items',{})[0].get('statistics',{}).get('viewCount')  # - общее количество просмотров
        # Channel.to_json(self)





    pass

    @staticmethod
    def get_service(https):
        # API_KEY скопирован из гугла и вставлен в переменные окружения
        # api_key: str = os.getenv('API_KEY')

        response = get(https)

        return response


    def get_request(self):
        pass


    def __repr__(self):
        return f'Channel({self.title}, {self.video_count},{self.viewCount},{self.subscriberCount})'

    def __str__(self):
        return f'Youtube-канал: {self.title}'

    def __add__(self, other):
        count = self.subscriberCount + other.subscriberCount
        return print(f'{count}')

    def __gt__(self, other):
        A = int(self.subscriberCount)
        B = int(other.subscriberCount)

        return print(f'{(A > B)}')

    def __lt__(self, other):
        A = int(self.subscriberCount)
        B = int(other.subscriberCount)

        return print(f'{(A < B)}')


    @property
    def channel_id(self):
        pass
    @channel_id.setter
    def channel_id(self, new_id):
        return print(f"AttributeError: property 'channel_id' of 'Channel' object has no setter")

    def to_json(self, file):
        """Метод переноса атрибутов класса в файл json"""

        to_json = {
            'kind': self.kind,
            #'url': access_template,
            'pageInfo': self.pageInfo,
            'items': self.items,
            'channel_id': self.channel_id,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'subscriberCount': self.subscriberCount,
            'video_count': self.video_count,
            'viewCount': self.viewCount
            }

        with open(file, 'w') as f:
            f.write(json.dumps(to_json))

        pass



    def print_info (self):
        """Метод вывода данных о канале"""
        self.log = json.dumps(self.channel, indent=2, ensure_ascii=False)

        return self.log

