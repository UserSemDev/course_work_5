import psycopg2


class DBManager:
    """Класс для работы с БД PostgreSQL"""

    def __init__(self, bd_name: str, params: dict) -> None:
        self.bd_name = bd_name
        self.params = params

    def bd_connect(self, query: str = None):
        """Метод подключения к БД"""
        try:
            conn = psycopg2.connect(dbname=self.bd_name, **self.params)
            with conn.cursor() as cur:
                cur.execute(query)
                result = cur.fetchall()
                for num, i in enumerate(result, 1):
                    print(f"{num}: {i}")
            conn.close()
        except Exception:
            print(f"Ошибка подключения к базе данных. Проверьте корректность данных.")

    def get_companies_and_vacancies_count(self):
        """Получение списка всех компаний и количества вакансий у каждой компании"""
        sql_query = ("""SELECT employers.company_name, COUNT(*) as count_vacancy
                        FROM vacancies
                        JOIN employers USING(employer_id)
                        GROUP BY employers.company_name
                        ORDER BY count_vacancy DESC""")
        self.bd_connect(sql_query)

    def get_all_vacancies(self):
        """Получение списка всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию."""
        sql_query = ("""SELECT employers.company_name, vacancy_name, salary_from, salary_to, valuta, vacancy_url 
                        FROM vacancies
                        JOIN employers USING(employer_id)""")
        self.bd_connect(sql_query)

    def get_avg_salary(self):
        """Получение средней зарплаты по вакансиям."""
        sql_query = ("""SELECT AVG(COALESCE((salary_from + salary_to) / 2, salary_from, salary_to)) AS avg_salary 
                        FROM vacancies""")
        self.bd_connect(sql_query)

    def get_vacancies_with_higher_salary(self):
        """Получение списка всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        sql_query = ("""SELECT * FROM vacancies
                        WHERE COALESCE((salary_from + salary_to) / 2, 
                                        salary_from, 
                                        salary_to) > 
                                        (SELECT AVG(COALESCE((salary_from + salary_to) / 2, 
                                                              salary_from, 
                                                              salary_to)) 
                                        FROM vacancies)
                        ORDER BY  COALESCE((salary_from + salary_to) / 2, salary_from, salary_to) DESC""")
        self.bd_connect(sql_query)

    def get_vacancies_with_keyword(self, keyword: str) -> None:
        """Получение списка всех вакансий, в названии которых содержатся переданные в метод слова, например python."""
        sql_query = (f"""SELECT * FROM vacancies
                        WHERE vacancy_name LIKE '%{keyword}%'
                        """)
        self.bd_connect(sql_query)
