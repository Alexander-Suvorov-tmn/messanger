# Программа сервера для получения приветствия от клиента и отправки ответа
from socket import *
import sys
import argparse
import pickle
from logger import server_log_config
from l import Log
import time


def createParser ():
    parser = argparse.ArgumentParser()
    parser.add_argument ('-p', '--port', nargs='?', type=int, default=7777)# порт для работы
    parser.add_argument ('-a', '--addr', nargs='?', default='')# адрес прослушивания
    return parser

@Log()
def upload_message(data):#обрабатываем сообещние от пользователя   
    print(pickle.loads(data))
    # send_message()
    logger.info('сообщение от пользователя сформированно')   

def response():# ответ пользователю
    response = {
        "response": 200,
        "alert":"Необязательное сообщение/уведомление"
    }
    return response

def form_mes(respons):#формируем ответ пользователю   
    mc = pickle.dumps(respons)
    logger.info('сообщение пользователю сформированно')
    return mc

# @Log()
# def send_message():#отправляем сообещнеи пользователю
#     respons = response()
#     a = form_mes(respons)
#     client.send()
#     client.close()
#     logger.info('сообщение пользователю отправленно')

 
if __name__ == "__main__":    
    logger = server_log_config.get_logger(__name__)
    
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    
    s = socket(AF_INET, SOCK_STREAM)  # Создает сокет TCP
    s.bind((namespace.addr, namespace.port))# Присваивает порт
    s.listen(5)                        # Переходит в режим ожидания запросов;# Одновременно обслуживает не более # 5 запросов.
    s.settimeout(0.2)   
    user = []#список с адресами пользователей
    
    try:
        while True:
            print ('Start Server')
            # client, addr = s.accept()
            # data = client.recv(1024)
            data, addres = s.recvfrom(1024)
            print (addres[0], addres[1])

            if  addres not in user: 
                user.append(addres)# Если такого клиента нету , то добавить
            
            for users in user:
                s.send(data, users)

            # upload_message(data)

    except Exception as e:
        logger.error('Ошибка работы программы server.py', e)
    