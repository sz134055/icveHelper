from time import strftime, localtime
from configparser import ConfigParser
import logging
from os.path import join, split, exists, realpath
from os import mkdir

# 获取当前工作目录
WORK_PATH = split(realpath(__file__))[0]

# 初始化错误日志名
LOG_FILE_NAME = ''


# 初始化LOGGING
def __format_switch(debug_status=None):
    global log_status
    if not debug_status:
        debug_status = coon.get('logging', 'debug')

    if debug_status == 'true':
        # log_status = logging.DEBUG
        return logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
    elif debug_status == 'false':
        log_status = logging.INFO
        return logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
    else:
        logger.warning('你的设置文件LOGGING选项有错误，请务必为 true 或 flas，当前已默认视为选中 true')


def __save_log():
    """
    保存日志
    :return: logging.FileHandler()
    """
    global LOG_FILE_NAME
    file_name = strftime('%Y-%m-%d_%H-%M-%S', localtime())
    LOG_FILE_NAME = join(WORK_PATH, 'logs', file_name + '.log')
    file_log = logging.FileHandler(filename=LOG_FILE_NAME)
    # file_log.setFormatter(__format_switch(debug_status=coon.get('logging', 'debug')))
    file_log.setFormatter(__format_switch('true'))
    file_log.setLevel(log_status)

    logger.info(f'日志保存已启用，保存名为：{file_name}.log')
    return file_log


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
for logger_handler in logger.handlers:
    logger.removeHandler(logger_handler)

log_status = logging.DEBUG

'''
consloe_log = logging.StreamHandler()
consloe_log.setLevel(log_status)
consloe_log.setFormatter(__format_switch(debug_status='true'))
'''

# logger.addHandler(consloe_log)

'''
if not exists(join(WORK_PATH, 'logs')):
    try:
        mkdir(join(WORK_PATH, 'logs'))
    except OSError:
        logger.warning('创建日志文件失败，请尝试手动在当前目录下创建 logs 目录（文件夹）')

# 配置文件初始化
coon = ConfigParser()
if not exists(join(WORK_PATH, 'setting.ini')):
    logger.warning('找不到配置文件！请务必将自带的setting.ini放置于软件同一目录下')
    raise FileNotFoundError('未能找到配置文件，请务必将自带的setting.ini放置于软件同一目录下')
coon.read(join(WORK_PATH, 'setting.ini'), encoding='utf-8')


# 配置文件更新函数
def conf_update(section, key, value):
    coon.set(section, key, value)
    coon.write(open(join(WORK_PATH, 'setting.ini'), 'w', encoding='utf-8'))


logger.addHandler(__save_log())
'''