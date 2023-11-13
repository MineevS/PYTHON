# %%
# Mineev S. A. [24.10.2023]
# %%
from enum import Enum
import datetime
import time


class STATUS(Enum):
    DEBUG = 1
    INFO = 2
    WANR = 3
    ERROR = 4
    CRITICAL = 5


class Singleton(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Singleton, cls).__new__(cls)
        return cls.instance


'''
sing_1 = Singleton()
sing_2 = Singleton()

print(sing_1)
print(sing_2)
print(sing_1 is sing_2)
'''


class LOGGER(object):
    def __new__(cls):
        cls.file = open("log.txt", 'w')
        if not hasattr(cls, 'instance'):
            cls.instance = super(LOGGER, cls).__new__(cls)
        return cls.instance

    def writeData(self, status: STATUS, msg: str):
        print(self.file)
        return self.file.write(f'[{status.name}]{datetime.datetime.now()}:{msg}\n');

    def closeLogger(self):
        print("closeLogger")
        print(self.file)
        self.file.close()


logger = LOGGER()

result = logger.writeData(STATUS.DEBUG, "Включен режим отладки")
print(result)

result = logger.writeData(STATUS.ERROR, "На сервере произошла ошибка E[388]")
print(result)

result = logger.writeData(STATUS.DEBUG, "Включен режим отладки")
print(result)

result = logger.writeData(STATUS.ERROR, "На сервере произошла ошибка E[388]")
print(result)

result = logger.writeData(STATUS.INFO, "Ведутся технические работы. Зайдите на сайт позже!")
print(result)

result = logger.writeData(STATUS.CRITICAL, "Критическая ошибка CR[721]")
print(result)

result = logger.writeData(STATUS.WANR, "В несенных изменениях есть неявное приведение типов long -> float W[124]")
print(result)

logger.closeLogger()

# Метод __del__ не подходит т. к. фактически он сработает тогда, когда
# сборщик мусора перекличится на контекст интепретатора выполнения текущей сессии программы.

f = open("log.txt")
lines = f.read()
print(lines)
f.close()

# %%
