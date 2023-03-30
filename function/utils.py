
from data.classes import HH
from requests import get, post, put, delete

# response = get ('https://api.hh.ru/')
# print(response)

hh = HH('https://api.hh.ru/')
print (hh.response.text)