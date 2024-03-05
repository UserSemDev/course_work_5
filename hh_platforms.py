import random
import re
import time

import requests


class HeadHunterAPI:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36"
    }

    def __init__(self):
        self.employers = []
        self.employers_vacancies = []

    def get_data_employers(self, employers_name: list) -> list[dict]:
        """
        Получение информации о работодателях
        :param employers_name: список названий работодателей
        :return: список словарей с информацией о работодателях
        """

        url = 'https://api.hh.ru/employers/'
        params = {
            "text": None,
            "only_with_vacancies": True,
            "sort_by": "by_vacancies_open"
        }

        for emp_name in employers_name:
            params["text"] = emp_name
            print(f"Получаем информацию о работодателе: {params['text']}")
            response = requests.get(url=url, params=params, headers=self.headers)
            if response:
                employer = response.json()['items']
                employer_id = employer[0]['id']
                resp = requests.get(url=url + employer_id, headers=self.headers)
                data = resp.json()
                name = data['name']
                description = re.search(r'(?<=<p>)(.+?)(?=</p>)', data['description'])[0]
                site_url = data['site_url']
                area = data['area']['name']
                open_vacancies = data['open_vacancies']
                data_employer = {
                    "id": employer_id,
                    "name": name,
                    "open_vacancies": open_vacancies,
                    "area": area,
                    "site_url": site_url,
                    "description": description,
                }
                self.employers.append(data_employer)
        return self.employers

    def get_data_vacancies_employer(self) -> list[dict[list[dict]]]:
        """
        Получение списка вакансий для каждого работодателя
        :return: список работодателей в каждом список вакансий
        """
        url = 'https://api.hh.ru/vacancies/'
        params = {
            "employer_id": None,
            "only_with_salary": True,
            "per_page": 100,
            "page": 0
        }

        for employer in self.employers:
            params['employer_id'] = employer['id']
            employer_vacancy = []
            params['page'] = 0
            print(f"\nПолучаем вакансии работодателя: {employer['name']}")
            while True:
                response = requests.get(url=url, params=params, headers=self.headers)
                if response:
                    resp = response.json()
                    items = resp['items']
                    page = resp['page']
                    pages = resp['pages']
                    for item in items:
                        job_vacancy = self.get_params_vacancy(item)
                        employer_vacancy.append(job_vacancy)
                    print(f'Загружены вакансии. Страница {page + 1} из {pages}')
                    if page == pages - 1:
                        break
                    params['page'] = params.get('page') + 1
                    random_time = random.uniform(0.2, 0.4)
                    time.sleep(random_time)
            self.employers_vacancies.append({employer['id']: employer_vacancy})
            print(f"Получено вакансий: {len(employer_vacancy)}")
        return self.employers_vacancies

    @staticmethod
    def get_params_vacancy(job_item: dict) -> dict:
        """
        Метод получающий параметры вакансии и возвращающий словарь
        :param job_item: json словарь полученный от API с вакансией
        :return: возвращает словарь с вакансией
        """
        id_vacancy = int(job_item['id'])
        name = job_item['name']
        if job_item['salary']:
            currency = 'BYN' if job_item['salary']['currency'].upper() == 'BYR' else job_item['salary'][
                'currency'].upper()
            salary = {"from": job_item['salary']['from'],
                      "to": job_item['salary']['to'],
                      "currency": currency}
        else:
            salary = None
        experience = job_item.get('experience').get('name')
        area = job_item.get('area').get('name')
        alternate_url = job_item.get('alternate_url')
        data = {"id": id_vacancy,
                "name": name,
                "salary": salary,
                "experience": experience,
                "area": area,
                "url_vacancy": alternate_url}
        return data
