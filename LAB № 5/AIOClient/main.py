import json

from aiohttp import web

import aiohttp
import asyncio

import argparse

format_date = "%d.%m.%Y"

import datetime
import csv
import re

'''
session.get('http://localhost:8080/labs/')
session.get('http://localhost:8080/labs/{name_lab}')
session.post('http://localhost:8080/labs')
session.put('http://localhost:8080/labs/{name_lab}')
session.put('http://localhost:8080/labs/{name_lab}/')
session.delete('http://localhost:8080/labs/{name_lab}')
'''

class Data:
    code_operation = 0
    name_lab = ''
    param2 = 1
    location = ''

def get_all_labs(session):
    async with session.get('http://localhost:8080/labs/') as response:
        print("Status:", response.status)
        print("Content-type:", response.headers['content-type'])
        if response.status == 200:
            jsonDate = await response.json()
            print(data.name_lab, ": ", jsonDate, "...")

def get_concrete_lab(session):
    data.name_lab = input(
        "Введите имя лабораторной работы, для которой требуется вывести информацию или слово 'location' для работы с последней созданной: ")

    if data.name_lab != 'location':
        data.location = 'http://localhost:8080/labs/' + str(data.name_lab)

    async with session.get(data.location) as response:
        print("Status:", response.status)
        print("Content-type:", response.headers['content-type'])
        if response.status == 200:
            jsonDate = await response.json()
            print(data.name_lab, ": ", jsonDate, "...")

def post_request(session):
    async with session.post('http://localhost:8080/labs') as response:
        print("Status:", response.status)
        print("Content-type:", response.headers['content-type'])
        print("Location:", response.headers['location'])
        data.location = response.headers['location']
        if response.status == 200:
            jsonDate = await response.json()
            print(data.name_lab, ": ", jsonDate, "...")

def put_request_add(session):
    data.name_lab = input(
        "Введите имя лабораторной работы, для которой требуется вывести информацию или слово 'location' для работы с последней созданной: ")
    if data.name_lab != 'location':
        data.location = 'http://localhost:8080/labs/' + str(data.name_lab)

    params = create_change_dict()
    if len(params) == 0 or params is None:
        return

    async with session.put(data.location, data=json.dumps(params)) as response:
        print("Status:", response.status)
        print("Content-type:", response.headers['content-type'])
        if response.status == 200:
            jsonDate = await response.json()
            print(data.name_lab, ": ", jsonDate, "...")

def put_request_overwrite(session):
    data.name_lab = input(
        "Введите имя лабораторной работы, для которой требуется вывести информацию или слово 'location' для работы с последней созданной: ")
    if data.name_lab != 'location':
        data.location = 'http://localhost:8080/labs/' + str(data.name_lab)

    params = create_change_dict()
    if len(params) == 0 or params is None:
        return

    async with session.put(data.location + '/', data=json.dumps(params)) as response:
        print("Status:", response.status)
        print("Content-type:", response.headers['content-type'])
        if response.status == 200:
            jsonDate = await response.json()
            print(data.name_lab, ": ", jsonDate, "...")

def del_all_labs(session):
    data.name_lab = input(
        "Введите имя лабораторной работы, для которой требуется удалить информацию или слово 'location' для работы с последней созданной: ")
    if data.name_lab != 'location':
        data.location = 'http://localhost:8080/labs/' + str(data.name_lab)

    FLAG0 = input("Требуется ли удалить полностью лабораторную работу?"
                  "(Y[Yes, Да], N[No, Нет]): ")

    if FLAG0 in ['Y', 'Yes', 'Да', 'да']:
        async with session.delete(data.location) as response:
            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])
            if response.status == 200:
                jsonDate = await response.json()
                print(data.name_lab, ": ", jsonDate, "...")
    else:
        params = del_dict()

        if len(params) == 0 or params is None:
            return

        async with session.delete(data.location, data=json.dumps(params)) as response:
            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])
            if response.status == 200:
                jsonDate = await response.json()
                print(data.name_lab, ": ", jsonDate, "...")

def export_all_labs(session):
    async with session.get('http://localhost:8080/labs/') as response:
        print("Status:", response.status)
        print("Content-type:", response.headers['content-type'])
        if response.status == 200:
            jsonDate = await response.json()
            STUDENT_LAB = dict()
            with open("student_result_all.csv", 'w', newline='') as csv_file:  # auto clouse()
                field = ["Ф. И. О студента"]
                writer = csv.writer(csv_file, dialect='excel', delimiter=";")
                for lab_name in jsonDate.keys():
                    field_lab = lab_name + ' [' + jsonDate[lab_name]["DeadLine"]
                    if "Description" in jsonDate[lab_name].keys():
                        field_lab += ', ' + jsonDate[lab_name]["Description"]
                    field_lab += ']'
                    field.append(field_lab)  # len

                    if "Students" in jsonDate[lab_name].keys():
                        for student in jsonDate[lab_name]["Students"]:
                            if student not in STUDENT_LAB:
                                STUDENT_LAB[student] = [student, len(field) - 1]  # Ф. И. О.
                            else:
                                STUDENT_LAB[student].append(len(field) - 1)
                writer.writerow(field)
                for student in STUDENT_LAB.keys():
                    writer.writerow(STUDENT_LAB[student])

def export_concrete_lab(session):
    data.name_lab = input(
        "Введите имя лабораторной работы, для которой требуется вывести информацию или слово 'location' для работы с последней созданной: ")
    if data.name_lab != 'location':
        data.location = 'http://localhost:8080/labs/' + str(data.name_lab)
    async with session.get(data.location) as response:
        print("Status:", response.status)
        print("Content-type:", response.headers['content-type'])
        if response.status == 200:
            jsonDate = await response.json()
            print(data.name_lab, ": ", jsonDate, "...")
            with open("student_result.csv", 'w', newline='') as csv_file:  # auto clouse()
                writer = csv.writer(csv_file, dialect='excel', delimiter=";")
                field_lab = data.name_lab + ' [' + jsonDate["DeadLine"]
                if "Description" in jsonDate.keys():
                    field_lab += ', ' + jsonDate["Description"]
                field_lab += ']'
                field = ["Ф. И. О студента", field_lab]
                writer.writerow(field)
                if "Students" in jsonDate.keys():
                    for student in jsonDate["Students"]:
                        writer.writerow([student, re.findall(r'\d+', data.name_lab)[0]])

async def Handler(data: Data):
    async with aiohttp.ClientSession() as session:
        match data.code_operation:
            case 0:
                get_help()
            case 1:  # get-all
                print("Description:", "Get all data all lab")
                get_all_labs(session)
            case 2:  # get-concrete_lab
                print("Description:", "Get data concrete lab")
                get_concrete_lab(session)
            case 3:  # post +
                print("Description:", "Create lab!")
                post_request(session)
            case 4:  # put add
                print("Description:", "Add data in lab(s)")
                put_request_add(session)
            case 5:  # put overwrite
                print("Description:", "Overwrite lab(s)")
                put_request_overwrite(session)
            case 6:  # delele
                print("Description:", "delele lab(s)")
                del_all_labs(session)
            case 7:  # export_all
                print("Description:", "Export all lab")
                export_all_labs(session)
            case 8:  # export_concrete-lab
                print("Description:", "Export concrete lab")
                export_concrete_lab(session)
            case _:
                print("Для введенного кода команды не определены. Подромнее смотрите в справку[Код: 0]")

def get_help():
    print(''' 
        Программа-клиент для работы с лабораторными работами на сервере.
        version: 1.0
        Описание кодов операций:
        0 - Справка.
        1 - Получение всей информации с сервера по всем лабараторным работам.
        2 - Получение информации по конкретной лабораторной работе.
        3 - Создание лабораторной работы.
        4 - Изменение лабораторной работы (Добавление данных) .
        5 - Изменение лабораторной работы (Перезапись данных).
        6 - Удаление данных лабораторной работы.
        7 - Экспорт всех лабораторных работ в csv-файл.
        8 - Экспорт конкретной лабораторной работы в csv-файл.
        exit/quit - выход из программы.
        ''')

def validDate(date) -> bool:
    try:
        datetime.datetime.strptime(date, format_date)
        return True  # Дата соответствует формату
    except ValueError:
        return False  # Дата не соответствует формату


def create_change_dict() -> dict:
    FLAG1 = input("Требуется ли для данной лабораторной работы создавать/изменить время дедлайна? "
                  "(Y[Yes, Да], N[No, Нет]): ")
    if FLAG1 in ['Y', 'Yes', 'Да', 'да']:
        while True:
            DeadLine = input("Введите дату дедлайна в формате DD.MM.YYYY:")
            if validDate(DeadLine):
                break
        FLAG1 = True
    else:
        FLAG1 = False
    FLAG2 = input("Требуется ли для данной лабораторной работы создавать/изменить/удалять описание? "
                  "(Y[Yes, Да], N[No, Нет]): ")
    if FLAG2 in ['Y', 'Yes', 'Да']:
        Description = input("Введите описание лабораторной работы: ")
        FLAG2 = True
    else:
        FLAG2 = False
    FLAG3 = input("Требуется ли для данной лабораторной работы создавать/изменить/удалять"
                  " список студентов ? (Y[Yes, Да], N[No, Нет]): ")
    if FLAG3 in ['Y', 'Yes', 'Да']:
        Students = input("Введите через запятую студентов: ")
        Students = Students.replace("'", "").split(",")
        FLAG3 = True
    else:
        FLAG3 = False

    dict1 = dict()

    if FLAG1:
        dict1["DeadLine"] = DeadLine
    if FLAG2:
        dict1["Description"] = Description
    if FLAG3:
        dict1["Students"] = Students

    return dict1


def del_dict() -> dict:
    FLAG2 = input("Требуется ли для данной лабораторной работы удалять описание? "
                  "(Y[Yes, Да], N[No, Нет]): ")
    if FLAG2 in ['Y', 'Yes', 'Да']:
        # Description = input("Введите описание лабораторной работы: ")
        FLAG2 = True
    else:
        FLAG2 = False
    FLAG3 = input("Требуется ли для данной лабораторной работы удалять"
                  " список студентов полностью? (Y[Yes, Да], N[No, Нет]): ")
    #FLAG4 = False
    if FLAG3 in ['Y', 'Yes', 'Да']:
        FLAG3 = True
    else:
        FLAG3 = False
        '''FLAG4 = input("Требуется ли для данной лабораторной работы удалять"
                      " часть студентов из списка? (Y[Yes, Да], N[No, Нет]): ")
        if FLAG4 in ['Y', 'Yes', 'Да']:
            Students = input("Введите через запятую студентов, которых требуется удалить: ").replace("'", '" ').split(',')
            FLAG4 = True
        else:
            FLAG4 = False'''

    list1 = list()

    if FLAG2:
        list1.append("Description")
    if FLAG3:
        list1.append("Students")
    '''elif FLAG4:
        dict1.add({"Students": Students})'''

    return list1


if __name__ == "__main__":
    print("Start client!")

    data = Data()

    while True:
        print('Введите код операции(Справка - код[0])')
        input_data = input("Client >> ")

        if input_data in ['exit', 'quit']:
            break

        if input_data.split(' ')[0].isdigit():
            data.code_operation = int(input_data.split(' ')[0])

        if len(input_data.split(' ')) > 1:
            data.name_lab = input_data.split(' ')[1]

        loop = asyncio.get_event_loop()
        loop.run_until_complete(Handler(data))

    print("Close client!")
