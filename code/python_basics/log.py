import os
import logging
import time
from pythonjsonlogger import jsonlogger


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        log_record['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(record.created))
        log_record['level'] = record.levelname


class Logger(logging.Logger):
    def __init__(self):
        super(Logger, self).__init__('')
        type = os.getenv('LOG_TYPE', 'raw')
        level = os.getenv('LOG_LEVEL', 'DEBUG')
        if type == 'raw':
            formatter = logging.Formatter(fmt='%(asctime)s - %(module)s - %(funcName)s - %(levelname)s - %(message)s',
                                          datefmt='%Y/%m/%d %H:%M:%S')
        elif type == 'json':
            formatter = CustomJsonFormatter('(timestamp) (level) (module) (funcName) (lineno) (message)')
        log_handler = logging.StreamHandler()
        log_handler.setFormatter(formatter)
        log_handler.setLevel(level)
        self.addHandler(log_handler)


logger = Logger()


def test():
    logger.info('hello')
    logger.debug('hi')
    logger.error('err')


if __name__ == '__main__':
    logger.info('hello')
    logger.debug('hi')
    logger.error('Hello %s, %s!', 'World', 'Congratulations')
    test()
