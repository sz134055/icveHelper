import requests
from requests import utils
import os.path
import time
import hashlib
import logging
from configparser import ConfigParser
from random import randint

# 一些初始化设置
requests.packages.urllib3.disable_warnings()
WORK_PATH = os.path.split(os.path.realpath(__file__))[0]

# 初始化Logger
log = logging.getLogger()
log.setLevel(logging.DEBUG)
for logger_handler in log.handlers:
    log.removeHandler(logger_handler)

# 控制台输出
__consloe_log = logging.StreamHandler()
__consloe_log.setLevel(logging.DEBUG)
__consloe_log.setFormatter(
    logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s'))
log.addHandler(__consloe_log)

# 文件输出
if not os.path.exists(WORK_PATH + '/logs'):
    try:
        os.mkdir(WORK_PATH + '/logs')
    except OSError:
        log.warning('创建日志文件失败，请尝试手动在当前目录下创建 logs 目录（文件夹）')

__file_log = logging.FileHandler(filename='{0}/logs/{1}.log'.format(
    WORK_PATH,
    time.strftime('%Y-%m-%d %H-%M-%S', time.localtime(time.time()))
    # hashlib.md5(bytes(randint(1000, 9999))).hexdigest()
))
__file_log.setFormatter(logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s'))
__file_log.setLevel(logging.DEBUG)
log.addHandler(__file_log)

log.info('初始化完成')


class ReqError(Exception):
    pass


class BaseReq:
    def __init__(self):
        self.__headers = {
            'Accept': '*/*',
            'Accept-Language': 'zh-Hans-CN;q=1.0',
            'Accept-Encoding': 'gzip;q=1.0, compress;q=0.5',
        }
        self.__s = requests.session()
        self.__s.verify = False

        self.__data = {}  # 默认加载的表单
        self.__params = {}  # 默认加载的参数

        # 内部自维护的实时消息，当调用例如request请求发生意外结果时会尝试从此获取状态以防止程序崩溃
        self.info = {
            'code': '',
            'msg': ''
        }

        # API池
        self.apis = {}

        # Cookies池
        self.cookies = {}

    def update_header(self, info: dict):
        try:
            self.__headers.update(info)
        except Exception as e:
            log.error('在尝试更新请求头时发生错误：' + e)

    def set_agent(self,agent):
        self.update_header({
            'User-Agent':agent
        })

    def new_info(self, code, msg):
        self.info.update({
            'code': code,
            'msg': msg
        })

    def req(self, method: str, api=None, data={}, params={}, url=None):
        # 处理URL
        if not url and api:
            self.new_info('0', '没有请求的链接')
            raise ReqError('没有请求的链接')
        elif api and not url:
            try:
                url = self.apis[api]
            except KeyError:
                self.new_info('0', '尝试获取指定的API失败')
                raise ReqError('尝试获取指定的API失败')
        else:
            # 处理METHOD
            REQ_METHOD = None
            if method.upper() == 'GET' or method.upper() == 'G':
                REQ_METHOD = 'GET'
            elif method.upper() == 'POST' or method.upper() == 'P':
                REQ_METHOD = 'POST'
            else:
                self.new_info('0', '意外的请求方式')
                raise ReqError('意外的请求方式')

        # 处理data和params
        if data or params:
            try:
                the_data = self.__data.copy()
                the_data.update(data)
                the_params = self.__params.copy()
                the_params.update(params)
            except TypeError:
                self.new_info('0', '在处理表单和参数时发生错误')
                raise ReqError('在处理表单和参数时发生错误')

        if REQ_METHOD:
            return self.__s.request(
                method=REQ_METHOD
                , url=url
                , data=the_data
                , params=the_params
            )

    def get(self, api=None, data={}, params={}, url=None):
        return self.req('g', api, data, params, url)

    def post(self, api=None, data={}, params={}, url=None):
        return self.req('p', api, data, params, url)



class User(BaseReq):
    def __init__(self):
        super().__init__()

        self.__login_info = {
            'appVersion':'2.8.43',
            'clientId':'',
            'equipmentApiVersion':'',
            'equipmentAppVersion':'',
            'equipmentModel':'',
            'userName':'',
            'userPwd':''
        }

    def set_account(self,account:str,pswd:str):
        self.__login_info.update({
            'userName':account,
            'userPwd':pswd
        })

    def set_device(self,name:str,version:str):
        self.__login_info.update({
            'equipmentModel':name,
            'equipmentApiVersion':version
        })

    def set_app(self,version:str,os_type:str):
        self.__login_info.update({
            'equipmentAppVersion':version,
            'appVersion':version
        })
        if os_type.upper() == 'IOS':
            self.update_header({
                'User-Agent': 'yktIcve/{0} (com.66ykt.66yktteacherzhihui; build:{1}; iOS {2})'.format(
                    '2.8.43',
                    '2021042101',
                    version
                )
            })
        else:
            self.update_header({
                'User-Agent':'okhttp/4.5.0'
            })



class Course:
    def __init__(self):
        pass


class Mooc:
    def __init__(self):
        pass


class Task:
    def __init__(self):
        pass


class Tool:
    def __init__(self):
        pass
