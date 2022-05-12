import time
import logging
from web import get_now_path

class Logger:
    handlers_list = []

    def __init__(self, debug_status=True,name='', console=True, file=False):

        self.log_level = logging.INFO

        self.name = name
        if name:
            self.name = '['+name+']'

        self.update_status(debug_status)

        self.update_method(console, file)

    def update_status(self, status):
        if status == 'development' or status:
            # 启用DEBUG
            self.log_level = logging.DEBUG

    def update_method(self, console, file):
        if console:
            self.__console_log()
        if file:
            self.__file_log()

    def __format_switch(self):
        if self.log_level == logging.DEBUG:
            return logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
        else:
            # logging.INFO
            return logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')

    def __file_log(self):
        file_name = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())
        if self.name:
            file_name = self.name+file_name
        file_log = logging.FileHandler(filename=get_now_path() + '/logs/' + file_name + '.log')
        file_log.setFormatter(self.__format_switch())
        file_log.setLevel(self.log_level)

        self.handlers_list.append(file_log)

    def __console_log(self):
        console_log = logging.StreamHandler()
        console_log.setLevel(self.log_level)
        console_log.setFormatter(self.__format_switch())

        self.handlers_list.append(console_log)

    def get_logger(self):
        logger = logging.getLogger()
        logger.setLevel(self.log_level)
        # 重置
        for logger_handler in logger.handlers:
            logger.removeHandler(logger_handler)

        # 添加Handlers
        for handler in self.handlers_list:
            logger.addHandler(handler)

        return logger