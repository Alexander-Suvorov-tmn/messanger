from socket import *
import sys
import argparse
import pickle

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
    return a

def send_mess():#отправляем сообещние
    m = msg()
    sen = form_message(m)
    s.send(sen)

def loads_msg():#принимаем сообещение от сервера
    data = s.recv(1024)
    q = pickle.loads(data)
    print('Сообщение от сервера: ', q, ', длиной ', len(data), ' байт')
    s.close()
    # return data, q

# def print_msg():#обрабатываем принятое сообещние
    # # data, q = loads_msg()
    # print('Сообщение от сервера: ', q, ', длиной ', len(data), ' байт')
    # s.close()


parser = createParser()
namespace = parser.parse_args (sys.argv[1:])

s = socket(AF_INET, SOCK_STREAM)  # Создать сокет TCP
s.connect((namespace.addr, namespace.port))   # Соединиться с сервером

send_mess()
loads_msg()


