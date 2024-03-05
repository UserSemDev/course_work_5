import random
import re
import time
import requests


class HeadHunterAPI:

    def __init__(self):
        self.employers_vacancies = []

    def get_data_employers(self, employers_name: list) -> list[dict]:
        """
        Получение информации о работодателях и вакансиях
        :param employers_name: список названий работодателей
        :return: список словарей с информацией о работодателях и их вакансиях
        """

        url = 'https://api.hh.ru/employers/'
        params = {
            "text": None,
            "only_with_vacancies": True,
            "sort_by": "by_vacancies_open"
        }

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/120.0.0.0 Safari/537.36"
        }

        for emp_name in employers_name:
            params["text"] = emp_name
            response = requests.get(url=url, params=params, headers=headers)
            if response:
                employer = response.json()['items']
                employer_id = employer[0]['id']
                resp = requests.get(url=url + employer_id, headers=headers)
                data = resp.json()
                name = data['name']
                description = re.search(r'(?<=<p>)(.+?)(?=</p>)', data['description'])[0]
                site_url = data['site_url']
                area = data['area']['name']
                open_vacancies = data['open_vacancies']

                print(f"\nПолучаем вакансии работодателя: {name}")

                employer_vacancy = self.get_data_vacancies_employer(employer_id)

                data_employer = {
                    "id": employer_id,
                    "name": name,
                    "open_vacancies": open_vacancies,
                    "area": area,
                    "site_url": site_url,
                    "description": description,
                    "vacancies": employer_vacancy
                }
                self.employers_vacancies.append(data_employer)
        return self.employers_vacancies

    @staticmethod
    def get_data_vacancies_employer(id_employer: int) -> list[dict]:
        """
        Получение списка вакансий работодателя
        :return: список вакансий работодателя
        """
        url = 'https://api.hh.ru/vacancies/'
        params = {
            "employer_id": id_employer,
            "only_with_salary": True,
            "per_page": 100,
            "page": 0
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/120.0.0.0 Safari/537.36"
        }

        employer_vacancy = []
        while True:
            response = requests.get(url=url, params=params, headers=headers)
            if response:
                resp = response.json()
                items = resp['items']
                page = resp['page']
                pages = resp['pages']
                for item in items:
                    job_vacancy = HeadHunterAPI.get_params_vacancy(item)
                    employer_vacancy.append(job_vacancy)

                print(f'Загружены вакансии. Страница {page + 1} из {pages}')

                if page == pages - 1:
                    break
                params['page'] = params.get('page') + 1
                random_time = random.uniform(0.2, 0.4)
                time.sleep(random_time)

        print(f"Получено вакансий: {len(employer_vacancy)}")

        return employer_vacancy

    @staticmethod
    def get_params_vacancy(job_item: dict) -> dict:
        """
        Метод получающий параметры вакансии и возвращающий словарь
        :param job_item: json словарь полученный от API с вакансией
        :return: возвращает словарь с вакансией
        """
        id_vacancy = int(job_item['id'])
        name = job_item['name']
        salary_from = job_item['salary']['from']
        salary_to = job_item['salary']['to']
        currency = 'BYN' if job_item['salary']['currency'].upper() == 'BYR' else job_item['salary'][
            'currency'].upper()
        experience = job_item.get('experience').get('name')
        area = job_item.get('area').get('name')
        alternate_url = job_item.get('alternate_url')

        data = {"id": id_vacancy,
                "name": name,
                "salary_from": salary_from,
                "salary_to": salary_to,
                "currency": currency,
                "experience": experience,
                "area": area,
                "url_vacancy": alternate_url}

        return data
