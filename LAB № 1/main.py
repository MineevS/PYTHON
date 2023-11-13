# Задача № 1:
def lensort(list):
    return sorted(list, key=len, reverse=False)

print(lensort(['python', 'perl', 'java', 'c',  'haslkell', 'ruby']))

# Задача № 2:
def unique(list):
    return set(list)

print(unique([1, 2, 1, 3,  2, 5]))

# Задача № 3:
def my_enumerate(list_input):
    return list(zip(range(len(list_input), list_input))

print(my_enumerate(["a", "b", "c"]))

# Задача № 4:
from collections import Counter

def file_func(file_name):
    file = open(file_name, "r")
    data = file.readline()
    data1 = []
    for item in data.split(" "):
        data1.append(item)
        
    data1 = dict(Counter(data1))

    for item in data1:
        print(item, data1[item], sep=':')

file_func("data.txt")

# Задача № 5:

import time
from decimal import *
getcontext().clear_flags()
getcontext().prec = 8

def decorator(func):
    def wrapper(*args, **kwargs):
        start_time = Decimal(time.time())
        # print(start_time)
        val = func(*args)
        # print(time.time())
        print("--- %s seconds ---" % (Decimal(time.time()) - start_time))
        return val
    
    return wrapper

@decorator
def func1(list_arg):
    list_output = []
    for x in list_arg:
        list_output.append(x**2)
    return list_output

print(func1(list(range(1, 100))))

@decorator
def func2(list_arg):
    list_output = [i**2 for i in list_arg]
    return list_output

print(func2(list(range(1, 100))))

@decorator
def func3(list_arg):
    list_output = list(map(lambda x: x**2, list_arg))
    return list_output

print(func3(list(range(1, 100))))  
