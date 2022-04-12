import uuid
from functools import wraps
import requests
from requests import utils
import os.path
import time
import hashlib
import logging
from configparser import ConfigParser
from random import randint, sample

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


class LoginFail(Exception):
    pass


class CourseError(Exception):
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
        self.apis = {
            'login': 'https://zjyapp.icve.com.cn/newMobileAPI/MobileLogin/newSignIn',
        }

        # Cookies池
        self.cookies = {}

    def update_header(self, info: dict):
        try:
            self.__headers.update(info)
        except Exception as e:
            log.error('在尝试更新请求头时发生错误：' + e)

    def set_agent(self, agent):
        self.update_header({
            'User-Agent': agent
        })

    def new_info(self, code, msg):
        self.info.update({
            'code': code,
            'msg': msg
        })
        if code == '1':
            log.info(msg)
        elif code == '0':
            log.warning(msg)

    def req(self, method: str, api=None, data={}, params={}, url=None):
        REQ_METHOD = None
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

            if method.upper() == 'GET' or method.upper() == 'G':
                REQ_METHOD = 'GET'
            elif method.upper() == 'POST' or method.upper() == 'P':
                REQ_METHOD = 'POST'
            else:
                self.new_info('0', '意外的请求方式')
                raise ReqError('意外的请求方式')

        # 处理data和params
        the_data = self.__data.copy()
        the_params = self.__params.copy()
        if data or params:
            try:
                the_data.update(data)
                the_params.update(params)
            except TypeError:
                self.new_info('0', '在处理表单和参数时发生错误')
                raise ReqError('在处理表单和参数时发生错误')

        if REQ_METHOD:
            # 这里待加入针对登陆过期判断，特征-> [200] : {"code":-1000,...}

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
    # 默认为未登陆状态
    isLogin = False
    # 上次登陆时间
    last_login = 0

    def __init__(self):
        super().__init__()

        # 登陆表单
        self.__login_info = {
            'appVersion': '2.8.43',
            'clientId': '',
            'equipmentApiVersion': '',
            'equipmentAppVersion': '2.8.43',
            'equipmentModel': '',
            'userName': '',
            'userPwd': ''
        }

        # 用户信息
        self.my_info = {
            'account': self.__login_info['userName'],
            'device': {
                'name': self.__login_info['equipmentModel'],
                'id': self.__login_info['clientId']
            }
        }

        # 登陆状态
        # self.isLogin = False

        self.apis.update({
            'login':'https://zjyapp.icve.com.cn/newMobileAPI/MobileLogin/newSignIn',
            'newTokne':'https://zjyapp.icve.com.cn/newMobileAPI/MobileLogin/getNewSignInToke',
            'msg':'https://zjyapp.icve.com.cn/newMobileAPI/News/getUserNewsList',
            'msgRead':'https://zjyapp.icve.com.cn/newMobileAPI/News/setNewsIsReadById',
            'msgAllRead':'https://zjyapp.icve.com.cn/newMobileAPI/News/setAllNewsIsRead',
            'msgDelete':'https://zjyapp.icve.com.cn/newMobileAPI/News/deletedNewsByIds',
            'pswdEidt':'',
            'Logout':'',
            'saveLogin':''
        })

    def set_account(self, account: str, pswd: str):
        """
        设置登陆的账号密码
        :param account: 账号
        :param pswd: 密码
        :return: None
        """
        self.__login_info.update({
            'userName': account,
            'userPwd': pswd
        })

    def set_device(self, name: str, version: str, clientID: str):
        """
        设置设备名和系统版本号
        :param name: 设备名
        :param version: 系统版本号
        :param clientID: clientId
        :return: None
        """
        self.__login_info.update({
            'equipmentModel': name,
            'equipmentApiVersion': version
        })
        if not clientID:
            self.__login_info.update({
                'clientId': str(uuid.uuid4()).replace('-', '')
            })
        else:
            self.__login_info.update({
                'clientId':clientID
            })

    def set_app(self, version: str, os_type: str):
        """
        设置APP的版本号和系统类别（iOS或安卓），会自动根据系统类别增加User-Agent头
        :param version: APP版本号
        :param os_type: 系统类别
        :return: None
        """
        self.__login_info.update({
            'equipmentAppVersion': version,
            'appVersion': version
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
                'User-Agent': 'okhttp/4.5.0'
            })

    def login(self):
        """
        登陆
        :return: 返回登陆状态
        """

        def get_device(emit):
            def md5it(content=None):
                if content:
                    md5 = hashlib.md5()
                    md5.update(content.encode("utf-8"))
                    return md5.hexdigest()
                else:
                    return ''

            # need_info = [设备名，设备系统版本号，职教云版本号，时间戳]
            need_info = [
                self.__login_info['equipmentModel'],
                self.__login_info['equipmentApiVersion'],
                self.__login_info['appVersion'],
                emit
            ]

            device_id = ''
            for i in range(0, len(need_info)):
                device_id = md5it(device_id) + need_info[i]
            device_id = md5it(device_id)  # 最终加密结果

            return device_id

        # EMIT & Headers
        emit = str(int(time.time())) + '000'
        # new_headers = self.__headers.copy()
        new_headers = {
            'emit': emit,
            'device': get_device(emit),
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'
        }
        self.update_header(new_headers)

        login_info = self.__login_info.copy()
        self.__login_info.update({'sourceType': '3'})

        try:
            res = self.get('login', login_info)
            res_json = res.json()
            if res_json['code'] == 1:
                # 登陆成功并刷新user_info
                self.my_info.update({
                    'type': res_json['userType'],  # 用户类别，已知1为学生
                    'id': res_json['userId'],  # 用户ID
                    'token': res_json['newToken'],  # Token
                    'name': res_json['displayName'],  # 用户姓名
                    'num': res_json['employeeNumber'],  # 用户学号（或其他工号）
                    'url': res_json['url'],  # 用户头像URL
                    'schoolName': res_json['schoolName'],  # 用户所在学校名
                    'schoolId': res_json['schoolId'],  # 用户所在学校ID
                    'cookies': utils.dict_from_cookiejar(res.cookies)  # dict Cookies
                })
                # 更新登陆状态
                self.isLogin = True
                # 更新登陆时间
                self.last_login = time.time()

                # 更新默认表单
                self.__params.update({
                    'sourceType': '3',
                    'userId': self.my_info['id'],
                    #'userName': self.__login_info['userName'],
                    #'userPwd': self.__login_info['userPwd'],
                    #'clientId': self.__login_info['clientId']
                })

                self.new_info('1', f'用户{self.my_info["name"]}({self.my_info["id"]})已登陆')
            else:
                # 登陆失败
                self.new_info('0', f'账号{self.my_info["account"]}尝试登陆失败，错误返回：{res_json["code"]}---{res_json["msg"]}')
                raise LoginFail(f'{res_json["code"]}---{res_json["msg"]}')

        except ReqError as e:
            self.new_info('0', e)
            # 这里应该需要再来一个异常去截断
        finally:
            return self.isLogin

    @classmethod
    def login_check(cls, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if cls.isLogin:
                if time.time() - cls.last_login < 10800:
                    return func(*args, **kwargs)
                else:
                    # 更换TOKEN
                    cls.token_update()
                    return func(*args, **kwargs)
            else:
                raise LoginFail('请先登陆！')

        return wrapper

    @login_check
    def token_update(self):
        try:
            res = self.get(api='newToken', params={
                'userName': self.__login_info['userName'],
                'userPwd': self.__login_info['userPwd'],
                'clientId': self.__login_info['clientId']
            })
            res_json = res.json()
            if res_json['code'] == 1:
                # 刷新TOKEN
                self.my_info.update({
                    'token':res_json['newToken']
                })
            else:
                raise LoginFail(f'更换TOKEN失败：{res_json["msg"]}')
        except ReqError as e:
            raise LoginFail(f'更换TOKEN失败：{e}')


    @property
    @login_check
    def name(self):
        """
        用户名
        :return: 用户名
        """
        return self.my_info['name']

    @property
    @login_check
    def id(self):
        """
        用户ID
        :return: 用户ID
        """
        return self.my_info['id']

    @property
    @login_check
    def header_url(self):
        """
        用户头像地址
        :return: 用户头像地址
        """
        return self.my_info['url']

    @property
    @login_check
    def type(self):
        """
        用户类型
        :return: 用户类型：学生或老师
        """
        if self.user_info['type'] == '1':
            return '学生'
        else:
            return '教职工'

    @property
    @login_check
    def token(self):
        """
        用户的token
        :return: token
        """
        return self.user_info['token']

    @property
    @login_check
    def number(self):
        """
        用户的工号
        :return: 学工号
        """
        return self.user_info['num']

    @property
    @login_check
    def school_info(self):
        """
        用户所在学校信息
        :return: dict 包含学校名和ID
        """
        return {
            'name': self.user_info['schoolName'],
            'id': self.user_info['schoolId']
        }

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
        return self.__s


class Course(BaseReq):
    def __init__(self, user: User):
        super().__init__()
        self.__s = user.req
        self.user = user

        # 公用PAYLOAD
        self.__params.update({
            'sourceType': '3',
            'stuId': self.user.id,
            'newToken': self.user.token
        })

        # 课程列表
        self.courses = self.__courses()

        # 用于指定当前课程，省去重复指定导致搜索的搜索时间
        self.now_course = {}

    def __courses(self):
        course_list = []
        pay_load = {
            'isPass': '0',
            'page': '1',
        }
        while True:
            try:
                res = self.get(api='allCourses', params=pay_load)
                res_json = res.json()

                if res_json['code'] == 1:
                    c_list = res_json['dataList']
                    if len(c_list) < 1:
                        if len(course_list) < 1:
                            self.new_info('0', '你还没有参加任何课程')
                        break
                    else:
                        self.new_info('1', f'正在尝试获取第{pay_load["page"]}页可能存在的课程')
                        for c in c_list:
                            course_list.append({
                                'courseOpenId': c['courseOpenId'],  # 课程开课ID
                                'courseName': c['courseName'],  # 课程名称
                                'url': c['thumbnail'],  # 课程封面URL
                                'openClassName': c['openClassName'],  # 开课班级名称
                                'openClassId': c['openClassId'],  # 开课班级ID
                                'mainTeacherName': c['mainTeacherName'],  # 主教师名
                                'mainTeacherNum': c['mainTeacherNum'],  # 主教师编号
                                'process': c['process'],  # 课程学习进度
                                'totalScore': c['totalScore'],  # 课程学习总得分
                                'InviteCode': c['InviteCode']  # 课程开课班级邀请码
                            })

                            # 更新page
                            pay_load['page'] = str(int(pay_load['page']) + 1)
                            continue
            except ReqError as e:
                self.new_info('0', f'获取所有课程失败，错误信息：{e}')
            finally:
                return course_list

    def search(self, wd, key=None):
        """
        用于实现关键字搜索指定课程信息并返回课程信息的方法
        :param wd: 关键字，如ID，名称，教师名等
        :param key: 指定关键字对应类别，加速搜索
        :return: 课程信息
        """
        if key:
            try:
                for l in self.courses:
                    if wd in l[key]:
                        return l
            except KeyError:
                raise CourseError(f'未查找到包含关键字 {wd} 的课程')
        else:
            # 随机抽取
            courses = self.courses.copy()
            while courses:
                sample_c = sample(courses, 1)[0]
                for info in sample_c.values():
                    if wd in info:
                        return sample_c
                courses.remove(sample_c)
            raise CourseError(f'未查找到包含关键字 {wd} 的课程')

    def __search_now(self, wd, key=None):
        """
        内部用于对比当前课程是否与预查询课程相同
        :param wd: 关键字
        :param key: 关键字对应的类别
        :return: 查询的课程是否为当前课程的结果（True OR False）
        """
        if self.now_course:
            if key:
                try:
                    if wd in self.now_course[key]:
                        return True
                except KeyError:
                    return False
            else:
                if wd in self.now_course.values():
                    return True
                else:
                    return False
        else:
            return False

    def now_course_id(self):
        pass

    def get_courses(self):
        self.courses = self.__courses()

    def __courseware_get(self, api, params):
        res = self.get(api=api, params=params)
        res_json = res.json()
        if res_json['code'] == 1:
            # 预处理
            del res_json['code']
            del res_json['msg']
            return list(res_json.values())[0]
        else:
            raise ReqError(f'获取失败：{res_json["code"]}---{res_json["msg"]}')

    def modules(self, course_id=None, wd=None):
        course_info = {}
        if not course_id and not wd:
            raise CourseError('未指定课程')
        elif course_id:
            if self.__search_now(wd=course_id, key='courseOpenId'):
                course_info = self.now_course
            else:
                try:
                    course_info = self.search(course_id, key='courseOpenId')
                except CourseError as e:
                    self.new_info('0', f'查找课程所有章节时失败：{e}')
                    return []
        else:
            if self.__search_now(wd=wd):
                course_info = self.now_course
            else:
                try:
                    course_info = self.search(wd)
                except CourseError as e:
                    self.new_info('0', f'查找课程所有章节时失败：{e}')
                    return []
        try:
            m_list = self.__courseware_get(api='modules', params={
                'courseOpenId': course_info['courseOpenId'],
                'openClassId': course_info['openClassId']
            })
            # 预处理
            return [{'name': m['moduleName'], 'id': m['moduleId']} for m in m_list]
        except ReqError as e:
            self.new_info('0', f'获取课程章节失败：{e}')
        finally:
            return []

    def courseware(self):
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
