import time

class Abstract():
    def addData(obj, data):
        self._history_call.append(f'{data[0]}: function {data[1]} called with arguments {data[2]}')

class Decorator(Abstract):
    def __init__(self, cls):
        self._cls = cls # Timer
        self._history_call = list()

    def __call__(self, args):
        # print("Start Decorator")
        print("<html><body>")
        result_data = self._cls(args)
        addData(self, [result_data, args])
        # self._history_call.append(f'{result_data[0]}: function {result_data[1]} called with arguments {args}')
        print(self._history_call[-1])
        print("</body></html>")
        # print("End Decorator")

class Timer(Abstract):
    def __init__(self, func):
        self._func = func
        self._history_call = list()

    def __call__(self, args):
        # print("Start Timer")
        addData(obj, [time.time(), self._func.__qualname__, args])
        # self._history_call.append(f'{time.time()}: function {self._func.__qualname__} called with arguments {args}')
        print(self._history_call[-1])
        start = time.time()
        self._func(args)
        end = time.time()
        print(f'Class-Decorator elapsed time = {end-start:01f} sec')
        # print("End Timer")
        return end, self._func.__qualname__

def gen_list(n):
    lst = list()
    for num in range(1, n):
        lst.append(num)
    return lst

@Decorator  # sq = sq2: sq2 = Dec(sq1)
@Timer # sq1 = Tm(sq)
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
    lst = list(map(lambda x: x**2, lst))


def job():
    lst = gen_list(10) #000000
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
    
