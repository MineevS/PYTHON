#%%

#%%
from enum import Enum
import datetime

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

    def writeData(self, status : STATUS, msg: str):
        self.file.write(f'[{status.name}]{datetime.datetime.now()}:{msg}\n');

    def __del__(self):
        self.file.close()


logger = LOGGER()

logger.writeData(STATUS.DEBUG, "Включен режим отладки")
logger.writeData(STATUS.ERROR, "На сервере произошла ошибка E[388]")

logger.writeData(STATUS.DEBUG, "Включен режим отладки")
logger.writeData(STATUS.ERROR, "На сервере произошла ошибка E[388]")
logger.writeData(STATUS.INFO, "Ведутся технические работы. Зайдите на сайт позже!")
logger.writeData(STATUS.CRITICAL, "Критическая ошибка CR[721]")
logger.writeData(STATUS.WANR, "В несенных изменениях есть неявное приведение типов long -> float W[124]")

del logger

f = open("log.txt")
lines = f.read()
print(lines)
f.close()


#%%