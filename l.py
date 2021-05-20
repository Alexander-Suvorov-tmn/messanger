import inspect
import datetime

class Log():
    def __call__(self, func):
        def decorated(*args, **kwargs):
            res = func(*args, **kwargs)            
            current_frame = inspect.currentframe()# возьми текущий фрейм объект (frame object)            
            caller_frame = current_frame.f_back# получи фрейм объект, который его вызвал            
            code_obj = caller_frame.f_code# возьми у вызвавшего фрейма исполняемый в нём объект типа "код" (code object)
            code_obj_name = code_obj.co_name# и получи егSо имя
            
            today = datetime.datetime.today()         
            
            req_file = inspect.getouterframes(inspect.currentframe(), 2)#из какого файла вызывается функция
            r = str(req_file[1][1])

            if r == 'server.py':
                from logger import server_log_config
                logger = server_log_config.get_logger(__name__)
                logger.info(f'функция {func.__name__}, аргументы {args}')
                logger.info(f'{today.strftime("%Y-%m-%d-%H.%M.%S")},  функция {func.__name__},  вызвана из функции {code_obj_name}')
            else:
                from logger import client_log_config
                logger = client_log_config.get_logger(__name__)
                logger.info(f'{today.strftime("%Y-%m-%d-%H.%M.%S")},  функция {func.__name__},  вызвана из функции {code_obj_name}')

            return res
        return decorated
