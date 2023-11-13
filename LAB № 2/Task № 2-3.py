# Mineev S. A. [24.10.2023]

import time
from abc import ABC, abstractmethod


class WriteData(object):
    def __init__(self):
        self._history_call = list()

    def addData(self, arg1, arg2, arg3):
        self._history_call.append(f'{arg1}: function {arg2} called with arguments {arg3}')


class Decorator(WriteData):
    def __init__(self, cls):
        super(self, cls).__init__()
        self._cls = cls  # Timer

    def __call__(self, args):
        print("<html><body>")
        result_data = self._cls(args)
        super(Decorator, self).addData(result_data[0], result_data[1], args)
        print(self._history_call[-1])
        print("</body></html>")


class Timer(WriteData):
    def __init__(self, func):
        super(self, func).__init__()
        self._func = func
        self._history_call = list()

    def __call__(self, args):
        self.addData(time.time(), self._func.__qualname__, args)
        start = time.time()
        self._func(args)
        end = time.time()
        print(f'Class-Decorator elapsed time = {end - start:01f} sec')
        return end, self._func.__qualname__


def gen_list(n) -> list[int]:
    lst = list()
    for num in range(1, n):
        lst.append(num)
    return lst


@Decorator  # sq = sq2: sq2 = Dec(sq1)
@Timer  # sq1 = Tm(sq)
def squares_for(lst: list) -> list:
    for i in range(len(lst)):
        lst[i] **= 2


@Decorator
@Timer
def squares_list_comprehenshion(lst: list) -> list:
    lst = [i ** 2 for i in lst]


@Decorator
@Timer
def squares_map(lst: list) -> list:
    lst = list(map(lambda x: x ** 2, lst))


def job():
    lst = gen_list(10)  # 000000
    squares_for(lst)
    print("Result 1:", squares_for._history_call);

    lst = gen_list(5)
    squares_for(lst)
    print("Result 2:", squares_for._history_call);

    # ! Для каждого объекта (функции или класса) своя история!

    squares_list_comprehenshion(lst)
    # print("Result 3:", squares_for._history_call);
    squares_map(lst)
    # print("Result 4:", squares_for._history_call);


if __name__ == "__main__":
    job()
