from socket import *
import sys
import argparse
import pickle
from logger import client_log_config
#from l import Log
import select
import json
import threading
import time

#Парсер адреса и порта
def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument ('-p', '--port', nargs='?', type=int, default=7777)# порт на сервере
    parser.add_argument ('-a', '--addr', nargs='?', default='localhost')# адрес сервера 
    parser.add_argument('-n', '--name', default=None, nargs='?')#имя пользователя
    return parser

#выбор режима отправки сообщения
def selecting_mode(sock, client_name):
    while True:
            
        print('\nВыберите действие:')
        print('  отправить сообещение в личку 1;')
        print('  отправить сообещенеи в общую группу 2;')
        print('  войти в/ создать группу 3.\n')
        print('  выйти из программы 4.\n')
        purpose = input('Введите 1, 2, 3 или 4: ')

        if purpose == '1':
            to = input('Введите имя получателя: ')
            message_u(sock, to, client_name)
        elif purpose == '2':
            to = 'all'
            message_u(sock, to, client_name)
        elif purpose == '3':
            to = input('Введите имя группы: ')
            send_message_group(sock, to, client_name)
        elif purpose == '4':
            send_message(sock, create_exit_message(client_name))
            print('Завершение соединения.')
            logger.info('Завершение работы по команде пользователя.')
            # Задержка неоходима, чтобы успело уйти сообщение о выходе
            time.sleep(0.5)
            break
        else:
            print('Команда не распознана, попробойте снова.')

def send_message_group(sock, to, client_name):
    pass

#сообщение для выхода
def create_exit_message(client_name):
    return {
        "action": 'exit',
        "time": time.time(),
        "sender": client_name
    }

# Функция генерирует запрос о присутствии клиента
def create_presence(account_name):
    out = {
        "action": 'presence',
        "time": time.time(),
        "user": {
            "account_name": account_name
        }
    }
    logger.debug(f'Сформировано сообщение для пользователя {account_name}')
    return out

# Функция разбирает ответ сервера на сообщение о присутствии, возращает 200 если все ОК или генерирует исключение при\
# ошибке.

def process_response_ans(message):
    logger.debug(f'Разбор приветственного сообщения от сервера: {message}')
    if "responce" in message:
        if message['response'] == 200:
            return '200 : OK'
        elif message['responce'] == 400:
            raise (f'400 : {message["error"]}')
    raise ("response")

#формируем  и  отправляем сообщение 
def message_u(sock, to, client_name = 'Guest'):

    message = input('Введите сообщение для отправки: ')
    msg = {
        "action": 'msg',
        "time": time.time(),
        "distination": to,
        "sender": client_name,
        "message": message
    }
    try:
        send_message(sock, msg)
        logger.info(f'Отправлено сообщение для пользователя {to}')
    except:
        logger.critical('Потеряно соединение с сервером.')
        exit(1)

# Функция создаёт словарь с сообщением о выходе.
def create_exit_message(client_name):
    return {
        "action": 'exit',
        "time": time.time(),
        "sender": client_name
    }


#принимаем сообещение от сервера,декодируем, 
#Принимает байты и выдает словарь, если принято что - то другое отдает ошибку значения
def loads_msg(sock, client_name):
    while True:
        try:
            data = sock.recv(1024)
            if isinstance(data, bytes):
                response = pickle.loads(data)

                if isinstance(response, dict):
                    print(f'\nПолучено сообщение от пользователя {response["sender"]}:\n{response["message"]}')
                    logger.info(f'Получено сообщение от пользователя {response["sender"]}:\n{response["message"]}')
                
                else:
                    print(f'Получено некорректное сообщение с сервера: {response}')
                    logger.error(f'Получено некорректное сообщение с сервера: {response}')
        except:
            logger.error(f'Не удалось декодировать полученное сообщение.')
            print(f'Не удалось декодировать полученное сообщение.')
            break

#кодирование и отправка сообщения. Принимает словарь и отправляет его
def send_message(sock, msg):#отправляем сообещение серверу
    sock.send(pickle.dumps(msg))

#основной код работы   
def main(namespace):

    client_name = input('Введите имя пользователя: ')
    print(f'Запущен клиент с парамертами: адрес сервера: {namespace.addr} , порт: {namespace.port}, имя пользователя: {client_name}')

    logger.info(
        f'Запущен клиент с парамертами: адрес сервера: {namespace.addr} , порт: {namespace.port}, имя пользователя: {client_name}')

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
                # Если соединение с сервером установлено корректно, запускаем клиенский процесс приёма сообщний
                receiver = threading.Thread(target=loads_msg, args=(sock, client_name))
                receiver.daemon = True
                receiver.start()  

                # затем запускаем отправку сообщений и взаимодействие с пользователем.
                user_interface = threading.Thread(target=selecting_mode, args=(sock, client_name))
                user_interface.daemon = True
                user_interface.start()
                logger.debug('Запущены процессы')  

                # если один из потоков завершён, то значит или потеряно соединение или пользователь
                # ввёл exit. Поскольку все события обработываются в потоках, достаточно просто завершить цикл.
                while True:
                    time.sleep(1)
                    if receiver.is_alive() and user_interface.is_alive():
                        continue
                    break   
          
if __name__ == "__main__" :
    logger = client_log_config.get_logger(__name__)
    parser = createParser()
    namespace = parser.parse_args (sys.argv[1:])
    main(namespace)
