import argparse
import tempfile
import json
import os

parser = argparse.ArgumentParser(
                    prog='storage',
                    description='...',
                    epilog='Text')

parser.add_argument('-k', '--key')
parser.add_argument('-v', '--val')

args = parser.parse_args()
print(args.key, args.val, sep=': ')

filename = "storage.data"

if args.val == None:                                                # Если отсутствует значение аргумента --val
    print("Чтение")
    d = 'r'
    with open(filename, d, encoding='utf-8') as f:                  # Открываем файл на чтение
        data = json.load(f)                                         # Считываем данные
        # print(data)
        if  args.key not in data.keys():                            # Если ключа нет в словаре
            print("None")                                           # Выводим соответствующее сообщение на консоль
        elif isinstance(data[args.key], list):                      # Иначе если тип значения по ключу является списком(list)
            print(", ".join(data[args.key]))                        # преобразуем этот список в строку и выводим на печать
        else:                                                       # Иначе
            print(data[args.key])                                   # Печатаем значение на экран
else:
    print("Запись")
    data = {}
    if os.path.isfile(filename):
        file_size = os.stat(filename)                               # Узнаем размер файла
        # print(file_size.st_size)
        if file_size.st_size != 0:                                  # Если файл не пуст
            d = 'r+'
            with open(filename, d, encoding='utf-8') as f:          # открываем файл на загрузку данных из него
                data = json.load(f)                                 # Загружаем данные
                #print(data)
            # with автоматически закрывает файл
            # после выхода из соответствующего уровня
            # поэтому нам нет необходимости писать file.close()
    d = 'w+'
    with open(filename, d, encoding='utf-8') as f:                  # Открываем снова файл на перезапись.
                                                                    # Старые данные удалятся!
        if  args.key not in data.keys():                            # Если ключа нет в словаре
            data[args.key] = args.val                               # добавляем в словарь значение {key: val}
        else:                                                       # Иначе
            if isinstance(data[args.key], list):                    # Если тип значения по ключу является списком(list)
                data.setdefault(args.key, []).append(args.val)      # Добавляем в этот список с конца новое значение.
            else:
                data[args.key] = list([data[args.key], args.val])   # Изменяем значения и тип по ключу.
        # print(data)
        json.dump(data, f, ensure_ascii=False, indent=4)            # Записывыем данные в файл.



