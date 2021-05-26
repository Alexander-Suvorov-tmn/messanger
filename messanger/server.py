# Программа сервера для получения приветствия от клиента и отправки ответа
from socket import *
import sys
import argparse
import pickle
from logger import server_log_config
from l import Log
import time
import select

def createParser ():
    parser = argparse.ArgumentParser()
    parser.add_argument ('-p', '--port', nargs='?', type=int, default=7777)# порт для работы
    parser.add_argument ('-a', '--addr', nargs='?', default='')# адрес прослушивания
    return parser

def read_requests(r_clients, all_clients):
# """ Чтение запросов из списка клиентов"""
    responses = {} # Словарь ответов сервера вида {сокет: запрос}
    for sock in r_clients:
        try:
            data = pickle.loads(sock.recv(1024))
            responses[sock] = data
        except:
            print(f'Клиент {sock.fileno()} {sock.getpeername()} отключился')
            all_clients.remove(sock)

    return responses


def write_responses(requests, w_clients, all_clients):
# """ Эхо-ответ сервера клиентам, от которых были запросы"""
    for sock in w_clients:
        try:
    # Подготовить и отправить ответ сервера
            resp = {'sock':sock.getpeername(), 'msg':requests[sock]}
    # Эхо-ответ сделаем чуть непохожим на оригинал
            sock.send(pickle.dumps(resp.upper()))
        except: # Сокет недоступен, клиент отключился
            print(f'Клиент {sock.fileno()} {sock.getpeername()} отключился')
            sock.close()
            all_clients.remove(sock)


def write_responses_all(requests, all_clients):
    # """ Пересылка сообщений
    # """
    for sock in all_clients:
        for val in requests.values():
            if val['to'] == '#room_boom':
                try:                   
                    sock.send(pickle.dump(response(val['from'], val['message'])))
                except:  # Сокет недоступен, клиент отключился
                    print(f'Клиент {sock.fileno()} {sock.getpeername()} отключился')
                    sock.close()
                    all_clients.remove(sock)

@Log()
def upload_message(data):#обрабатываем сообещние от пользователя   
    print(pickle.loads(data))
    # send_message()
    logger.info('сообщение от пользователя сформированно')   

def response(alias, message):# ответ пользователю
    response = {
        "action": "msg",
        "time": "<unix timestamp>",
        "to": "#room_boom",
        "from": alias,
        "message": message
    }
    return response

def form_mes(respons):#формируем ответ пользователю   
    mc = pickle.dumps(respons)
    logger.info('сообщение пользователю сформированно')
    return mc

if __name__ == "__main__":    
    logger = server_log_config.get_logger(__name__)
    
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    
    sock = socket(AF_INET, SOCK_STREAM)  # Создает сокет TCP
    sock.bind((namespace.addr, namespace.port))# Присваивает порт
    sock.listen(5)                        # Переходит в режим ожидания запросов;# Одновременно обслуживает не более # 5 запросов.
    sock.settimeout(0.2)   
    logger.info(f"Сервер запущен на порту: {namespace.port}")
    user = []#список с адресами пользователей
    
    while True:
        try:
            print ('Start Server')
            conn, addres = sock.accept()            
           
        except OSError as e:
            pass  # timeout вышел

        else:
            print (f'Подключение {str(addres)}')
            if  addres not in user: 
                user.append(conn)# Если такого клиента нету , то добавить
        finally:    
            wait = 10
            r = []
            w = []
            e = []
            try:
                r, w, e = select.select(user, user, [], wait)
            except:
                pass  # Ничего не делать, если какой-то клиент отключился

            requests = read_requests(r, user)  # Сохраним запросы клиентов
            if requests:              
                write_responses_all(requests, user)
