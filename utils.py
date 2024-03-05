import psycopg2


def create_database(database_name: str, params: dict):
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE employers (
                employer_id INT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                open_vacancies INTEGER,
                city VARCHAR(50),
                site_url TEXT,
                description TEXT    
            )
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vacancies (
                vacancy_id INT PRIMARY KEY,
                employer_id INT REFERENCES employers(employer_id),
                title VARCHAR(255) NOT NULL,
                salary_from INT,
                salary_to INT,
                currency VARCHAR(3),
                experience VARCHAR(50),
                city VARCHAR(50),
                vacancy_url TEXT 
            )
        """)
    conn.commit()
    conn.close()


def save_data_to_database(data: list, database_name: str, params: dict):
    conn = psycopg2.connect(dbname=database_name, **params)
    with conn.cursor() as cur:
        for employer in data:
            cur.execute("""
                INSERT INTO employers (employer_id, title, open_vacancies, city, site_url, description)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                        (employer['id'], employer['name'], employer['open_vacancies'], employer['area'],
                            employer['site_url'], employer['description'])
                        )
            for vacancy in employer['vacancies']:
                cur.execute("""
                    INSERT INTO vacancies (vacancy_id, employer_id, title, salary_from, salary_to, currency, experience,
                    city, vacancy_url)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (vacancy['id'], employer['id'], vacancy['name'], vacancy['salary_from'], vacancy['salary_to'],
                          vacancy['currency'], vacancy['experience'], vacancy['area'], vacancy['url_vacancy'])
                            )
    conn.commit()
    conn.close()

