from os.path import exists
from web import get_now_path
from configparser import ConfigParser


# 配置文件读取
def __get_coon():
    if not exists(get_now_path() + '/setting.ini'):
        raise FileNotFoundError('未能找到一个名为 setting.ini 的配置文件！')
    c = ConfigParser()
    c.read(get_now_path() + '/setting.ini', encoding='utf-8')
    return c


coon = __get_coon()
