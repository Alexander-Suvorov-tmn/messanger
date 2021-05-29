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
    parser.add_argument ('-p', '--port', nargs='?', type=int, default=7777)# порт на сервере
    parser.add_argument ('-a', '--addr', nargs='?', default='localhost')# адрес сервера
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p



# @Log()
def read_requests(r_clients, all_clients):
    """ Прием сообщения сообщения
    """
    responses = {}  # Словарь ответов сервера вида {сокет: запрос}

    for sock in r_clients:
        try:
            data = sock.recv(1024)
            responses[sock] = pickle.loads(data)

        except:
            print(f'Client {sock.fileno()} {sock.getpeername()} DISCONNECTED')
            # logger.info(f'Client {sock.fileno()} {sock.getpeername()} DISCONNECTED')
            all_clients.remove(sock)
    return responses

def message_processing_client(requests, messages, client_with_message, clients, names, sock):
    """ обработка сообщений клиентов """

    if requests["action"] == 'presence':#проверяем назначение сообщения
        if requests["user"]["account_name"] not in names.keys():
            names[client_with_message["user"]["account_name"]] = client_with_message#если такого пользователя нет, то добавляем его в names
            response = pickle.dumps(client_with_message, {"responce": 200})
        else:#если такой прользователь есть
            response = { 'response': 400,
            'error': 'Имя пользователя уже занято.'
        }        
            sock.send(pickle.dumps(client_with_message, response))
            clients.remove(client_with_message)
            client_with_message.close()
        return
    elif requests["action"] == 'msg':# Если это сообщение, то добавляем его в очередь сообщений
        messages.append(requests)
        return
    elif  requests["action"] == 'exit':#Если клиент выходит
        clients.remove(names(["account_name"]))
        names["account_name"].close()
        del names["account_name"]
        return
    else:#иначе отдаем ошибку
        response = { "response": 400,
            "error": 'Запрос некорректен.'
        }        
        sock.send(pickle.dumps(client_with_message, response))
        return


# @Log()
def write_responses(i, names, send_data_lst, sock):
    """ Отпрвака сообщений
    """
    #отправка в общую группу
    if  i["destination"] == 'all':
        for r in names:
            try:
                response = r.values()
                sock.send(pickle.dumps(response, i))
            except:  # Сокет недоступен, клиент отключился
                print(f'Client {sock.fileno()} {sock.getpeername()} DISCONNECTED')
                # logger.info(f'Client {sock.fileno()} {sock.getpeername()} DISCONNECTED')
                sock.close()
                send_data_lst.remove(sock)

    # отправка адресно
    if i["destination"] in names and names[i["destination"]] in send_data_lst:
       sock.send(pickle.dumps(names[i["destination"], i]))
        # logger.info(f'Отправлено сообщение пользователю {i["destination"]} от пользователя {i["sender"]}.')
    elif i["destination"] in names and names[i["destination"]] not in send_data_lst:
        raise ConnectionError
    else:
        pass
        # logger.error(
            # f'Пользователь {i["destination"]} не зарегистрирован на сервере, отправка сообщения невозможна.')


# @Log()
def main():

        # Загрузка параметров командной строки, если нет параметров, то задаём значения по умоланию.
    listen_address, listen_port = createParser()

    try:
        if not 1024 <= listen_port <= 65535:
            raise ValueError
        # logger.info(f"Connected to remote host - {listen_address}:{listen_port} ")
    except ValueError:
        # logger.warning("The port must be in the range 1024-6535")
        sys.exit(1)
    else:
        sock = (AF_INET, SOCK_STREAM)    
        sock.bind((listen_address, listen_port))
        sock.listen(5)
        sock.settimeout(0.2)
        # logger.info(f"The server is RUNNING on the port: {listen_port}")

        # список клиентов , очередь сообщений
        clients = []
        messages = []

        # Словарь, содержащий имена пользователей и соответствующие им сокеты.
        names = dict()

    while True:
        # Ждём подключения, если таймаут вышел, ловим исключение.
        try:
            client, client_address = sock.accept()
        except OSError:
            pass
        else:
            # logger.info(f'Установлено соедение с ПК {client_address}')
            clients.append(client)

        recv_data_lst = []
        send_data_lst = []
        err_lst = []
        # Проверяем на наличие ждущих клиентов
        try:
            if clients:
                recv_data_lst, send_data_lst, err_lst = select.select(clients, clients, [], 0)
        except OSError:
            pass

        # принимаем сообщения и если ошибка, исключаем клиента.
        if recv_data_lst:
            for client_with_message in recv_data_lst:
                try:
                    requests = read_requests(recv_data_lst, clients)
                    names[requests["destination"]]=client_with_message
                    message_processing_client(requests, messages, client_with_message, clients, names, sock)
                except:
                    # logger.info(f'Клиент {client_with_message.getpeername()} отключился от сервера.')
                    clients.remove(client_with_message)

        # Если есть сообщения, обрабатываем каждое.
        for i in messages:
            write_responses(i, names, send_data_lst, sock)
        messages.clear()


if __name__ == '__main__':
    main()
   