from socket import *
import sys
import argparse
import pickle
from logger import client_log_config
from l import Log
import select

def createParser ():
    parser = argparse.ArgumentParser()
    parser.add_argument ('-p', '--port', nargs='?', type=int, default=7777)# порт на сервере
    parser.add_argument ('-a', '--addr', nargs='?', default='localhost')# адрес сервера
    return parser

def respons(nick_nam, message):#сообщение
    msg = {
        "action": "msg",
        "time": "<unix timestamp>",
        "to": "#room_boom",
        "from": nick_nam,
        "message": message
    }
    return msg

def read_requests(r, sock):
    """ Чтение запросов из списка клиентов
    """
    for s in sock:
        data = pickle.loads(s.recv(1024))
        if not data :
            print (f'\nDisconnected from chat server')
            sys.exit()
        else :
            print(f'<{data["from"]}>: {data["message"]}')

def write_responses(nick_nam, w, msg):

    for sock in w:
        try:
            msg = pickle.dumps(respons(nick_nam, msg))
            sock.send(msg)
        except:  # Сокет недоступен, клиент отключился
            sock.close()
            sys.exit()


if __name__ == "__main__":
    logger = client_log_config.get_logger(__name__)

    parser = createParser()
    namespace = parser.parse_args (sys.argv[1:])

    with socket(AF_INET, SOCK_STREAM) as sock:
        # Соединиться с сервером
        try :
            sock.connect((namespace.addr, namespace.port))
        except :
            print(f'Unable to connect')
            sys.exit()
           
        nick_nam = input('Name: ')
        while True:
            sock_lst = [sock]

            msg = input('Say: ')
            if msg == 'exit':
                break

            r, w, e = select.select(sock_lst , sock_lst, [], 0)

            write_responses(nick_nam, w, msg)
            read_requests(r, sock_lst)
