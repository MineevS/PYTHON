# Mineev S. A. [08.11.2023]

# Server:  http:://localhost:8080

import aiohttp
import asyncio

import self as self
# from aiohttp import web_server
from aiohttp import web
import json
import datetime

class Handler:
    def __init__(self):
        self.NameLabs = None
        self.routes = web.RouteTableDef()
        self.LABS = dict()
        self.pastCreateLab = None
        self.status = 200
        self.countLabAbsalute = 0


    #@self.routes.get('/')
    async def get_handler_default(self, request):
        # Если передано тело, то подразумевается, что пользователь хочет создать таблицу на основе определенного имени и определенных полей
        if request.body_exists:         # Запрос содержит тело
            if request.can_read_body:   # Можем прочесть тело
                self.countLabAbsalute += 1
        else:
            self.countLabAbsalute += 1
            self.pastCreateLab = ("lab1", "lab" + self.countLabAbsalute)[self.LABS.__len__() != 0]
            text = "http://" + request.host + '/' + self.pastCreateLab
        now = datetime.date.today().strftime("%d.%m.%Y")
        self.LABS.setdefault(self.pastCreateLab, dict({"Deadline": now}))
        self.NameLabs = self.LABS.keys()
        return web.Response(text=text, status=self.status)  # web.Response(text="Hello world")

    async def get_handler_receiveConcreteData(self, request):
        path = request.path
        head = path.split('/')  # '/labs/lab<i>' -> ['', 'labs', 'lab<i>'] head[3] = 'lab<i>';

        for elem in head:
            text = dict()
            if elem in self.LABS.keys():
                print(self.LABS[elem])
                data = self.LABS[elem]
                text.update({elem: data})
                self.status = (200, self.status)[self.status == 404] # Если ранее хотя бы для одной из таблиц уже был установлен код, того, что она не найдена (404), то не менять код, иначе сменить.
            else:
                self.status = 404   # нет лабы

        return web.Response(text=json.dumps(text), status=self.status)  # web.Response(text="Hello world")

    async def get_handler_receiveAllData(self, request):
        text = dict()
        for elem in self.LABS.keys():
            data = self.LABS[elem]
            text.update({elem: data})
        return web.Response(text=json.dumps(text), status=self.status)  # web.Response(text="Hello world")

    #@self.routes.post('/post')
    async def post_handler(self, request): # Создание
        # text = request.read()
        if request.body_exists:         # Запрос содержит тело
            if request.can_read_body:   # Можем прочесть тело
                data = await request.json()

                path = request.path
                head = path.split('/')

                for namelab in head:
                    if namelab in self.LABS.keys():
                        for field_key in data.keys():
                            if field_key in self.LABS[namelab]:
                                self.LABS[namelab][field_key] = [self.LABS[namelab][field_key], data[field_key]]
                            else:
                                # значение по ключу может не являться dict и у него может выйти ошибка ( 'lab1': ' ')
                                # self.LABS[namelab] =
                                self.LABS[namelab].update({field_key: data[field_key]})

                        # self.LABS.update({elem: data}) # {'Dectination': '...', 'Deadline': '12.11.23', 'ListStudy': 'Smirnov I.I.'}

                print(data)
                self.status = 200
            else:
                data = "Тело не читабельно"
                self.status = 100

        return web.json_response(text=json.dumps(data), status=self.status)

    #@self.routes.put('/put')
    async def put_handler(self, request): # Изменение
        # text = request.read()
        if request.body_exists:  # Запрос содержит тело
            if request.can_read_body:  # Можем прочесть тело
                data = await request.json()

                path = request.path
                head = path.split('/')

                for namelab in head:
                    if namelab in self.LABS.keys():
                        for field_key in data.keys():
                            if field_key in self.LABS[namelab]:
                                self.LABS[namelab][field_key] = [self.LABS[namelab][field_key], data[field_key]]
                            else:
                                # значение по ключу может не являться dict и у него может выйти ошибка ( 'lab1': ' ')
                                # self.LABS[namelab] =
                                self.LABS[namelab].update({field_key: data[field_key]})

                        # self.LABS.update({elem: data}) # {'Dectination': '...', 'Deadline': '12.11.23', 'ListStudy': 'Smirnov I.I.'}

                print(data)
                self.status = 200
            else:
                data = "Тело не читабельно"
                self.status = 100

        return web.json_response(text=json.dumps(data), status=self.status)

    #@self.routes.delete('/delete')
    async def delete_handler(self, request):
        print(request.path)
        path = request.path
        head = path.split('/')

        # Если вызов содержит тело, то удалить требуется определенные поля лабораторной, а не все сведения о лабораторной.
        if request.body_exists:         # Запрос содержит тело
            if request.can_read_body:   # Можем прочесть тело
                pass
        else: # Иначе, удалить все сведения о лабораторной.
            for namelab in head:
                if namelab in self.LABS.keys():
                    self.LABS.pop(namelab, None)  # or del self.LABS[request.path]
                    self.status = 200

        return web.Response(text=request.path, status=self.status)


'''
app = web.Application()
app.add_routes([web.get('/', handle)])
web.run_app(app)
'''

class AioServer:
    def __init__(self):
        print("Start Server")
        self.app = web.Application()
        self.handler = Handler()
        # self.app.add_routes(self.handler.routes)
        self.init_app(self.handler)
        web.run_app(self.app)

    def init_app(self, handler):
        self.app.router.add_routes(
            [web.get('/labs',                   handler.get_handler_default),               # Default create and print lab<i>
             web.get('/labs/',                  handler.get_handler_receiveAllData),        # all data print
             web.get('/labs/{NameLabs}',        handler.get_handler_receiveConcreteData),   # concrete data print
             web.post('/labs/{NameLabs}',       handler.post_handler),                      # Create
             web.put('/labs/{NameLabs}',        handler.put_handler),                       # Change
             web.delete('/labs/{NameLabs}',     handler.delete_handler),                    # Delete
             ])
        '''
        routes = web.RouteTableDef()
        # ...
        self.app.add_routes(routes)
        '''


if __name__ == '__main__':
    aio_server = AioServer()
