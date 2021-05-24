from socket import *
import sys
import argparse
import pickle
from logger import client_log_config
from l import Log
import threading


def createParser ():
    parser = argparse.ArgumentParser()
    parser.add_argument ('-p', '--port', nargs='?', type=int, default=7777)# порт на сервере
    parser.add_argument ('-a', '--addr', nargs='?', default='localhost')# адрес сервера
    return parser

def msg(name):#сообщение
    msg = {
        "action": "presence",
        "time": '<unix timestamp>',
        "type": "status",
        "user": {
            "account_name": name,
            "status": "Yep, I am here!"
        }
    }
    return msg

def form_message(m):#формируем сообещение серверу
    a = pickle.dumps(m)
    logger.info('сообщение сформированно')
    return a

@Log()
def send_mess():#отправляем сообещние
    m = msg(nick_name)
    sen = form_message(m)
    s.sendto(sen, namespace)
    logger.info('сообщение отправленно на сервер')

# @Log()
def rec_messages():#прием сообщения и обрабатываем сообещение от сервера
    while 1:
        data = s.recv(1024)
    
        try:
            q = pickle.loads(data)
            print(q)
            logger.info('Сообщение c сервера: ', q, ', длиной ', len(data), ' байт')
            # s.close()
        except Exception as e:
            logger.error('Ошибка работы программы client.py', e)


if __name__ == "__main__":
    logger = client_log_config.get_logger(__name__)

    parser = createParser()
    namespace = parser.parse_args (sys.argv[1:])
    nick_name = input('Ваш Ник')
    s = socket(AF_INET, SOCK_STREAM)  # Создать сокет TCP
    # s.connect((namespace.addr, namespace.port))   # Соединиться с сервером
    s.bind(('', 0))
    send_mess()
    potok = threading.Thread(target= rec_messages)
    potok.start()
    while 1:
        mes = input('Введите сообщение: ')
        s.sendto(('['+nick_name+']' + pickle.dumps(mes)), namespace)


    


