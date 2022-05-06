from configparser import ConfigParser
import logging
import hashlib
from random import randint
import os

# 获取当前工作目录
WORK_PATH = os.path.split(os.path.realpath(__file__))[0]
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


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
for logger_handler in logger.handlers:
    logger.removeHandler(logger_handler)

log_status = logging.DEBUG

consloe_log = logging.StreamHandler()
consloe_log.setLevel(log_status)
consloe_log.setFormatter(__format_switch(debug_status='true'))

logger.addHandler(consloe_log)

if not os.path.exists(WORK_PATH + '/logs'):
    try:
        os.mkdir(WORK_PATH + '/logs')
    except OSError:
        logger.warning('创建日志文件失败，请尝试手动在当前目录下创建 logs 目录（文件夹）')

# 配置文件初始化
coon = ConfigParser()
if not os.path.exists(WORK_PATH + '/setting.ini'):
    logger.warning('找不到配置文件！请务必将自带的setting.ini放置于软件同一目录下')
    raise FileNotFoundError('未能找到配置文件，请务必将自带的setting.ini放置于软件同一目录下')
coon.read(WORK_PATH + '/setting.ini',encoding='utf-8')


# 设置LOGGING
def __save_log(mark=None):
    """
    保存日志
    :param mark: 标记，默认为None时将为随机数
    :return: logging.FileHandler()
    """
    file_name = hashlib.md5(bytes(randint(1000, 9999))).hexdigest()
    file_log = logging.FileHandler(filename=WORK_PATH + '/logs/' + file_name + '.log')
    file_log.setFormatter(__format_switch(debug_status=coon.get('logging', 'debug')))
    file_log.setLevel(log_status)

    logger.info(f'日志保存已启用，保存名为：{file_name}.log')
    return file_log

# 刷新和添加Handler
consloe_log.setFormatter(__format_switch(debug_status=coon.get('logging', 'debug')))
consloe_log.setLevel(log_status)

logger.addHandler(consloe_log)
if coon.get('logging','file_save') == 'true':
    logger.addHandler(__save_log())

# DEBUG 提醒
if log_status == logging.DEBUG:
    logger.info('注意：已启动DEBUG模式，如需关闭请在同目录下 setting.ini 文件中将 logging中debug 选项更改为 false')

# ADMIN-KEY
ADMIN_KEY = coon.get('web','admin-key')
FIRST_USE = False
if ADMIN_KEY == 'None':
    FIRST_USE = True
    logger.info('你的ADMIN-KEY已自动设置，请前去 setting.ini 文件或管理界面查看&修改')
    coon.set('web','admin-key',hashlib.md5(bytes(randint(1000, 9999))).hexdigest())
    coon.write(open(WORK_PATH + '/setting.ini','w',encoding='utf-8'))