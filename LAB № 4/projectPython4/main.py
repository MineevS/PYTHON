# Mineev S. A. [08.11.2023]

# Server:  http:://localhost:8080

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

    async def get_handler_receiveConcreteData(self, request):
        path = request.path
        head = path.split('/')  # '/labs/lab<i>' -> ['', 'labs', 'lab<i>'] head[3] = 'lab<i>';

        for elem in head[2::]:
            text = dict()
            if elem in self.LABS.keys():
                print(self.LABS[elem])
                data = self.LABS[elem]
                text.update({elem: data})
                self.status = (200, self.status)[
                    self.status == 404]  # Если ранее хотя бы для одной из таблиц уже был установлен код, того, что она не найдена (404), то не менять код, иначе сменить.
            else:
                self.status = 404  # нет лабы
        return web.Response(headers={'Location': text}, status=self.status)  # web.Response(text="Hello world")

    async def get_handler_receiveAllData(self, request):
        text = dict()
        for elem in self.LABS.keys():
            data = self.LABS[elem]
            text.update({elem: data})

        self.status = 200
        return web.Response(text=json.dumps(text), status=self.status)  # web.Response(text="Hello world")

    async def post_handler(self, request):  # Создание
        # Если передано тело, то подразумевается, что пользователь хочет создать таблицу на основе определенного имени и/или определенных полей
        if request.body_exists:  # Запрос содержит тело
            if request.can_read_body:  # Можем прочесть тело
                self.countLabAbsalute += 1
                data = await request.json()
                path = request.path
                head = path.split('/')

                h = (head[2:-1], head[2::])[head[-1] != '']

                if not h:
                    self.pastCreateLab = ("lab1", "lab" + str(self.countLabAbsalute))[self.LABS.__len__() != 0]
                    self.countLabAbsalute += 1
                else:
                    self.pastCreateLab = h[0]

                text = "http://" + request.host + '/labs/' + self.pastCreateLab

                if self.pastCreateLab in self.LABS:
                    self.status = 409  # Уже имеется лабораторная работа с данным именем
                    text = 'Уже имеется лабораторная работа с данным именем!'
                else:
                    now = datetime.date.today().strftime("%d.%m.%Y")
                    self.LABS.setdefault(self.pastCreateLab, dict({"Deadline": now}))

                    self.add_value(head, self.pastCreateLab, data)
        else:
            self.countLabAbsalute += 1
            self.pastCreateLab = ("lab1", "lab" + str(self.countLabAbsalute))[self.LABS.__len__() != 0]
            text = "http://" + request.host + '/labs/' + self.pastCreateLab

            now = datetime.date.today().strftime("%d.%m.%Y")
            self.LABS.setdefault(self.pastCreateLab, dict({"Deadline": now}))
            self.NameLabs = self.LABS.keys()

        self.status = (201, self.status)[self.status == 409]

        return web.Response(text=json.dumps({self.pastCreateLab: self.LABS[self.pastCreateLab]}),
                            headers={'Location': text}, status=self.status)  # web.Response(text="Hello world")

    async def put_handler(self, request):  # Изменение
        # text = request.read()
        if request.body_exists:  # Запрос содержит тело
            if request.can_read_body:  # Можем прочесть тело
                data = await request.json()

                path = request.path
                head = path.split('/')

                h = (head[2:-1], head[2::])[head[-1] != '']
                text=None
                for namelab in h:
                    if namelab in self.LABS.keys():
                        self.add_value(head, namelab, data)
                        if text == None:
                            text = {namelab: self.LABS[namelab]}
                        else:
                            text = [text, {namelab: self.LABS[namelab]}]
                    else:
                        self.status = 404  # Нет такой таблицы для добавления.
                        if text == None:
                            text = "Нет такой таблицы для добавления";
                        else:
                            text = [text, "Нет такой таблицы для добавления"]

                text = (json.dumps(text), "Error date format")[self.status == 400]
            else:
                self.status = 400
                text = "не корректно тело запроса!"

        return web.json_response(text=text, status=self.status)

    def add_value(self, head, namelab, data):
        for field_key in data.keys():
            if field_key in self.LABS[namelab]:
                if head[-1] != '':  # add data
                    self.status = self.isdataformatCorrect(field_key, data)
                    if self.status == 200:
                        if field_key == "Deadline":
                            if data[field_key] in self.LABS[namelab][field_key]:
                                pass
                            else:
                                self.LABS[namelab][field_key] = [self.LABS[namelab][field_key],
                                                                 data[field_key]]
                                self.LABS[namelab][field_key].sort(
                                    key=lambda date: datetime.datetime.strptime(date, '%d.%m.%Y'))
                        else:
                            if isinstance(data[field_key], list):
                                for val in data[field_key]:
                                    if val in self.LABS[namelab][field_key]:
                                        pass
                                    else:

                                        if isinstance(self.LABS[namelab][field_key], list):
                                            self.LABS[namelab][field_key].append(val)
                                        else:
                                            self.LABS[namelab][field_key] = [
                                                self.LABS[namelab][field_key],
                                                val]
                            else:
                                if data[field_key] in self.LABS[namelab][field_key]:
                                    pass
                                else:
                                    self.LABS[namelab][field_key] = [
                                        self.LABS[namelab][field_key], data[field_key]]
                else:  # overwriting data
                    self.status = self.isdataformatCorrect(field_key, data)
                    if self.status == 200:
                        self.LABS[namelab][field_key] = data[field_key]
            else:
                # значение по ключу может не являться dict и у него может выйти ошибка ( 'lab1': ' ')
                self.LABS[namelab][field_key] = data[field_key]
                # self.LABS[namelab].update({field_key: data[field_key]})
                self.status = (200, self.status)[self.status == 400]

    def isdataformatCorrect(self, field_key, data) -> int:
        if field_key == 'Deadline':  # "%d.%m.%Y"
            try:
                datetime.datetime.strptime(data[field_key], "%d.%m.%Y")
                status = 200
            except ValueError:
                status = 400  # Дата не корректная.
        else:
            status = 200
        return status

    async def delete_handler(self, request):
        massage = ''
        print(request.path)
        path = request.path
        head = path.split('/')

        # Если вызов содержит тело, то удалить требуется определенные поля лабораторной, а не все сведения о лабораторной.
        if request.body_exists:  # Запрос содержит тело
            if request.can_read_body:  # Можем прочесть тело
                data = await request.json()
                path = request.path
                head = path.split('/')
                for namelab in head[2::]:
                    if namelab in self.LABS.keys():
                        for field_key in data.keys():
                            if field_key in self.LABS[namelab]:
                                v = data[field_key]
                                if isinstance(v, list):
                                    for elem in v:
                                        if field_key == 'Deadline':
                                            if elem in self.LABS[namelab][field_key] and len(self.LABS[namelab][field_key]) > 1:
                                                self.LABS[namelab][field_key].remove(elem)
                                                self.status = (200, self.status)[self.status == 408]
                                            else:
                                                self.status = 408  # Дата последняя. Не удалаем т. к. является обязательным полем.
                                                massage = "Попытка удалить обязательное поле - дату"
                                        else:
                                            if elem in self.LABS[namelab][field_key]:
                                                self.LABS[namelab][field_key].remove(elem)
                                                self.status = (200, self.status)[self.status == 408]
                                elif isinstance(v, str):
                                    elem = v
                                    if field_key == 'Deadline':
                                        self.status = 408  # Дата последняя. Не удалаем т. к. является обязательным полем.
                                        massage = "Попытка удалить обязательное поле - дату"
                                    else:
                                        if elem in self.LABS[namelab][field_key]:
                                            self.LABS[namelab][field_key].remove(elem)
                                            self.status = 200
                                            massage = self.LABS[namelab]
                                        else:
                                            self.status = 409  # Иначе элемента в данной таблицы у данного ключа нет.
                                            massage = "элемента в данной таблицы у данного ключа нет"

        else:  # Иначе, удалить все сведения о лабораторной.
            for namelab in head:
                if namelab in self.LABS.keys():
                    self.LABS.pop(namelab, None)  # or del self.LABS[request.path]
                    self.status = 200

        return web.Response(text=(request.path, (json.dumps({namelab: massage}), massage)[self.status == 408])[massage != ''],
                            status=self.status)


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
            [web.get('/labs/',              handler.get_handler_receiveAllData),  # all data print
             web.get('/labs/{NameLabs}',    handler.get_handler_receiveConcreteData),  # concrete data print
             web.post('/labs',              handler.post_handler),  # Default create and print lab<i>
             web.post('/labs/{NameLabs}',   handler.post_handler),  # Create concrete data
             web.put('/labs/{NameLabs}',    handler.put_handler),  # Change with addition
             web.put('/labs/{NameLabs}/',   handler.put_handler),  # Change with overwriting
             web.delete('/labs/{NameLabs}', handler.delete_handler),  # Delete
             ])


if __name__ == '__main__':
    aio_server = AioServer()
