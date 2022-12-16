# Операции обработки данных
# Создание, Чтение, Изменение, Удаление
import os
import functools
from tinydb import TinyDB, Query
from datetime import datetime
import logger as log
import logging
global db, logger

logger = log.init(__name__)
db = TinyDB('db.json', ensure_ascii=False, encoding='utf-8')

employees = db.table("Employees")
query = Query()


def init_db():
    logger.info(f"init db...")
    db.table("Employees")
    # db.table("Department")


info = lambda message: to_log(message)


def to_log(message, level=logging.INFO):
    if level == logging.ERROR:
        logger.error(message)
    else:
        logger.info(message)
    return message



def import_employee(data):
    error = ""
    if not data:
        error = info(f"нет данных для импорта")

    if employees.contains(query.fullname == data[0]):
        error = info(f"!! Сотрудник {data[0]} с похожим ФИО уже существует в системе !!")

    employee = {
        "fullname": data[0],
        "birthDate": data[1],
        "jobPosition": data[2],
        "department": data[3],
        "tel": data[4],
        "email": data[5],
        "status": data[6],
        "history": [f"{datetime.today().strftime('%Y-%m-%d %H:%M:%S')} Импорт из файла {list(data)}"]
    }

    if error == "":
        id_rec = employees.insert(employee)
        print(info(f"Запись успешно добавлена, ID:{id_rec}"))
    else:
        print(error)


def add_employee(data):
    error = ""
    try:
        error = info(f"params({data})")
        employee = {
            "fullname": data[0],
            "birthDate": data[1],
            "jobPosition": data[2],
            "department": data[3],
            "tel": data[4],
            "email": data[5],
            "status": "Работает",
            "history": [f"{datetime.today().strftime('%Y-%m-%d %H:%M:%S')} "
                        f"Принят на работу в отдел {data[3]} на позицию {data[2]}"]
        }
        if employees.contains(query.fullname == data[0]):
            error = info(f"!! Сотрудник {data[0]} с похожит ФИО уже существует в системе !!")

        if error == "":
            employees.insert(employee)
        else:
            print(error)
    except Exception as e:
        logger.exception(e, exc_info=True)


test_contains = lambda value, search: search in value


def employee_matching_all(**query):
    q = Query()
    return employees.search(functools.reduce(lambda x, y: x | y,
                                             [getattr(q, k).test(test_contains, str(v))
                                              for k, v in query.items()]))


def all_employee():
    return employees.all()


def transfer_employee(data):
    if not data:
        return

    toDept = input("Укажите новый отдел: ")
    history = data["history"]
    history.append(f"{datetime.today().strftime('%Y-%m-%d %H:%M:%S')}"
                   f"Перевод из отдела {data['department']}  на позицию {toDept}")

    result = employees.update({"department": toDept, "history": history}, doc_ids=[data.doc_id])

    if result:
        print("Перевод по компании успешно проведен")


def vacation_employee(data):
    if not data:
        return
    vacationDate = input("Укажите дату окончания отпуска: ")
    history = data["history"]
    history.append(f"{datetime.today().strftime('%Y-%m-%d %H:%M:%S')}"
                   f"Плановый отпуск с {datetime.today().strftime('%Y-%m-%d')} по {vacationDate}")

    result = employees.update({"status": "В отпуске", "history": history}, doc_ids=[data.doc_id])

    if result:
        print("Отпуск успешно проведен")


def sick_employee(data):
    if not data:
        return

    sickDate = input("Укажите дату окончания  больничного: ")
    history = data["history"]
    history.append(f"{datetime.today().strftime('%Y-%m-%d %H:%M:%S')}"
                   f"Больничный с {datetime.today().strftime('%Y-%m-%d')} по {sickDate}")

    result = employees.update({"status": "На больничном", "history": history}, doc_ids=[data.doc_id])
    if result:
        print("Больничный успешно проведен")


def dismissal_employee(data):
    if not data:
        return
    history = data["history"]
    history.append(f"{datetime.today().strftime('%Y-%m-%d %H:%M:%S')}"
                   f"Уволен {datetime.today().strftime('%Y-%m-%d')}")

    result = employees.update({"status": "Уволен", "history": history}, doc_ids=[data.doc_id])
    if result:
        print("Увольнение успешно проведено")


def repeat_employee(data):
    if not data:
        return
    history = data["history"]
    history.append(f"{datetime.today().strftime('%Y-%m-%d %H:%M:%S')}"
                   f"Принят на работу {datetime.today().strftime('%Y-%m-%d')}")

    result = employees.update({"status": "Работает", "history": history}, doc_ids=[data.doc_id])
    if result:
        print("Прием на работу успешно проведено")


def rename_employee(data):
    if not data:
        return

    rename = input("Укажите полное имя: ")
    history = data["history"]
    history.append(f"{datetime.today().strftime('%Y-%m-%d %H:%M:%S')}"
                   f"Переименование с {data['fullname']} на  {rename}")

    result = employees.update({"fullname": rename, "history": history}, doc_ids=[data.doc_id])

    if result:
        print("Переименование сотрудника успешно выполнено")


def ls_change_contacts_employee(data):
    if not data:
        return
    print("Чтобы удалить контакт, укажите значение del")
    tel = input(f"Изменить контактный телефон с {data['tel']} на: ")
    email = input(f"Изменить электронную почту с {data['email']} на: ")

    if tel == "del":
        tel = ""
    elif tel == "":
        tel = data["tel"]

    if email == "del":
        email = ""
    elif tel == "":
        email = data["email"]

    history = data["history"]

    if tel != data["tel"]:
        history.append(f"{datetime.today().strftime('%Y-%m-%d %H:%M:%S')}"
                       f"Изменение контактного телефона с {data['tel']} на {tel}")
    if email != data["email"]:
        history.append(f"{datetime.today().strftime('%Y-%m-%d %H:%M:%S')}"
                       f"Изменение электронной почты с {data['email']} на {email}")

    result = employees.update({"tel": tel, "email": email, "history": history}, doc_ids=[data.doc_id])

    if result:
        print("Изменение контактных данных сотрудника успешно завершено")


def get_by_id(id):
    return employees.get(doc_id=id)
