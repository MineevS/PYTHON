import json
# mport datetime
import datetime
from aiohttp import web

router = web.RouteTableDef()
LABS = dict()
format_date = "%d.%m.%Y"


def validDate(date) -> bool:
    try:
        datetime.datetime.strptime(date, format_date)
        return True  # Дата соответствует формату
    except ValueError:
        return False  # Дата не соответствует формату


@router.get("/labs/")
@router.get("/labs/{name_lab}")
async def get_handle(request: web.Request) -> web.Response:
    # Запрос получения информации LABS.
    lab_name = request.match_info.get("name_lab", "")
    status = 200  # default

    if lab_name != "" and lab_name in LABS:
        data_output = LABS[lab_name]
    elif lab_name != "":
        data_output = {lab_name: "Информации по запрашиваемой лабе нет"}
        status = 404
    else:
        data_output = LABS

    return web.Response(text=(json.dumps(data_output), json.dumps(data_output))[status == 404],
                        status=status,
                        content_type='application/json')


@router.post("/labs")
async def post_handle(request: web.Request) -> web.Response:
    # Запрос создания LAB.
    nameLab = "lab" + str(len(LABS) + 1)
    LABS.setdefault(nameLab, dict({"DeadLine": datetime.date.today().strftime(format_date)}))
    location = request.scheme + "://" + request.host + request.path + "/" + nameLab
    return web.Response(text=json.dumps(LABS[nameLab]),
                        headers={'Location': location},
                        status=200,
                        content_type='application/json')


@router.put("/labs/{name_lab}")
@router.put("/labs/{name_lab}/")
async def put_handle(request: web.Request) -> web.Response:
    # Запрос изменения LAB.
    lab_name = request.match_info.get("name_lab", "")
    if (not request.body_exists or not request.can_read_body) or not (lab_name in LABS):
        # Запрос не содержит тело или не можем его прочесть или имя лабы нет в LABS.
        return web.Response(text=json.dumps({lab_name: "Отсутствует!"}),
                            status=400,
                            content_type='application/json')

    data = await request.json()

    for key in data.keys():
        if key == 'DeadLine' and not validDate(data[key]):
            # передана невалидная дата
            return web.Response(text=json.dumps({lab_name: "Отсутствует!"}),
                                status=404,
                                content_type='application/json')

        header = request.path.split('/')

        if header[-1] == '' and key in LABS[lab_name].keys():  # append
            if isinstance(data[key], str):
                LABS[lab_name][key] = data[key]
            if isinstance(data[key], list):
                if isinstance(LABS[lab_name][key], str): # Если строка, то сделать ее массивом.
                    LABS[lab_name][key] = [LABS[lab_name][key]]

                for val in data[key]: # И добавить элемент
                    LABS[lab_name][key].append(val)  # Если ключ есть, то перезапишет, если ключа нет, то дополнит.
        else:
            LABS[lab_name].update({key: data[key]})  # overwise

    return web.Response(text=json.dumps(LABS[lab_name]),
                        status=200,
                        content_type='application/json')


def all_keys_available(dict1, dict2):
    return all(k in dict2 for k in dict1)


@router.delete("/labs/{name_lab}")
async def delete_handle(request: web.Request) -> web.Response:
    # Запрос удаления LAB.
    lab_name = request.match_info.get("name_lab", "")
    status = 200  # default
    if not request.body_exists and (lab_name in LABS):
        # Удалить всю лабу
        LABS.pop(lab_name)  # or del self.LABS[lab_name]
        return web.Response(text=json.dumps({lab_name: "Данныя лабараторная работа удалена"}),
                            status=status,
                            content_type='application/json')
    else:
        status = 404  # "лабы в данной базе не существует!"
        return web.Response(text=json.dumps({lab_name: "Данныя лабараторная работа отсутствует"}),
                            status=status,
                            content_type='application/json')


async def init_app() -> web.Application:
    app = web.Application()
    app.add_routes(router)
    return app


if __name__ == '__main__':
    web.run_app(init_app())
