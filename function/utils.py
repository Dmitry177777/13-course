
from data.API_connect import HeadHunterAPI, SuperJobAPI
from requests import get, post, put, delete

# response = get ('https://api.hh.ru/')
# print(response)

# Создание экземпляра класса для работы с API сайтов с вакансиями
# hh_api = HeadHunterAPI()
# superjob_api = SuperJobAPI()

# # Получение вакансий с разных платформ
# hh_vacancies = HeadHunterAPI("Python")
superjob_vacancies = SuperJobAPI("Python")
print (superjob_vacancies.job_list)


# # Создание экземпляра класса для работы с API сайтов с вакансиями
# hh_api = HeadHunterAPI()
# superjob_api = SuperJobAPI()
#
# # Получение вакансий с разных платформ
# hh_vacancies = hh_api.get_vacancies("Python")
# superjob_vacancies = superjob_api.get_vacancies("Python")
#
# # Создание экземпляра класса для работы с вакансиями
# vacancy = Vacancy("Python Developer", "<https://hh.ru/vacancy/123456>", "100 000-150 000 руб.", "Требования: опыт работы от 3 лет...")
#
# # Сохранение информации о вакансиях в файл
# json_saver = JSONSaver()
# json_saver.add_vacancy(vacancy)
# json_saver.get_vacancies_by_salary("100 000-150 000 руб.")
# json_saver.delete_vacancy(vacancy)
#
#
#
#
# if __name__ == "__main__":
#     user_interaction()