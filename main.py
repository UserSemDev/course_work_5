from config import config, EMPLOYERS_FILE_PATH
from db_class import DBManager
from hh_platforms import HeadHunterAPI
from utils import create_database, save_data_to_database
import os


def get_data_from_api() -> None:
    """
    Функция создает и наполняет БД данными от API
    :return: None
    """
    if os.path.exists(EMPLOYERS_FILE_PATH):
        with open(EMPLOYERS_FILE_PATH, 'r', encoding='UTF-8') as file:
            data_employers = file.read().split(', ')
    else:
        exit("Ошибка! Файл с компаниями не найден!")

    hh = HeadHunterAPI()
    data_employer = hh.get_data_employers(data_employers)

    params = config()
    create_database('hh_base', params)
    save_data_to_database(data_employer, 'hh_base', params)
    print("База данных успешно создана и заполнена данными.")
    answer = input("Хотите продолжить работу с БД:\n"
                   "1 - Да\n"
                   "2 - Нет\n").strip()
    if answer == "1":
        get_data_database()
    else:
        exit("Спасибо за использование приложения. Всего доброго!")


def get_data_database() -> None:
    """
    Функция взаимодействия с пользователей для получения данных и БД
    :return: None
    """
    params = config()
    while True:
        user_answer = input("\nВыберите действие для работы с БД:\n"
                            "1 - Получить список всех компаний и количество вакансий\n"
                            "2 - Получить список всех вакансий с подробной информацией\n"
                            "3 - Получить среднюю зарплату всех вакансий\n"
                            "4 - Получить список всех вакансий с зарплатой выше средней\n"
                            "5 - Получить список вакансий по ключевому слову\n"
                            "6 - Выход\n").strip()
        if user_answer in ["1", "2", "3", "4", "5"]:
            db_manager = DBManager('hh_base', params)
            if user_answer == "1":
                db_manager.get_companies_and_vacancies_count()
            elif user_answer == "2":
                db_manager.get_all_vacancies()
            elif user_answer == "3":
                db_manager.get_avg_salary()
            elif user_answer == "4":
                db_manager.get_vacancies_with_higher_salary()
            elif user_answer == "5":
                answer = input("Введите ключевое слово для фильтрации: ").strip()
                db_manager.get_vacancies_with_keyword(answer)
        elif user_answer == "6":
            exit("Спасибо за использование приложения. Всего доброго!")


def main() -> None:
    """
    Стартовое взаимодействие с пользователем
    :return: None
    """
    while True:
        answer = input("Здравствуйте! Для продолжения выберите действие:\n"
                       "1 - Создать базу данных и наполнить ее данными\n"
                       "2 - Работать с уже существующей БД\n").strip()
        if answer in ["1", "2"]:
            break
    if answer == "1":
        get_data_from_api()
    elif answer == "2":
        get_data_database()
    else:
        exit("Непредвиденная ошибка. Выход.")


if __name__ == '__main__':
    main()
