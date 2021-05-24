from socket import *
import sys
import argparse
import pickle
from log import client_log_config

def createParser ():
    parser = argparse.ArgumentParser()
    parser.add_argument ('-p', '--port', nargs='?', type=int, default=7777)# порт на сервере
    parser.add_argument ('-a', '--addr', nargs='?', default='localhost')# адрес сервера
    return parser

def msg():#сообщение
    msg = {
        "action": "presence",
        "time": '<unix timestamp>',
        "type": "status",
        "user": {
            "account_name": "AlexSu",
            "status": "Yep, I am here!"
        }
    }
    return msg

def form_message(m):#формируем сообещение серверу
    a = pickle.dumps(m)
    logger.info('сообщение сформированно')

    return a

def send_mess():#отправляем сообещние
    m = msg()
    sen = form_message(m)
    s.send(sen)
    logger.info('сообщение отправленно на сервер')

def rec_messages():#прием сообщения
    data = s.recv(1024)
    loads_msg(data)

def loads_msg(data):#обрабатываем сообещение от сервера
    try:
        q = pickle.loads(data)
        logger.info('Сообщение от сервера: ', q, ', длиной ', len(data), ' байт')
        s.close()
    except Exception as e:
        logger.error('Ошибка работы программы client.py', e)



parser = createParser()
namespace = parser.parse_args (sys.argv[1:])

s = socket(AF_INET, SOCK_STREAM)  # Создать сокет TCP
s.connect((namespace.addr, namespace.port))   # Соединиться с сервером

logger = client_log_config.get_logger(__name__)

if __name__ == "__main__":
    send_mess()
    rec_messages()


