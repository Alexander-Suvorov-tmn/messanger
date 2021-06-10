import logging
from logging.handlers import TimedRotatingFileHandler

#форматер
_log_format = f"%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"

#уровень ERROR
def get_file_handler():
    file_handler = logging.FileHandler("server.log")
    file_handler.setLevel(logging.ERROR)
    file_handler.setFormatter(logging.Formatter(_log_format))
    return file_handler

#уровень INFO
def get_stream_handler():
    stream_handler = logging.FileHandler("server.log")
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(logging.Formatter(_log_format))
    return stream_handler

#уровень DEBUG
def get_stream_handler():
    stream_handler = logging.FileHandler("server.log")
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(logging.Formatter(_log_format))
    return stream_handler

#уровень WARNING
def get_stream_handler():
    stream_handler = logging.FileHandler("server.log")
    stream_handler.setLevel(logging.WARNING)
    stream_handler.setFormatter(logging.Formatter(_log_format))
    return stream_handler



#общая обработка + ротация
def get_logger(name):
    logger = logging.getLogger('app.server')
    logger.setLevel(logging.INFO)
    logger.addHandler(get_file_handler())
    logger.addHandler(get_stream_handler())
    handler = TimedRotatingFileHandler("server.log", when='d', interval=1, backupCount=5)
    logger.addHandler(handler)
    return logger



