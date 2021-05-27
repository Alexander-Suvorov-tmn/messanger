import logging

#форматер
_log_format = f"%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"

#уровень ERROR
def get_file_handler():
    file_handler = logging.FileHandler("client.log")
    file_handler.setLevel(logging.ERROR)
    file_handler.setFormatter(logging.Formatter(_log_format))
    return file_handler

#уровень INFO
def get_stream_handler():
    stream_handler = logging.FileHandler("client.log")
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(logging.Formatter(_log_format))
    return stream_handler

#общая обработка
def get_logger(name):
    logger = logging.getLogger('app.client')
    logger.setLevel(logging.INFO)
    logger.addHandler(get_file_handler())
    logger.addHandler(get_stream_handler())
    return logger


