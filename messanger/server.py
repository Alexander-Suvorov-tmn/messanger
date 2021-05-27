# Программа сервера для получения приветствия от клиента и отправки ответа
from socket import *
import sys
import argparse
import pickle
from logger import server_log_config
#from l import Log
import time
import select

def createParser ():
    parser = argparse.ArgumentParser()
    parser.add_argument ('-p', '--port', nargs='?', type=int, default=7777)# порт для работы
    parser.add_argument ('-a', '--addr', nargs='?', default='')# адрес прослушивания
    return parser

#@Log()
def read_requests(r_clients, all_clients):
    """ Чтение запросов из списка клиентов
    """
    responses = {}  # Словарь ответов сервера вида {сокет: запрос}

    for sock in r_clients:
        try:
            data = sock.recv(1024)
            responses[sock] = pickle.loads(data)
        except:
            print(f'Client {sock.fileno()} {sock.getpeername()} DISCONNECTED')
            logger.info(f'Client {sock.fileno()} {sock.getpeername()} DISCONNECTED')
            all_clients.remove(sock)

    return responses

#@Log()
def write_responses_all(requests, all_clients):
    """ Общий чат
    """
    for sock in all_clients:
        for val in requests.values():
            try:
                sock.send(pickle.dumps(message(val['from'], val['message'])))
            except:  # Сокет недоступен, клиент отключился
                print(f'Client {sock.fileno()} {sock.getpeername()} DISCONNECTED')
                logger.info(f'Client {sock.fileno()} {sock.getpeername()} DISCONNECTED')
                sock.close()
                all_clients.remove(sock) 

def message(alias, message):
    """Функция формирует сообщение"""
    msg = {
        "action": "msg",
        "time": "<unix timestamp>",
        "to": "#room_boom",
        "from": alias,
        "message": message
    }
    return msg

#@Log()
def main(namespace):
    """ Основной скрипт работы сервера""" 
    clients = []

    sock = socket(AF_INET, SOCK_STREAM)

    try:
        if not 1024 <= namespace.port <= 65535:
            raise ValueError
    except ValueError:
        logger.warning("The port must be in the range 1024-6535")
        sys.exit(1)
    else:
        sock.bind((namespace.addr, namespace.port))
        sock.listen(5)
        sock.settimeout(0.2)
        logger.info(f"The server is RUNNING on the port: {namespace.port}")

    while True:
        try:
            conn, addr = sock.accept()  # Проверка подключений
        except OSError as e:
            pass  # timeout вышел
        else:
            print(f"Client {str(addr)} CONNECTED")
            logger.info(f"Client {str(addr)} CONNECTED")
            clients.append(conn)
        finally:
            # Проверить наличие событий ввода-вывода
            wait = 10
            r = []
            w = []
            e = []
            try:
                r, w, e = select.select(clients, clients, [], wait)
            except:
                pass  # Ничего не делать, если какой-то клиент отключился

            requests = read_requests(r, clients)  # Сохраним запросы клиентов
            if requests:
                write_responses_all(requests, clients)


if __name__ == "__main__":
    logger = server_log_config.get_logger(__name__)
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])

    main(namespace)

        
    