import re
import csv


def get_data():

    #главный список
    main_data = [['Изготовитель системы', 'Код продукта', 'Тип системы', 'Название ОС'] ]

    info_1 = []
    info_2 = []
    info_3 = []


    file_list = ['info_1.txt', 'info_2.txt', 'info_3.txt']
    l_s = ['Изготовитель системы', 'Код продукта', 'Тип системы', 'Название ОС']

    #списки выходных данных
    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []

    #функция обработки файла
    def file_open(file, key):
        with open(file, encoding='cp1251') as f:
            for line in f:
                if key in line:
                    res = re.split(r':', line, maxsplit=1)
                    if key == 'Изготовитель системы':
                        os_prod_list.append(res[1].lstrip())                    
                    elif key == 'Код продукта':
                        os_code_list.append(res[1].lstrip())
                    elif key == 'Тип системы':
                        os_type_list.append(res[1].lstrip())
                    elif key == 'Название ОС':
                        os_name_list.append(res[1].lstrip())

    #циклическая обработка файлов
    def handler():

        for file in file_list:
            for key in l_s:
                file_open(file, key)
        
    handler()

    #передаем значения в главный список
    info_1.append(os_prod_list[0])
    info_1.append(os_code_list[0])
    info_1.append(os_type_list[0])
    info_1.append(os_name_list[0])
    main_data.append(info_1)

    info_2.append(os_prod_list[1])
    info_2.append(os_code_list[1])
    info_2.append(os_type_list[1])
    info_2.append(os_name_list[1])
    main_data.append(info_2)

    info_3.append(os_prod_list[2])
    info_3.append(os_code_list[2])
    info_3.append(os_type_list[2])
    info_3.append(os_name_list[2])
    main_data.append(info_3)

    return main_data
    

def write_to_csv(link):

    res = get_data()
    with open(link, "w", newline='') as f:
        csv.writer(f).writerow(res)

write_to_csv('outfile.csv')
