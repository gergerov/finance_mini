from flask import Flask, request
import json
from Config import checktoken, secretkey, host, port
from handling import message_handling
from Dbj import Dbj
import threading
import logging

logger = logging.getLogger("Server")
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler("server.log")
formatter = logging.Formatter('%(lineno)s : %(asctime)s : %(name)s : %(levelname)s : %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

app = Flask(__name__)
logger.info('Запуск приложения flask server')


@app.route('/', methods=['GET'])
def homepage():
    u = request.remote_addr
    logger.info("Обращение методом GET пользователем: " + u)
    return 'Это домашняя страница веб-сервиса, который является частью бота'


@app.route('/', methods=['POST'])
def event_handling():
    u = request.remote_addr
    logger.info("Обращение методом POST пользователем: " + u)
    js = json.loads(request.data)

    if js['secret'] == secretkey:
        if js['type'] == 'confirmation':
            logger.info("Получено уведомления вида 'confirmation', возвращен код проверки")

            return checktoken

        elif js['type'] == 'message_new':
            logger.info("Получено уведомления вида 'message_new', запуск потока обработки нового сообщения")
            t = threading.Thread(target=handl, args=(js,))
            t.start()

            return 'ok'

        else:
            return 'ok'

    else:
        return 'Не знаю тебя'


def handl(js):
    handling = message_handling(js)
    handling.run()


if __name__ == "__main__":
    app.run()
