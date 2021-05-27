from socket import *
import sys
import argparse
import pickle
from logger import client_log_config
#from l import Log
import select
import json

def createParser ():
    parser = argparse.ArgumentParser()
    parser.add_argument ('-p', '--port', nargs='?', type=int, default=7777)# порт на сервере
    parser.add_argument ('-a', '--addr', nargs='?', default='localhost')# адрес сервера
    return parser

#формируем сообщение серверу
def message(alias, message):
    msg = {
        "action": "msg",
        "time": "<unix timestamp>",
        "to": "#room_boom",
        "from": alias,
        "message": message
    }
    return msg

#принимаем сообещение от сервера,декодируем, 
#Принимает байты и выдает словарь, если принято что - то другое отдает ошибку значения
def loads_msg(sock):
    data = sock.recv(1024)
    if isinstance(data, bytes):
        response = pickle.loads(data)
        logger.info('Сообщение от сервера: ', response, ', длиной ', len(data), ' байт')
        if isinstance(response, dict):
            return response
        raise ValueError
    raise ValueError

#кодирование и отправка сообщения. Принимает словарь и отправляет его
def send_message(sock, message):#отправляем сообещение серверу
    sock.send(pickle.dumps(message))



#основной код работы   
def main(namespace):

    try:
        if not 1024 <= namespace.port <= 65535:
            raise ValueError
        logger.info(f"Connected to remote host - {namespace.addr}:{namespace.port} ")
    except ValueError:
        logger.warning("The port must be in the range 1024-6535")
        sys.exit(1)
    else:
        with socket(AF_INET, SOCK_STREAM) as sock:
            # Соединиться с сервером
            try :
                sock.connect((namespace.addr, namespace.port))
            except :
                print(f'Unable to connect')
                sys.exit()
            else:
                alias = input('Name: ')              
                logger.info("Message send")

                while True:
                    try:
                        msg = input('Say: ')
                        if msg == 'exit':
                            sys.exit(1)
                        send_message(sock, message(alias, msg))
                        data = loads_msg(sock)
                        print(f'<{data["from"] if data["from"] != alias else "You"}>: {data["message"]}')
                        logger.info("The message is received")
                    except (ValueError, json.JSONDecodeError):
                        pass
                        logger.warning("Failed to decode server message.")


if __name__ == "__main__":
    logger = client_log_config.get_logger(__name__)

    parser = createParser()
    namespace = parser.parse_args (sys.argv[1:])
    main(namespace)