# 1. Каждое из слов «разработка», «сокет», «декоратор» 
# представить в строковом формате и проверить тип и содержание 
# соответствующих переменных. Затем с помощью онлайн-конвертера 
# преобразовать строковые представление в формат Unicode и также 
# проверить тип и содержимое переменных.

# sim = ['разработка', 'сокет', 'декоратор']

# for line in sim:
#     print('тип переменной: {}\n'.format(type(line)))
#     print('содержание переменной - {}\n'.format(line))


# # в Unicode
# var = ['\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430',
#        '\u0441\u043e\u043a\u0435\u0442',
#        '\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440']
# for line in var:
#     print('тип переменной: {}\n'.format(type(line)))
#     print('содержание переменной - {}\n'.format(line))  

# 2. Каждое из слов «class», «function», «method» записать в байтовом типе без преобразования 
# в последовательность кодов (не используя методы encode и decode) и определить тип, 
# содержимое и длину соответствующих переменных. 
# sim = [b'class', b'function', b'method']

# for line in sim:
#     print('содержание переменной - {}\n'.format(line))
#     print('тип переменной: {}\n'.format(type(line)))    
#     print('длинна строки: {}\n'.format(len(line)))

# # 3. Определить, какие из слов «attribute», «класс», «функция», «type» невозможно 
# # записать в байтовом типе.
# sim2 = b'attribute'
# sim3 = b'класс'
# sim4 = b'функция'
# # sim5 = b'type'  
# #на кирилических словах выскакивают исключения
# #   File "/home/alexandr/Клиент-серверные приложения на Python/mes/1.py", line 34
# #     sim3 = b'класс'
# #            ^
# # SyntaxError: bytes can only contain ASCII literal characters.

# # 4. Преобразовать слова «разработка», «администрирование», «protocol», «standard» 
# # из строкового представления в байтовое и выполнить обратное преобразование 
# # (используя методы encode и decode).

# sim = ['разработка', 'администрирование', 'protocol', 'standard']
# for i in sim:
#     print(i, 'encode')
#     a = i.encode('utf-8')
#     print(a, type(a))

#     b = bytes.decode(a, 'utf-8')
#     print(b, 'decode', type(b))
#     print('---   ---   ---'*4)

# # 5. Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать 
# # результаты из байтовового в строковый тип на кириллице.

# print('--'*30)
 
# import subprocess
 
 
# ping_resurs = [['ping', 'yandex.ru'],['ping', 'youtube.com']]
 
# for ping_now in ping_resurs:
 
#     ping_process = subprocess.Popen(ping_now, stdout=subprocess.PIPE)
 
#     i = 0
 
#     for line in ping_process.stdout:
 
#         if i<10:
#             print(line)
#             line = line.decode('cp866').encode('utf-8')
#             print(line.decode('utf-8'))
#             i += 1
#         else:
#             print('--'*30)
#             break

# # 6. Создать текстовый файл test_file.txt, заполнить его тремя строками: 
# # «сетевое программирование», «сокет», «декоратор». Проверить кодировку файла по умолчанию. 
# # Принудительно открыть файл в формате Unicode и вывести его содержимое.

import locale
 
resurs_string = ['сетевое программирование', 'сокет', 'декоратор']
 
#Создаем файл
with open('resurs.txt', 'w+') as f_n:
    for i in resurs_string:
        f_n.write(i + '\n')
    f_n.seek(0)
 
print(f_n) # печатаем объект файла, что бы узнать его кодировку
 
file_coding = locale.getpreferredencoding()
 
#Читаем из файла
with open('resurs.txt', 'r', encoding=file_coding) as f_n:
    for i in f_n:
        print(i)
 
    f_n.seek(0)