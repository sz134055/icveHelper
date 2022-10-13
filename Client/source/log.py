from time import strftime, localtime
import logging
from os.path import join, split, exists, realpath
from os import mkdir


def get_logger():
    # 获取当前工作目录
    work_path = split(realpath(__file__))[0]
    # 创建目录
    if not exists(join(work_path, 'logs')):
        try:
            mkdir(join(work_path, 'logs'))
        except OSError:
            raise OSError('创建日志文件失败，请尝试手动在当前目录下创建 logs 目录（文件夹）')

    file_name = strftime('%Y-%m-%d_%H-%M-%S', localtime())
    log_file_path = join(work_path, 'logs', file_name + '.log')
    file_log = logging.FileHandler(filename=log_file_path,encoding='utf-8')
    # file_log.setFormatter(__format_switch(debug_status=coon.get('logging', 'debug')))
    file_log.setFormatter(logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s'))
    file_log.setLevel(logging.DEBUG)

    log = logging.getLogger()
    for logger_handler in log.handlers:
        log.removeHandler(logger_handler)

    log.addHandler(file_log)

    return log
