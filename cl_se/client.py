# Программа клиента для отправки приветствия серверу и получения ответа
from socket import *
import sys
import argparse
import pickle

def createParser ():
    parser = argparse.ArgumentParser()
    parser.add_argument ('-p', '--port', nargs='?', type=int, default=7777)# порт на сервере
    parser.add_argument ('-a', '--addr', nargs='?', default='localhost')# адрес сервера
 
    return parser

parser = createParser()
namespace = parser.parse_args (sys.argv[1:])
print(namespace)

s = socket(AF_INET, SOCK_STREAM)  # Создать сокет TCP
s.connect((namespace.addr, namespace.port))   # Соединиться с сервером

msg = {
    "action": "presence",
    "time": '<unix timestamp>',
    "type": "status",
    "user": {
        "account_name": "AlexSu",
        "status": "Yep, I am here!"
    }
}

s.send(pickle.dumps(msg))
data = s.recv(1024)
print('Сообщение от сервера: ', pickle.loads(data), ', длиной ', len(data), ' байт')
s.close()
