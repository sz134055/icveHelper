from random import uniform, randint
import requests
from requests import utils
import time
import hashlib
from json.decoder import JSONDecodeError
from json import load as json_load
from json import dump as json_dump
from time import strftime, localtime
import logging
# from . import logger
# from sys import _getframe
from uuid import uuid4
from urllib import parse

requests.packages.urllib3.disable_warnings()
from os.path import join, split, exists, realpath
from os import mkdir

# 初始化requests
# s = requests.session()
# s.verify = False

"""
信息返回 dict
code：int 状态码
    - 0 一切正常
    - -1 致命错误
    - 1 正常请求但是内部发生异常
msg：str 返回信息
data：dict 返回数据
"""


class Logs:
    def __init__(self):

        # self.work_path = split(realpath(__file__))[0]
        self.log_path = self.__log_dir_init()
        self.IS_PATH_NORMAL = True

    def __log_dir_init(self):
        # 创建目录
        if not exists('./logs'):
            try:
                mkdir('./logs')
                return './logs'
            except OSError:
                self.IS_PATH_NORMAL = False
                return './'
        else:
            return './logs'

    def get_logger(self):
        logging.basicConfig(level=logging.DEBUG)

        file_name = strftime('%Y-%m-%d_%H-%M-%S', localtime())
        log_file_path = join(self.log_path, file_name + '.log')
        file_log = logging.FileHandler(filename=log_file_path, encoding='utf-8')
        file_log.setFormatter(
            logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s'))

        log = logging.getLogger()
        for logger_handler in log.handlers:
            log.removeHandler(logger_handler)

        log.addHandler(file_log)

        if not self.IS_PATH_NORMAL:
            log.warning('创建日志文件失败，请尝试手动在当前目录下创建 logs 目录（文件夹）；目前日志将会被保存在程序同目录下')

        return log


logger = Logs().get_logger()


class CONF:
    # 配置文件初始信息
    BASE_INFO = {
        'icve_version': {
            'android': {'version': '4.5.0', 'build': ''},
            'ios': {'version': '2.8.43', 'build': '2021042101', }
        },
        'api': {
            'login': 'https://zjyapp.icve.com.cn/newMobileAPI/MobileLogin/newSignIn',
            'all_course': 'https://zjyapp.icve.com.cn/newMobileAPI/Student/getCourseList_new',
            'all_module': 'https://zjyapp.icve.com.cn/newMobileAPI/AssistTeacher/getModuleListByClassId',
            'all_topic': 'https://zjyapp.icve.com.cn/newMobileAPI/AssistTeacher/getTopicListByModuleId',
            'all_cell': 'https://zjyapp.icve.com.cn/newMobileAPI/AssistTeacher/getCellListByTopicId',
            'all_comment': 'https://zjyapp.icve.com.cn/newMobileAPI/BBS/getCellBBSList',
            'add_comment': 'https://zjyapp.icve.com.cn/newMobileAPI/BBS/addCellComment',
            'change_sign': 'https://zjyapp.icve.com.cn/newMobileAPI/FaceTeach/changeSignType',
            'get_answer': 'https://zjyapp.icve.com.cn/newMobileAPI/Homework/getHomeworkStuRecord',
            'all_class': 'https://zjyapp.icve.com.cn/newMobileAPI/FaceTeach/getAllFaceTeachListByStu',
            'get_active': 'https://zjyapp.icve.com.cn/newMobileAPI/faceTeach/getStuFaceActivityList',
            'class_comment': 'https://zjyapp.icve.com.cn/newMobileAPI/FaceTeach/getstuEvaluationInfo',
            'self_comment': 'https://zjyapp.icve.com.cn/newMobileAPI/FaceTeach/getFaceTeachSelfEvaluation',
            'cell_info': 'https://zjyapp.icve.com.cn/newMobileAPI/AssistTeacher/getCellInfoByCellId',
            'cell_info_new': 'https://zjy2.icve.com.cn/api/common/Directory/viewDirectory',
            'finish_cell': 'https://zjy2.icve.com.cn/api/common/Directory/stuProcessCellLog'
        }
    }

    def __init__(self):
        self.conf = self.__get_config()

    def __get_config(self) -> dict:
        """
        初始化配置文件

        如果没有配置文件将会创建，并将自带的信息导入
        如果有配置文件会以配置文件内容为准

        :return: 配置文件内容
        """
        try:
            f = open('setting.json')
            conf = json_load(f)
            f.close()
            return conf
        except FileNotFoundError:
            f = open('setting.json', 'w+')
            # 初始信息填入
            json_dump(self.BASE_INFO, f, ensure_ascii=False)
            f.close()
            return self.__get_config()

    def get_icve_version(self) -> dict:
        """
        获取ICVE设备类型UA信息

        :return: ICVE设备类型UA信息
        """
        return self.conf['icve_version']

    def get_apis(self) -> dict:
        """
        获取ICVE API列表

        :return: ICVE API列表
        """
        return self.conf['api']


# 全局配置文件对象
conf = CONF()


class BaseReq:
    # 职教云版本信息
    icve_version = conf.get_icve_version()

    # API Collection
    apis = conf.get_apis()

    def __init__(self):
        self.the_headers = {
            'Host': 'zjyapp.icve.com.cn',
            'Accept': '*/*',
            'Accept-Language': 'zh-Hans-CN;q=1.0',
            'Accept-Encoding': 'gzip;q=1.0, compress;q=0.5',
        }
        # REQ
        self.s = requests.session()
        self.s.verify = False

    def get_headers(self, update_item: dict = None, new: bool = True, ) -> dict:
        """
        获取Headers

        :param update_item: 需要更新进Headers的信息
        :param new: 默认为True，此会返回一个新的Headers，不会影响类本事的Headers，如若为False，则可利用为更新类Headers
        :return: Headers
        """
        if new:
            header = self.the_headers.copy()
        else:
            header = self.the_headers

        if update_item:
            header.update(update_item)

        return header

    def request(self, url: str, header: dict = None, params: dict = None, data: dict = None,
                timeout: int = None) -> dict:
        if not header:
            # 返回默认Header
            header = self.get_headers()

        req_method = 'GET'
        if data:
            req_method = 'POST'

        res = self.s.request(method=req_method, url=url, headers=header, params=params, data=data, timeout=timeout)
        if res.status_code == 200:
            try:
                res_json = res.json()
                logger.info(f"请求成功 -> {url}")
                return {"code": 0, "msg": "请求成功", "data": res_json}
            except JSONDecodeError:
                logger.warning(f"请求成功但是解析为JSON失败 -> {url}")
                return {"code": 1, "msg": "请求成功，但是JSON解析失败", "data": {"content": res.text}}
        else:
            logger.warning(f"请求失败->{url}；[{res.status_code}]响应内容：{res.text}")
            return {"code": -1, "msg": f"[{res.status_code}]响应内容：{res.text}", "data": {}}

    @property
    def req_cookies(self):
        """
        返回Cookies（RequestsCookieJar）

        :return: Cookies（RequestsCookieJar）
        """
        return self.s.cookies

    def req_flash(self, req) -> None:
        """
        替换当前的requests.session()对象

        :param req: requests.session()对象
        :return: None
        """
        self.s = req

    def req_clear_cookies(self) -> None:
        """
        清除Cookies

        :return: None
        """
        self.s.cookies.clear()

    @property
    def req_headers(self) -> dict:
        """
        返回Headers

        :return: Headers
        """
        return self.the_headers


def login_check(func):
    """
    登录检查装饰器

    原理为如若发生KeyError则说明登录后的信息未导入，说明未登录
    """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            logger.warning('用户未登录或登录失效导致操作失败')
            return {'code': -1, 'msg': '未登陆！', 'data': {}}

    return wrapper


class User(BaseReq):
    def __init__(self):
        """
        User类，处理ICVE用户账户相关

        """
        # REQ
        super().__init__()

        self.device_type = ''
        self.login_info = self.__login_init()
        # user_info
        self.user_info = {}
        self.user_info.update(self.login_info)

        self.ua_switch()
        # self.login()

        # SAVE_PATH
        self.__save_file_path = self.__save_init()

    def __login_init(self) -> dict:
        """
        初始化登录信息

        login_info: {
            appVersion:职教云版本    //暂时无用
            clientId:clientId
            equipmentApiVersion:设备系统版本号
            equipmentAppVersion:职教云版本      //暂时无用
            equipmentModel:设备名称
            userName:职教云账号
            userPwd:职教云密码
            }

        :return: 登录信息 login_info
        """
        # 默认登录信息
        login_form = {
            'appVersion': conf.get_icve_version()['ios']['version'],
            'clientId': '',
            'equipmentApiVersion': '15.0',
            'equipmentAppVersion': conf.get_icve_version()['ios']['version'],
            'equipmentModel': 'iPhone 11',
            'userName': '',
            'userPwd': ''
        }
        return login_form

    def login_setting(self, login_info: dict) -> None:
        """
        更新登录信息，推荐如下：

         login_info: {
            appVersion:职教云版本    //暂时无用
            clientId:clientId
            equipmentApiVersion:设备系统版本号
            equipmentAppVersion:职教云版本      //暂时无用
            equipmentModel:设备名称
            userName:职教云账号
            userPwd:职教云密码
            }

        :param login_info: 登录信息
        :return: None
        """

        # 更新
        if login_info['equipmentModel'] and login_info['equipmentApiVersion']:
            self.login_info.update(login_info)
            self.ua_switch()
            self.user_info.update(self.login_info)
        else:
            del login_info['equipmentApiVersion']
            del login_info['equipmentModel']
            self.login_info.update(login_info)
            self.user_info.update(self.login_info)

    def __save_init(self) -> str:
        """
        初始化存档目录，不存在则创建，并最终返回目录位置

        :return: 目录位置（相对路径）
        """
        save_path = ''
        if not exists('save'):
            logger.info('不存在 save 目录，将会创建')
            try:

                mkdir('save')
                save_path = 'save/'

                logger.info('成功创建 save 目录')
            except OSError:
                logger.warning('创建存档save目录失败，请管理员打开或手动创建 save 目录')
            finally:
                logger.info(f'存档目录 -> {save_path}')

                return save_path
        else:
            logger.info('存档目录 -> save/')
            return 'save/'

    def save_login(self, account: str, save_info: dict):
        save_name = join(self.__save_file_path, account + '.json')
        try:
            with open(save_name, 'w+', encoding='utf-8') as f:
                json_dump(save_info, f, ensure_ascii=False)
                logger.info(f'成功保存账户 {account} 存档')
        except Exception as e:
            logger.exception(f'在保存用户 {account} 存档时发生异常：{e}')

    def get_save(self, account: str) -> dict | None:
        """
        读取一个账号的保存信息，存在返回，不存在返回None

        :param account: ICVE账号
        :return: 查询到的信息或None
        """
        try:
            with open(join(self.__save_file_path, account + '.json'), 'r', encoding='utf-8') as f:
                logger.info(f'读取到账户 {account} 的存档信息')
                return json_load(f)
        except FileNotFoundError:
            logger.info(f'未能读取到账户 {account} 的存档信息')
            return None

    def ua_switch(self) -> str:
        """
        用于切换请求头中User-Agent当设备为iOS或Android时的情况

        :return: 会返回当前请求头中User-Agent，以供参考
        """

        type_name = self.login_info['equipmentModel']

        if 'iphone' or 'ios' in type_name.lower():
            # iOS
            self.device_type = 'ios'
            if len(self.login_info['equipmentApiVersion']) < 6:
                # 短版本号补0
                self.login_info['equipmentApiVersion'] += '.0'
            self.get_headers({
                'User-Agent': 'yktIcve/{0} (com.66ykt.66yktteacherzhihui; build:{1}; iOS {2})'.format(
                    self.icve_version['ios']['version'], self.icve_version['ios']['build'],
                    self.login_info['equipmentApiVersion'])
            }, False)
        else:
            # Android
            self.device_type = 'android'
            self.get_headers({
                'User-Agent': 'okhttp/{0}'.format(self.icve_version['android']['version'])
            }, False)

        return self.get_headers()['User-Agent']

    def gen_client_id(self) -> str:
        new_uuid = uuid4()
        new_uuid = str(new_uuid).replace('-', '')
        logger.info(f'生成ClientID(UUID4)->{new_uuid}')
        return new_uuid

    def login(self, account: str = None, pswd: str = None) -> dict:
        """
        登陆至ICVE（模拟APP登录），登陆后会同步登录信息并返回登录状态及用户的相关信息

        :param account: 职教云账号
        :param pswd: 职教云密码
        :return: 登陆状态和用户信息
        """

        def get_device(emit: str) -> str:
            """
            生成请求头中device token

            device token生成说明：
            需要按顺序准备 设备名，设备系统版本号，职教云版本号，时间戳 四项
            然后依次加密：
            加密内容 = MD5加密(加密内容+下一项)

            :param emit: 时间戳
            :return: 加密后的device token
            """

            def md5it(content: str = None) -> str:
                """
                MD5加密

                :param content: 加密对象
                :return: 加密后的内容
                """
                if content:
                    md5 = hashlib.md5()
                    md5.update(content.encode("utf-8"))
                    return md5.hexdigest()
                else:
                    return ''

            # need_info = [设备名，设备系统版本号，职教云版本号，时间戳]，最后一项留空保证最后有效项被加上后的结果得到再次加密
            need_info = [self.login_info['equipmentModel'], self.login_info['equipmentApiVersion'],
                         self.icve_version[self.device_type]['version'], emit, '']
            device_id = ''
            for need_item in need_info:
                device_id = md5it(device_id) + need_item
            # device_id = md5it(device_id)  # 最终加密结果

            return device_id

        # 账号判断
        if not account and not self.login_info['userName']:
            logger.info('未能登录，因为未输入账户')
            return {'code': 1, 'msg': '未能登录，因为未输入账户', 'data': {}}
        elif not self.login_info['userName'] and account:
            self.login_info.update({'userName': account})

        # 密码判断
        if not pswd and not self.login_info['userPwd']:
            logger.info('未能登录，因为未输入密码')
            return {'code': 1, 'msg': '未能登录，因为未输入密码', 'data': {}}
        elif not self.login_info['userPwd'] and pswd:
            self.login_info.update({'userPwd': pswd})

        # CLIENT ID
        if not self.login_info['clientId']:
            self.login_info.update({'clientId': self.gen_client_id()})
            self.user_info.update(self.login_info)

        # FORM LOAD
        login_form = self.login_info.copy()
        login_form.update({
            'sourceType': '3'
        })

        # EMIT
        emit = str(int(time.time())) + '000'
        # DEVICE ID
        device_id = get_device(emit)
        header = self.get_headers(update_item={
            'emit': emit,
            'device': device_id,
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'
        })

        res = self.request(url=self.apis['login'], header=header, data=login_form)
        if res['code'] == -1:
            logger.warning(f'登录时发生问题：{res["msg"]}')
            return res
        elif res['code'] == 1:
            logger.warning(f'登录可能失败；服务器响应：{res["data"]["content"]}')
            return {'code': 1, 'msg': f'登录可能失败；服务器响应：{res["data"]["content"]}'}
        else:
            res_json = res['data']
            if res_json['code'] == 1:
                # 登陆成功
                # 更新user_info
                self.user_info.update({
                    'userType': res_json['userType'],  # 用户类别，已知1为学生
                    'userId': res_json['userId'],  # 用户ID
                    'newToken': res_json['newToken'],  # Token
                    'displayName': res_json['displayName'],  # 用户姓名
                    'employeeNumber': res_json['employeeNumber'],  # 用户学号（或其他工号）
                    'url': res_json['url'],  # 用户头像URL
                    'schoolName': res_json['schoolName'],  # 用户所在学校名
                    'schoolId': res_json['schoolId'],  # 用户所在学校ID
                    'cookies': utils.dict_from_cookiejar(self.req_cookies)  # dict Cookies
                })
                logger.info(f'登录成功 -> 学号：{self.user_info["employeeNumber"]}')
                # 存档
                save_info = {
                    'account': self.login_info['userName'],
                    'info': self.user_info,
                    'login_time': time.time()
                }
                self.save_login(self.login_info['userName'], save_info)
                return {'code': 0, 'msg': '登陆成功！', 'data': {"token": self.user_info['newToken']}}
            else:
                # 失败
                logger.warning(f'登录失败；服务器响应：{res_json["msg"]}')
                return {'code': 1, 'msg': res_json['msg'], 'data': {}}


    @property
    @login_check
    def name(self) -> str:
        """
        用户姓名

        :return: 用户姓名
        """
        return self.user_info['displayName']

    @property
    @login_check
    def id(self) -> str:
        """
        用户ID

        :return: 用户ID
        """
        return self.user_info['userId']

    @property
    @login_check
    def token(self) -> str:
        """
        用户TOKEN

        :return: 用户TOKEN
        """
        return self.user_info['newToken']

    @property
    @login_check
    def user_header_url(self) -> str:
        """
        用户头像

        :return: 用户头像URL
        """
        return self.user_info['url']

    @property
    @login_check
    def type(self) -> str:
        """
        用户类型

        :return: 用户类型：学生或老师
        """
        if self.user_info['userType'] == '1':
            return '学生'
        else:
            return '教职工'

    @property
    @login_check
    def number(self) -> str:
        """
        用户的工号

        :return: 学工号
        """
        return self.user_info['employeeNumber']

    @property
    @login_check
    def school_info(self) -> dict:
        """
        用户所在学校信息

        返回示例：{
            name: 学校名,
            id: 学校ID
        }

        :return: dict 包含学校名和ID
        """
        return {
            'name': self.user_info['schoolName'],
            'id': self.user_info['schoolId']
        }

    '''
    @property
    @login_check
    def cookies(self) -> dict:
        """
        返回COOKIES

        :return: dict cookies
        """
        return self.user_info['cookies']


    @property
    @login_check
    def req(self):
        """
        返回requests.session()
        
        :return: 包含登陆后所需信息的requests.session()
        """
        # 触发login_check
        self.user_info['cookies']

        return self.__s
    '''

    @login_check
    def my_courses(self):
        """
        获取课程

        :return: 返回Course对象
        """
        course = Course()
        course.set_user(self.user_info, self.s)
        course.req_flash(self.s)
        course.get_headers({
            "Cookie": f"auth={utils.dict_from_cookiejar(self.s.cookies)['auth']};acw_tc={utils.dict_from_cookiejar(self.s.cookies)['acw_tc']}"},
            False)
        course.get_headers(self.req_headers, new=False)
        logger.info('获取课程对象')
        return course


class Course(BaseReq):
    def __init__(self):
        super().__init__()
        # self.user = None
        # self.__s = user.req
        self.user_info = None
        # 公用PAYLOAD
        self.the_pay_load = {}

        # TASK进度信息
        self.task_process = {
            'name': '',
            'id': '',
            'total': 0,
            'now': 0
        }

        self.progress = None  # RICH 进程
        self.progress_task = None

    def set_user(self, user_info: dict, user_req: requests.session()) -> None:
        self.req_flash(user_req)
        self.user_info = user_info
        # 更新公用PAYLOAD
        self.the_pay_load = {
            'sourceType': '3',
            'stuId': self.user_info['userId'],
            'newToken': self.user_info['newToken']
        }

    @property
    def process_now(self) -> int:
        """
        返回当前任务进度

        :return: 当前任务进度
        """
        return self.task_process['now']

    @property
    def process_total(self) -> int:
        """
        返回当前任务的总进度

        :return: 当前任务总进度
        """
        return self.task_process['total']

    @property
    def process_name(self) -> str:
        """
        返回当前任务名

        :return: 当前任务名
        """
        return self.task_process['name']

    @property
    def process_id(self) -> str:
        """
        返回当前任务ID

        :return: 当前任务ID
        """
        return self.task_process['id']

    def process_hook(self, func):
        pass

    def process_update(self, target_name: str, target_id: str, now_process: int | float,
                       total_process: int | float = None) -> int:
        """
        用于更新任务进度信息，并返回最新的任务进度

        根据以下情况提供不同功能：
        - 任务名和ID 与当前任务进度匹配时，仅会更新当前进度信息（即同步now_process至任务进度）
        - 任务名与ID 中任意一项与当前任务不匹配，且总进度不为空时，会更新全部信息，即切换至新输入的任务

        当不符合上列情况时，返回 -1

        :param target_name: 任务名
        :param target_id: 任务ID
        :param now_process: 更新当前进度的值
        :param total_process: 更新当前总进度的值
        :return: 当前任务进度
        """
        if target_name and target_id and self.task_process['name'] == target_name and self.task_process[
            'id'] == target_id:
            self.task_process.update({'now': now_process})
            logger.info(f'更新当前任务{self.process_name}({self.process_id})进度为[{self.process_now}/{self.process_total}]')
            return self.process_now
        elif total_process:
            # 任务切换
            self.task_process.update({
                'name': target_name,
                'id': target_id,
                'total': total_process,
                'now': now_process
            })
            logger.info(f'任务信息切换至->{self.process_name}({self.process_id})[{self.process_now}/{self.process_total}]')
            return self.process_now
        else:
            logger.warning('找不到指定任务或切换为新任务时候未指定总进度')
            return self.process_now

    '''
    # 用于设置RICH进程
    def set_progress(self, progress):
        self.progress = progress

    # 用于添加RICH进程任务
    def set_progress_task(self, task):
        self.progress_task = task

    '''

    @property
    def all_course(self) -> list[dict]:
        """
        获取所有在修课程列表，列表中包含了课程及对应的信息，不包括MOOC

        返回示例：

        [{
            courseOpenId: 课程ID,

            courseName: 课程名,

            url: 课程封面图片URL路径,

            openClassName: 开课班级（可能为列表）,

            openClassId: 开课班级,

            mainTeacherName: 课程老师,

            mainTeacherNum: 课程老师工号,

            process: 课程学习进度,

            totalScore: 课程得分,

            InviteCode: 当前课程所在班级邀请码

        }...]


        说明：

        - 仅返回较为有用信息，例如开课老师和带课老师中仅返回带课老师，因为大部分情况二者为一人
        - 开课班级及对应ID，应理解为该课程为某班，如XX2022班开设了一个班级，这个班级有一个对应ID，因此每个课程对任一用户都有一个班级，即使该用户实际为XX2022班学生，这就是为什么不同课程开课班级都为XX2022班，但是ID与邀请码均不同的原因
        - 开课班级可能为列表，例如该课程在XX20221和XX20222班均开设，老师在设置时可能就会将两班级填入，因此班级请以班级ID为准

        :return: 在修课程列表
        """

        pay_laod = self.the_pay_load.copy()
        pay_laod.update({
            'isPass': '0',
            'page': '1',
        })
        course_list = []

        while True:
            res = self.request(url=self.apis['all_course'], params=pay_laod)
            if res['code'] == 0:
                res_json = res['data']
                if res_json['code'] == 1:
                    c_list = res_json['dataList']
                    if len(c_list) < 1:
                        break
                    else:
                        for c in c_list:
                            course_list.append({
                                'courseOpenId': c['courseOpenId'],
                                'courseName': c['courseName'],
                                'url': c['thumbnail'],
                                'openClassName': c['openClassName'],
                                'openClassId': c['openClassId'],
                                'mainTeacherName': c['mainTeacherName'],
                                'mainTeacherNum': c['mainTeacherNum'],
                                'process': c['process'],
                                'totalScore': c['totalScore'],
                                'InviteCode': c['InviteCode']
                            })
                        # 更新page
                        pay_laod['page'] = str(int(pay_laod['page']) + 1)
                        continue
                else:
                    logger.warning(f'未能尝试获取课程列表：{res_json["msg"]}->{res["data"]}')
                    break
            else:
                logger.warning(f'尝试获取课程列表发生错误:{res["msg"]}->{res["data"]}')
                break
        return course_list

    def courseware(self, api: str, params: dict) -> dict | list | None:
        """
        [TOOL]工具方法，用于后续课件相关的操作的预处理

        :param api: 指定的API URL
        :param params: 指定附带的URL参数
        :return: 返回除 code 和 msg 外的回调信息
        """
        res = self.request(url=api, params=params)

        if res['code'] == 0:
            res_json = res['data']
            try:
                if res_json['code'] == 1:
                    # return res_json[res_json.keys()[1]]

                    del res_json['code']
                    del res_json['msg']
                    for d in res_json.values():
                        return d
                else:
                    logger.warning(f'未能成功获取：{res_json["msg"]}')
                    return None
            except Exception as e:
                logger.exception(f'COUSEWARE工具方法出现处理异常，原始响应：{res} 异常：{e}')
                return None
        else:
            logger.warning(f'课件操作异常，响应信息：{res}')
            return None

    def all_module(self, course_id: str, class_id: str) -> list | None:
        """
        获取当前课程的大纲列表

        :param course_id: 课程ID
        :param class_id: 班级ID
        :return: list 大纲名称和ID列表
        """
        pay_load = self.the_pay_load.copy()
        pay_load.update({
            'courseOpenId': course_id,
            'openClassId': class_id
        })

        m_list = self.courseware(self.apis['all_module'], params=pay_load)
        if m_list:
            logger.info(f'成功获取课程{course_id}的大纲列表')
            return [{'name': m['moduleName'], 'id': m['moduleId']} for m in m_list]
        else:
            logger.warning(f'获取课程{course_id}大纲列表失败')
            return None

    def get_topic(self, module_id: str, course_id: str) -> list | None:
        """
        获取章节列表

        :param module_id: 大纲ID
        :param course_id: 课程ID
        :return: list 包含章节名称和ID的列表
        """
        pay_load = self.the_pay_load.copy()
        pay_load.update({
            'courseOpenId': course_id,
            # 'openClassId': class_id,
            'moduleId': module_id
        })
        '''
        res = self.get_req('all_topic',params=pay_load)

        res_json = res.json()
        '''
        t_list = self.courseware(self.apis['all_topic'], params=pay_load)
        if t_list:
            logger.info(f'成功获取课程{course_id}大纲{module_id}的的章节列表')
            return [{'name': t['topicName'], 'id': t['topicId']} for t in t_list]
        else:
            logger.warning(f'获取课程{course_id}大纲{module_id}的章节列表失败')
            return None

    def get_cell(self, course_id: str, topic_id: str, class_id: str = None) -> list | None:
        """
        获取指定章节下的课件列表

        不指定 class_id 可能会导致无法获取准确的学习进度

        :param course_id: 课程ID
        :param topic_id: 章节ID
        :param class_id: 开课班级ID
        :return: list 包含课件名称和ID的列表
        """
        pay_laod = self.the_pay_load.copy()
        pay_laod.update({
            'courseOpenId': course_id,
            'topicId': topic_id,
            'openClassId': class_id
        })
        cell_list = []
        c_list = self.courseware(self.apis['all_cell'], params=pay_laod)
        if c_list or isinstance(c_list, list):
            # 修复因为无课件导致错误判断为获取失败
            for c in c_list:
                if c['categoryName'] == '子节点':
                    # 将子节点下课件信息更新到课件列表
                    c_list.extend(c['cellChildNodeList'])
                    continue

                cell_list.append(
                    {'name': c['cellName'], 'id': c['cellId'], 'type': c['categoryName'],
                     'process': c['studyCellPercent']})

            logger.info(f'成功获取课程{course_id}章节{topic_id}的课件列表')
            return cell_list
        else:
            logger.warning(f'获取课程{course_id}章节{topic_id}的课件列表失败')
            return None

    def change_corseware(self, course_id: str, class_id: str, cell_id: str, cell_name: str) -> bool:
        # 此方法存在 用户信息异常 响应，为未携带COOKIES导致，待解决
        """
        用于重置当前学习课件，避免因为上次学习记录影响课件完成方法

        :param course_id:
        :param class_id:
        :param cell_id:
        :param cell_name:
        :return:
        """
        # 重置INFO_GET
        header = self.get_headers(update_item={
            'Host': 'zjy2.icve.com.cn',
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36 Edg/93.0.961.52",
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        })
        form_load = {
            'courseOpenId': course_id,
            'openClassId': class_id,
            'cellId': cell_id,
            'cellName': cell_name
        }

        res = self.request(url='https://zjy2.icve.com.cn/api/common/Directory/changeStuStudyProcessCellData',
                           data=form_load, header=header)

        # 由于错误待解决，代码暂维持原状

        res_json = res['data']
        if res_json['code'] == 1:
            return True
        else:
            return False

    def cell_info(self, course_id: str, class_id: str, cell_id: str) -> dict | None:
        """
        用户获取课件信息

        返回示例：
         {
            name: 课件名,

            id: 课件ID,

            course_name: 课程名,

            course_id: 课程ID,

            type: (str)课件类别,

            type_code: (int)课件列表代码,

            page: (int)文档型课件页数,

            now_page: (int)文档型课件当前学习进度（页数）,

            long: (float)音频型课件总时长（秒）,与实际视频长度有差异，但是只要学习时长大于等于此即算100%完成，

            now_long: (float)音频型当前学习视频时长（秒）,

            process: (float)当前学习进度 %,

            time: (float)学习时长
        }


        :param course_id: 课程ID
        :param class_id: 开课班级ID
        :param cell_id: 课件ID
        :return: 课件信息
        """

        '''
        def cookie_check():
            # cookie = self.__s.cookies
            cookie = utils.dict_from_cookiejar(self.__s.cookies)
            if not cookie.get('auth'):
                cookie.update(self.user.cookies)
                self.__s.cookies = utils.cookiejar_from_dict(cookie)
        '''

        # cookie_check()
        form_load = {
            'courseOpenId': course_id,
            'openClassId': class_id,
            'cellId': cell_id,
            'flag': 's'
        }

        res = self.request(self.apis['cell_info_new'], data=form_load)
        if res['code'] == 0:
            res_json = res['data']
            if res_json['code'] == 1:
                logger.info(f'成功获取到课程 {res_json["courseName"]}({course_id})下课件{cell_id}的信息')
                return {
                    'name': res_json['cellName'],
                    'id': res_json['cellId'],
                    'course_name': res_json['courseName'],
                    'course_id': res_json['courseOpenId'],
                    'type': res_json['categoryName'],
                    'type_code': str(res_json['cellType']),
                    'page': res_json['pageCount'],  # 文档类型总页数
                    'now_page': res_json['stuStudyNewlyPicCount'],  # 当前学习页数
                    'long': res_json['audioVideoLong'],  # 视频类型总时长（秒）,与实际视频长度有差异，但是只要学习时长大于等于此即算100%完成
                    'now_long': res_json['stuStudyNewlyTime'],  # 当前学习视频时长（秒）
                    'process': res_json['cellPercent'],  # 当前学习进度 %
                    'time': res_json['stuCellViewTime']
                }
            elif res_json['code'] == -1:
                logger.warning(f'获取课件{cell_id}的信息失败：{res_json["msg"]}')
                return None
            else:
                logger.warning(f'获取课件 {cell_id} 的信息失败，原始响应信息：{res}')
                return None
        else:
            logger.warning(f'获取课件 {cell_id} 的信息失败，响应结果：{res}')
            return None

    def finish_cell(self, course_id: str, class_id: str, cell_id: str):
        # 在课件信息中包含学习时长，下一次更新中应加入学习时长增加功能
        """
        完成课件

        :param course_id: 课程ID
        :param class_id: 开课班级ID
        :param cell_id: 课件ID
        :return:
        """
        time.sleep(1)
        # 获取课件信息
        cell_info = self.cell_info(course_id, class_id, cell_id)

        if cell_info:
            if int(cell_info['process']) == 100:
                # 同样加载至任务列表，但默认视为总进度100
                self.process_update(
                    target_name=cell_info['name'],
                    target_id=cell_info['id'],
                    now_process=100,
                    total_process=100
                )
                logger.info(f'课件 {cell_info["name"]}({cell_info["id"]}) 已达到100%完成度，将不会进行添加时长或页数操作')
            else:
                header = self.get_headers(update_item={
                    'Host': 'zjyapp.icve.com.cn',
                    'Accept': '*/*',
                    'Accept-Language': 'zh-Hans-CN;q=1.0',
                    'Accept-Encoding': 'gzip;q=1.0, compress;q=0.5',
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36 Edg/93.0.961.52',
                    'Cookie': 'auth=' + utils.dict_from_cookiejar(self.req_cookies)['auth']
                })

                form_load = {
                    'courseOpenId': course_id,
                    'openClassId': class_id,
                    'cellId': cell_id,  # 2
                    'cellLogId': '',
                    'picNum': '0',
                    'studyNewlyTime': '',
                    'studyNewlyPicNum': '0',
                    'token': self.user_info['newToken'],
                    'dtype': '1',
                }

                if '频' in cell_info['type']:
                    # 视频、音频类型
                    def get_next_long(num: float, long: float) -> float:
                        """
                        自动处理并返回下一提交的音频学习进度

                        :param num: 目标时长
                        :param long: 音频课件总时长
                        :return: 下一次提交的学习进度
                        """
                        if num == long:
                            # 防止卡循环
                            return long + 1
                        else:
                            new_num = num + uniform(18, 19.5)
                            if new_num < long:
                                if new_num - num > 20:
                                    return new_num - 1
                                else:
                                    return new_num
                            else:
                                return long

                    # 加载至任务列表
                    self.process_update(
                        target_name=cell_info['name'],
                        target_id=cell_info['id'],
                        now_process=cell_info['now_long'],
                        total_process=cell_info['long']
                    )

                    # 音频课件进度信息
                    num = cell_info['now_long']
                    long = cell_info['long']

                    num = get_next_long(num, long)
                    while num <= long:
                        # 暂时忘了这里清楚COOKIES原因...
                        self.req_clear_cookies()

                        form_load['studyNewlyTime'] = num
                        res = self.request(self.apis['finish_cell'], data=form_load, header=header)
                        if res['code'] == 0:
                            res_json = res['data']
                            if res_json['code'] == 1:
                                logger.info(
                                    f'成功为课件 {cell_info["name"]}({cell_id}) 添加时长至 {num} ，总时长 {long} (注意此时长非真正意义上视频时长)')
                                # 更新到进度
                                self.process_update(
                                    target_name=cell_info['name'],
                                    target_id=cell_info['id'],
                                    now_process=num,
                                )

                                # 随机等待时长
                                wait = randint(5, 10)
                                logger.info(f'课件{cell_info["name"]}({cell_id})随机等待{wait}秒')
                                time.sleep(wait)

                                num = get_next_long(num, long)
                                continue
                            elif res_json['code'] == -2:
                                num = num - 0.00123
                                long.info(f'课件{cell_info["name"]}({cell_id})添加时长失败，重新调整添加时长为{num}')
                                time.sleep(randint(2, 4))
                                continue
                            else:
                                logger.warning(f'为课件 {cell_info["name"]}({cell_id}) 添加时长失败，原始响应：{res}')
                                break
                        else:
                            logger.warning(f'在完成课件{cell_info["name"]}({cell_id})时发生异外响应，响应内容：{res}')

                    # logger.info(f'已为课件 {cell_info["name"]}({cell_id}) 添加时长至{num}秒，目标时长{long}秒')
                else:
                    # 文档类型
                    # task_cell = self.progress.add_task(f'[red]{cell_info["name"]}', total=int(cell_info['page']))

                    def get_next_page(now: int, page: int) -> int:
                        """
                        自动处理并返回下一提交的音频学习进度

                        :param now: 目标页数
                        :param page: 总页数
                        :return: 下一次提交页数
                        """
                        if now == page:
                            return page + 1
                        else:
                            if (now + 5) <= page:
                                return now + 5
                            else:
                                return page

                    # 加载至任务列表
                    self.process_update(
                        target_name=cell_info['name'],
                        target_id=cell_info['id'],
                        now_process=cell_info['now_page'],
                        total_process=cell_info['page']
                    )

                    # 文档型课件进度信息
                    now_page = cell_info['now_page']
                    page_long = cell_info['page']
                    if now_page == 0:
                        # 针对图片类型
                        now_page += 1

                    now_page = get_next_page(now_page, page_long)
                    while now_page <= page_long:

                        form_load.update({
                            'picNum': str(now_page),
                            'studyNewlyPicNum': str(now_page),
                        })

                        res = self.request(self.apis['finish_cell'], data=form_load, header=header)
                        # res = requests.post(url=apis['finish_cell'],headers=headers,data=form_load)
                        if res['code'] == 0:
                            res_json = res['data']
                            if res_json['code'] == 1:
                                logger.info(f'成功为课件 {cell_info["name"]}({cell_id}) 添加页数至 {now_page} ，总页数 {page_long}')
                                # 更新进度
                                self.process_update(
                                    target_name=cell_info['name'],
                                    target_id=cell_info['id'],
                                    now_process=now_page,
                                )

                                # 随机等待时长
                                wait = randint(5, 10)
                                logger.info(f'课件{cell_info["name"]}({cell_id})随机等待{wait}秒')
                                time.sleep(wait)

                                now_page = get_next_page(now_page, page_long)
                                continue
                            else:
                                logger.warning(f'为课件 {cell_info["name"]}({cell_id}) 原始响应：{res}')
                                break
                        else:
                            logger.warning(f'在完成课件{cell_info["name"]}({cell_id})时发生异外响应，响应内容：{res}')

                    # logger.info(f'已为课件 {cell_info["name"]}({cell_id}) 添加页数至 {now_page} ，目标页数 {page_long}')
        else:
            logger.warning(f'获取课程{course_id}下课件{cell_id}信息失败，无法继续完成课件')

    def all_cell(self, course_id: str = None, course_name: str = None, class_id: str = None) -> list | None:
        """
        自动获取某一课程下所有课件列表，course_id 和 course_name 两个参数至少要有一项填入

        返回示例：

        :param course_id: （可选）课程ID，当两参数都有时以此为准
        :param course_name: （可选）课程名，会自动根据此来匹配课程名，可能会导致误差
        :param class_id: (可选)开课班级ID，此项可能会影响课件完成度的正确返回
        :return: list 包含课件名称和ID的列表
        """
        if not course_id and course_name:
            # 仅当无ID且有Name时尝试定位，二者都有时以ID为准
            course_list = self.all_course
            if course_list:
                for course in course_list:
                    logger.info(f'正在对比输入项：{course_name}---{course["courseName"]}')
                    if course_name in course['courseName']:
                        logger.info(f'已选中：{course["courseName"]}')
                        course_id = course['courseOpenId']
                        class_id = course['openClassId']
                        # 修正课程名
                        course_name = course['courseName']
                        logger.info(f'当前获取所有课件目标课程为：{course_name}({course_id})')
                        break
            else:
                logger.warning('因为未输入指定的课程ID，尝试对比课程名时无法获取所有课程，对比失败，无法继续获取所有课件')
                return None

        logger.info(f'获取课程 {course_name}[{course_id}]课件大纲中...')
        m_list = self.all_module(course_id, class_id)
        if m_list:
            logger.info(f'成功获取课程 {course_name}[{course_id}]课件大纲')
            t_list = []
            c_list = []
            for m in m_list:
                logger.info(f'获取大纲 {m["name"]} 的章节中...')
                __topic_list = self.get_topic(m['id'], course_id)
                if __topic_list:
                    logger.info(f'成功获取大纲 {m["name"]} 的章节')
                    t_list += __topic_list
                else:
                    logger.warning(f'获取大纲 {m["name"]} 的章节失败，无法继续获取所有课件')
                    return None

            for t in t_list:
                logger.info(f'获取章节 {t["name"]} 对应的课件中...')
                __cell_list = self.get_cell(course_id, t['id'], class_id)
                if __cell_list:
                    logger.info(f'成功获取章节 {t["name"]} 对应的课件')
                    c_list += __cell_list
                elif isinstance(__cell_list, list):
                    logger.info(f'章节 {t["name"]} 下无课件，跳过')
                    continue
                else:
                    logger.warning(f'获取章节 {t["name"]} 对应的课件失败，无法继续获取所有课件')
                    return None
            '''  
            for c in c_list:
                logger.info(f'获取到课件：{c["name"]}({c["type"]})[{c["id"]}]--{c["process"]}')
            '''
            return c_list
        else:
            logger.warning(f'获取课程 {course_name}[{course_id}]课件大纲失败，无法继续获取所有课件')
            return None

    def all_comment(self, cell_id: str, course_id: str, class_id: str, limit: int = 1) -> list | None:
        """
        获取某一课件下的所有评论

        返回示例：[{
            'user_id': 用户ID,
            'user_name': 用户名,
            'content': 用户评论内容,
            'star': (int)用户评星
        }...]
        用户评星最大值为5，最小值为0（根据APP结合API响应推测）

        :param cell_id: 课件ID
        :param course_id: 课程ID
        :param class_id: 班级ID
        :param limit: (int)限制返回页数（获取前 limit 页的所有评论）一页包含20个评论，默认为1，即只获取前1一页评论
        :return: 包含评论者信息的评论列表
        """

        pay_load = self.the_pay_load.copy()
        del pay_load['stuId']
        pay_load.update({
            'activeType': '1',
            'cellId': cell_id,
            'courseOpenId': course_id,
            # 'equipmentApiVersion': '15.0',
            # 'equipmentAppVersion': '2.8.43',
            # 'equipmentModel': 'iPhone 11',
            'newToken': self.user_info['newToken'],
            'openClassId': class_id,
            'page': '1',
            'pageSize': '20',
            'sourceType': '3',
            'userId': self.user_info['userId'],
        })
        '''
        pay_load.update({
            'page':'1',
            'pageSize':'20',
            'cellId':cell_id,
            'courseOpenId':course_id,
            'activeType':'1',
            'openClassId':class_id,
            'equipmentApiVersion':self.user.login_info['equipmentApiVersion'],
            'equipmentAppVersion':self.user.login_info['equipmentAppVersion'],
            'equipmentModel':self.user.login_info['equipmentModel']
        })
        '''
        logger.info(f'正在获取课程{course_id}下课件{cell_id}评论列表...')
        comment_list = []
        while int(pay_load['page']) <= limit:
            logger.info(f'正在获取获取课程{course_id}下课件{cell_id}评论列表第 {pay_load["page"]} 页的评论')
            res = self.request(url=self.apis['all_comment'], params=pay_load)
            if res['code'] == 0:
                res_json = res['data']
                if res_json['code'] == 1:
                    c_list = res_json['list']
                    comment_list += [
                        {'user_id': c['userId'], 'user_name': c['displayName'], 'content': c['content'],
                         'star': c['star']}
                        for c in c_list]
                    if len(c_list) < 20 and c_list:
                        pay_load['page'] = str(int(pay_load['page']) + 1)
                        continue
                    else:
                        break
                else:
                    logger.warning(f'获取课程{course_id}下课件{cell_id}评论列表时发生意外返回，原始响应：{res}')
                    return None
            else:
                # logger.info(f'函数：{_getframe().f_code.co_name}\n异常的返回：CODE {res.status_code}  CONTENT ：\n{res.text}')
                logger.warning(f'获取课程{course_id}下课件{cell_id}评论列表时发生意外返回，原始响应：{res}')
                return None
        return comment_list

    def add_comment(self, cell_id: str, course_id: str, class_id: str, content: str, star: int) -> bool:
        """
        为某一课件添加评论

        :param cell_id: 课件ID
        :param course_id: 课程ID
        :param class_id: 班级ID
        :param content: 评论内容
        :param star: (int)评论打分星级，区间[0,5]
        :return: 如果成功返回True，否则返回False
        """

        data_load = '''{6}
            "CourseOpenId": "{0}",
            "OpenClassId": "{1}",
            "UserId": "{2}",
            "DocJson": "[\\n\\n]",
            "Content": "{3}",
            "CellId": "{4}",
            "SourceType": 3,
            "Star": {5}
        {7}
        '''.format(course_id, class_id, self.user_info['userId'], content, cell_id, star, "{", "}")

        # 解决token中@不被URL转码问题
        form_load = {
            'data': data_load,
            'newToken': self.user_info['newToken'],
            'sourceType': '3'
        }

        res = self.request(self.apis['add_comment'], data=form_load)
        if res['data'] == 0:
            res_json = res['data']
            if res_json['code'] == 0:
                logger.info(f'用户{self.user_info["userId"]}为课程{course_id}下课件{cell_id}添加评论：{content}[{star}星]成功')
                return True
            else:
                logger.warning(
                    f'用户{self.user_info["userId"]}为课程{course_id}下课件{cell_id}添加评论：{content}[{star}星] 失败！失败原因：{res_json["msg"]}')
                return False
        else:
            logger.warning(f'用户{self.user_info["userId"]}为课程{course_id}下课件{cell_id}添加评论失败。原始响应：{res}')
            return False
