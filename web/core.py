import requests
from requests import utils
import time
import hashlib
import logging
from configparser import ConfigParser
import os
from random import randint

requests.packages.urllib3.disable_warnings()
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
coon.read(WORK_PATH + '/setting.ini')


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

    logger.info(f'文件保存已启用，保存名为：{file_name}')
    return file_log


# 刷新和添加Handler
consloe_log.setFormatter(__format_switch(debug_status=coon.get('logging', 'debug')))
consloe_log.setLevel(log_status)

logger.addHandler(consloe_log)
if coon.get('logging', 'file_save') == 'true':
    logger.addHandler(__save_log())

# DEBUG 提醒
if log_status == logging.DEBUG:
    logger.info('注意：目前已启动DEBUG模式，如需关闭请在同目录下 setting.ini 文件中将 logging中debug选项更改为 false')


def get_logger():
    return logger


# 初始化requests
# s = requests.session()
# s.verify = False
the_headers = {
    'Host': 'zjyapp.icve.com.cn',
    'Accept': '*/*',
    'Accept-Language': 'zh-Hans-CN;q=1.0',
    'Accept-Encoding': 'gzip;q=1.0, compress;q=0.5',
}

# 职教云版本信息
icve_version = {
    'android': {
        'version': coon.get('icve', 'android_version'),
    },
    'ios': {
        'version': coon.get('icve', 'ios_version'),
        'build': coon.get('icve', 'ios_build'),
    }
}

# API Collection
apis = {
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
    'cell_info_new': 'https://zjy2.icve.com.cn/api/common/Directory/viewDirectory'
}


def login_check(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return {'code': '0', 'msg': '未登陆！'}

    return wrapper


class User:
    def __init__(self, login_info: dict):
        """

        :param login_info: {
            appVersion:职教云版本    //暂时无用
            clientId:clientId
            equipmentApiVersion:设备系统版本号
            equipmentAppVersion:职教云版本      //暂时无用
            equipmentModel:设备名称
            userName:职教云账号
            userPwd:职教云密码
            }
        """
        # REQ
        self.__s = requests.session()
        self.__s.verify = False

        self.device_type = ''
        self.login_info = login_info
        # user_info
        self.user_info = {}
        self.user_info.update(login_info)
        # 自动登陆
        self.__ua_switch()
        self.login()

    def __ua_switch(self):
        if 'iPhone' or 'iphone' in self.login_info['equipmentModel']:
            # iOS
            self.device_type = 'ios'

            if len(self.login_info['equipmentApiVersion']) < 6:
                # 短版本号补0
                self.login_info['equipmentApiVersion'] += '.0'
            the_headers.update({
                'User-Agent': 'yktIcve/{0} (com.66ykt.66yktteacherzhihui; build:{1}; iOS {2})'.format(
                    icve_version['ios']['version'], icve_version['ios']['build'],
                    self.login_info['equipmentApiVersion'])
            })
        else:
            # Android
            self.device_type = 'android'
            the_headers.update({
                'User-Agent': 'okhttp/{0}'.format(icve_version['android']['version'])
            })

    def login(self):
        """
        登陆（APP），登陆后让session获取到相关信息并返回用户的相关信息
        :return: 登陆信息
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
            need_info = [self.login_info['equipmentModel'], self.login_info['equipmentApiVersion'],
                         icve_version[self.device_type]['version'], emit]
            device_id = ''
            for i in range(0, len(need_info)):
                device_id = md5it(device_id) + need_info[i]
            device_id = md5it(device_id)  # 最终加密结果

            return device_id

        new_headers = the_headers.copy()

        # EMIT
        emit = str(int(time.time())) + '000'
        new_headers.update({
            'emit': emit,
            'device': get_device(emit),
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'
        })

        # 装载headers
        self.__s.headers.update(new_headers)

        # FORM LOAD
        login_form = self.login_info
        login_form.update({
            'sourceType': '3'
        })

        res = self.__s.post(apis['login'], data=login_form)
        res_json = res.json()
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
                'cookies': utils.dict_from_cookiejar(res.cookies)  # dict Cookies
            })
            return {'code': '1', 'msg': '登陆成功！'}
        else:
            # 失败
            return {'code': '0', 'msg': res_json['msg']}

    def login_from_session(self,info:dict=None):
        if not info:
            info = self.login_info

        # 用于将User更新为已经登陆
        self.user_info.update(info)
        # 装载Cookie
        self.__s.cookies = utils.cookiejar_from_dict(info,cookiejar=None,overwrite=True)
        # TOKEN保质期测试
        course = Course(self)
        course_info = course.all_course
        if not isinstance(course_info,list):
            # 重新登陆
            self.login_info = self.user_info.copy()
            login_status = self.login()
            if login_status['code'] == '0':
                return {'code':'0','mdg':'重新登陆失败：'+login_status['msg']}
        else:
            # 成功登陆
            return {'code':'1','msg':'登陆成功'}



    @login_check
    def save_login(self):
        try:
            coon.set('user', 'cookies', str(self.cookies))
            coon.set('user', 'token', self.token)
            coon.write(open(WORK_PATH + '/setting.ini', 'w', encoding='utf-8'))
        except BaseException:
            return False
        else:
            return True

    @property
    def account(self):
        """
        返回职教云账号
        :return: 返回职教云账号
        """
        return self.login_info['userName']

    @property
    @login_check
    def name(self):
        """
        用户姓名
        :return: 用户姓名
        """
        return self.user_info['displayName']

    @property
    @login_check
    def id(self):
        """
        用户ID
        :return: 用户ID
        """
        return self.user_info['userId']

    @property
    @login_check
    def token(self):
        """
        用户TOKEN
        :return: 用户TOKEN
        """
        return self.user_info['newToken']

    @property
    @login_check
    def header_url(self):
        """
        用户头像
        :return: 用户头像URL
        """
        return self.user_info['url']

    @property
    @login_check
    def type(self):
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
    def number(self):
        """
        用户的工号
        :return: 学工号
        """
        return self.user_info['employeeNumber']

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
        # 触发login_check
        self.user_info['cookies']

        return self.__s


class Course:
    def __init__(self, user):
        self.user = user
        self.__s = user.req
        # 更新Headers
        self.new_headers = the_headers.copy()
        self.__s.headers.clear()
        self.__s.headers.update(self.new_headers)
        # 公用PAYLOAD
        self.the_pay_load = {
            'sourceType': '3',
            'stuId': self.user.id,
            'newToken': self.user.token
        }

    def get_req(self, api, params):
        res = self.__s.get(url=apis[api], params=params)
        return res

    def post_req(self, api, form):
        pass

    @property
    def all_course(self):
        """
        所有在修课程
        :return: 在修课程列表，列表中包含了课程及对应的信息
        """
        pay_laod = self.the_pay_load.copy()
        pay_laod.update({
            'isPass': '0',
            'page': '1',
        })
        course_list = []

        while True:
            res = self.__s.get(url=apis['all_course'], params=pay_laod)

            res_json = res.json()
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
                logger.warning('未能尝试获取课程列表')
                return {'code': '0', 'msg': res_json['msg']}
        return course_list

    def courseware(self, api, params) -> dict:
        """
        [TOOL]用于课件相关的操作
        :param api: 指定的API URL
        :param params: 指定附带的URL参数
        :return: 返回除 code 和 msg 外的回调信息
        """
        res = self.__s.get(url=api, params=params)

        res_json = res.json()
        if res_json['code'] == 1:
            # return res_json[res_json.keys()[1]]

            del res_json['code']
            del res_json['msg']
            for d in res_json.values():
                return d
        else:
            logger.warning('未能成功获取：{}'.format(res_json['msg']))
            return {}

    def all_module(self, course_id, class_id) -> list:
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

        m_list = self.courseware(api=apis['all_module'], params=pay_load)

        return [{'name': m['moduleName'], 'id': m['moduleId']} for m in m_list]

    def get_topic(self, module_id, course_id) -> list:
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
        t_list = self.courseware(api=apis['all_topic'], params=pay_load)
        return [{'name': t['topicName'], 'id': t['topicId']} for t in t_list]

    def get_cell(self, course_id, topic_id, class_id=None) -> list:
        """
        获取指定章节下的课件列表
        :param course_id: 课程ID
        :param topic_id: 章节ID
        :return: list 包含课件名称和ID的列表
        """
        pay_laod = self.the_pay_load.copy()
        pay_laod.update({
            'courseOpenId': course_id,
            'topicId': topic_id,
            'openClassId': class_id
        })

        c_list = self.courseware(api=apis['all_cell'], params=pay_laod)
        return [{'name': c['cellName'], 'id': c['cellId'], 'type': c['categoryName'], 'process': c['studyCellPercent']}
                for c in c_list]

    def get_cell_info(self, class_id, cell_id):
        pay_load = self.the_pay_load.copy()
        pay_load.update({
            'cellId': cell_id,
            'openClassId': class_id,
        })

        res = self.__s.get(apis['cell_info'], params=pay_load)
        res_json = res.json()
        if res_json['code'] == 1:
            logger.info(f'成功获取到课件{cell_id}的信息')
            cell = res_json['cellInfo']
            return {
                'name': cell['cellName'],
                'type': cell['categoryName'],
                'type_code': cell['cellType'],
                'long': cell['audioVideoLong'],
                'process': cell['studyCellPercent']
            }
        else:
            logger.warning(f'无法获取到课件{cell_id}的信息')

    def cell_info(self, course_id, class_id, cell_id):
        form_load = {
            'courseOpenId': course_id,
            'openClassId': class_id,
            'cellId': cell_id
        }

        res = self.__s.post(apis['cell_info_new'], data=form_load)
        res_json = res.json()

        if res_json['code'] == 1:
            logger.info(f'成功获取到课件 {cell_id} 的信息')

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
                'process': res_json['cellPercent']  # 当前学习进度 %
            }
        else:
            logger.warning(f'获取课件 {cell_id} 的信息失败')

    def finish_cell(self, course_id, class_id, cell_id):
        cell_info = self.cell_info(course_id, class_id, cell_id)

        if int(cell_info['process']) == 100:
            logger.info(f'课件 {cell_id} 已达到100%完成度，将不会进行添加时长或页数操作')
        else:
            headers = {
                'Host': 'zjyapp.icve.com.cn',
                'Accept': '*/*',
                'Accept-Language': 'zh-Hans-CN;q=1.0',
                'Accept-Encoding': 'gzip;q=1.0, compress;q=0.5',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36 Edg/93.0.961.52',
                'Cookie': 'auth=' + self.user.cookies['auth']
            }

            form_load = {
                'courseOpenId': course_id,
                'openClassId': class_id,
                'cellId': cell_id,  # 2
                'cellLogId': '',
                'picNum': '0',
                'studyNewlyTime': '',
                'studyNewlyPicNum': '0',
                # 'token':'sbjmapgth4topzqft1tikq',
                'token': self.user.token,
                'dtype': '1',
            }
            if '视' in cell_info['type']:
                def get_next_long(num, long):
                    if (num + 20) < long:
                        return num + 20
                    else:
                        return long

                # 视频课件
                num = cell_info['now_long']
                long = cell_info['long']

                num = get_next_long(num, long)
                while num <= long:
                    self.__s.cookies.clear()


                    form_load['studyNewlyTime'] = num
                    # res = requests.post(url='https://zjy2.icve.com.cn/api/common/Directory/stuProcessCellLog', data=form_load,headers=headers)

                    res = self.__s.post(url='https://zjy2.icve.com.cn/api/common/Directory/stuProcessCellLog',
                                        data=form_load,
                                        headers=headers)
                    res_json = res.json()
                    if res_json['code'] == 1:
                        logger.info(f'成功为课件{cell_id}添加时长至 {num} ，总时长 {long} (注意此时长非真正意义上视频时长)')

                        '''
                        # 防止增长区间大于20秒
                        the_new_num = num + 20
                        if (the_new_num - num) > 20:
                            num = the_new_num - 1
                        else:
                            num = the_new_num
                        '''
                        # 随机等待时长
                        wait = randint(5, 10)
                        logger.info(f'随机等待{wait}秒')
                        time.sleep(wait)

                        num = get_next_long(num,long)
                        continue
                    else:
                        logger.warning(f'为课件{cell_id}添加时长失败：{res_json["msg"]}')
                        break
                logger.info(f'已为课件{cell_id}添加时长至{num}秒，目标时长{long}秒')
            else:
                # 文档类型
                def get_next_page(now, page):
                    if (now + 5) <= page:
                        return now + 5
                    else:
                        return page

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

                    res = self.__s.post(url='https://zjy2.icve.com.cn/api/common/Directory/stuProcessCellLog',
                                        data=form_load,
                                        headers=headers)
                    res_json = res.json()
                    if res_json['code'] == 1:
                        logger.info(f'成功为课件 {cell_id} 添加页数至 {now_page} ，总页数 {page_long}')

                        # 随机等待时长
                        wait = randint(5, 10)
                        logger.info(f'随机等待{wait}秒')
                        time.sleep(wait)

                        now_page = get_next_page(now_page,page_long)
                        continue
                    else:
                        logger.warning(f'为课件 {cell_id} 添加页数失败：{res_json["msg"]}')
                        break
                logger.info(f'已为课件 {cell_id} 添加页数至 {now_page} ，目标页数 {page_long}')

    def all_cell(self, course_id=None, course_name=None) -> list:
        """
        自动获取某一课程下所有课件列表，两个参数至少要有一项
        :param course_id: （可选）课程ID，当两参数都有时以此为准
        :param course_name: （可选）课程名，会自动根据此来匹配课程名，可能会导致误差
        :return: list 包含课件名称和ID的列表
        """
        class_id = ''
        if not course_id and course_name:
            # 仅当无ID且有Name时尝试定位，二者都有时以ID为准
            course_list = self.all_course

            for course in course_list:
                logger.info('正在对比输入项：{0}---{1}'.format(course_name, course['courseName']))
                if course_name in course['courseName']:
                    logger.info('已选中：{}'.format(course['courseName']))
                    course_id = course['courseOpenId']
                    class_id = course['openClassId']
                    # 修正课程名
                    course_name = course['courseName']
                    break

        logger.info('获取课程 {0} [{1}] 课件大纲中...'.format(course_name, course_id))
        m_list = self.all_module(course_id, class_id)
        t_list = []
        c_list = []
        for m in m_list:
            logger.info('获取大纲 {} 的目录中...'.format(m['name']))
            t_list += self.get_topic(m['id'], course_id)
        for t in t_list:
            logger.info('获取目录 {} 对应的课件中...'.format(t['name']))
            c_list += self.get_cell(course_id, t['id'])

        for c in c_list:
            logger.info('获取到课件：{0}({1})[{2}]--{3}'.format(c['name'], c['type'], c['id'], c['process']))

        return c_list

    def all_comment(self, cell_id, course_id, class_id, limit=int(coon.get('courseware', 'comments_limit'))) -> list:
        """
        获取某一课件下的所有评论
        :param cell_id: 课件ID
        :param course_id: 课程ID
        :param class_id: 班级ID
        :param limit: int 限制，用于获取前 limit 页的所有评论，一页包含20个评论
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
            'newToken': self.user.token,
            'openClassId': class_id,
            'page': '1',
            'pageSize': '20',
            'sourceType': '3',
            'userId': self.user.id,
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
        logger.info('正在获取 {} 的评论'.format(cell_id))
        comment_list = []
        while int(pay_load['page']) <= limit:
            logger.info('正在获取第 {} 页的评论'.format(pay_load['page']))
            res = self.__s.get(url=apis['all_comment'], params=pay_load)
            res_json = res.json()

            if res_json['code'] == 1:
                c_list = res_json['list']
                comment_list += [
                    {'user_id': c['userId'], 'user_name': c['displayName'], 'content': c['content'], 'star': c['star']}
                    for c in c_list]
                if len(c_list) < 20:
                    pay_load['page'] = str(int(pay_load['page']) + 1)
                    continue
                else:
                    break
            else:
                logger.warning('获取 {} 的评论失败'.format(cell_id))
                break
        return comment_list

    def add_comment(self, cell_id, course_id, class_id, content, star):
        """
        为某一课件添加评论
        :param cell_id: 课件ID
        :param course_id: 课程ID
        :param class_id: 班级ID
        :param content: 评论内容
        :param star: 评论打分星级，区间[0,5]
        :return:
        """
        data_load = {
            "CellId": "{}".format(cell_id),
            "Star": "{}".format(star),
            "CourseOpenId": "{}".format(course_id),
            "OpenClassId": "{}".format(class_id),
            "SourceType": 3,
            "UserId": "{}".format(self.user.id),
            "Content": "{}".format(content),
            "DocJson": "[\n\n]"
        }
        form_load = {
            'data': str(data_load),
            # 'data': '{ "CellId" : "{0}","Star" : {1},"CourseOpenId" : "{2}","OpenClassId" : "{3}","SourceType" : 3,"UserId" : "{4}","Content" : "{5}","DocJson" : "[\n\n]" }'.format(cell_id, star, course_id, class_id, self.user.id, content),
            'newToken': self.user.token,
            'sourceType': '3'
        }
        res = self.__s.post(apis['add_comment'], data=form_load)
        res_json = res.json()
        if res_json['code'] == 1:
            logger.info('用户{0} 为 {1} 添加评论：{2}[{3}星] 成功！'.format(self.user.id, cell_id, content, star))
            return True
        else:
            logger.warning(
                '用户{0} 为 {1} 添加评论：{2}[{3}星] 失败！失败原因：{4}'.format(self.user.id, cell_id, content, star, res_json['msg']))
            return False

    # FROM LITE-CORE
    def change_corseware(self, course_id, class_id, cell_id, cell_name):
        # 重置INFO_GET
        headers = the_headers.copy()
        headers.update({
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

        res = self.__s.post(url='https://zjy2.icve.com.cn/api/common/Directory/changeStuStudyProcessCellData',
                            data=form_load, headers=headers)
        res_json = res.json()
        if res_json['code'] == 1:
            return True
        else:
            return False

class Classes:
    def __init__(self, user: User):
        self.user = user
        self.the_pay_load = {
            'sourceType': '3',
            'stuId': self.user.id,
            'newToken': self.user.token,
        }
        self.__s = self.user.req

    def all_class(self, course_list=None):
        def get_class():
            class_list = []
            while True:
                res = self.__s.get(apis['all_class'], params=pay_load)
                res_json = res.json()
                if res_json['code'] == 1:
                    if pay_load.get('courseOpenId'):
                        logger.info('正在获取课程 {0} 的所有开课中，共 {1} 次开课，当前页数为 {2}'.format(pay_load.get('courseOpenId'),
                                                                                   res_json['pagination'][
                                                                                       'totalCount'],
                                                                                   res_json['pagination'][
                                                                                       'pageIndex']))
                    else:
                        logger.info('正在获取所有开课，共 {0} 次开课，当前页数 {1}'.format(res_json['pagination']['totalCount'],
                                                                         res_json['pagination']['pageIndex']))
                    c_list = res_json['dataList']
                    for c in c_list:
                        class_list.append({
                            'title': '{0}-{1}'.format(c['courseName'], c['Title']),
                            'id': c['Id'],
                            'address': c['Address']
                        })
                    if len(c_list) < 10:
                        logger.info('当前课程或所有开课全部获取完毕')
                        break
                    else:
                        logger.info('获取完毕，准备进行下一页...')
                        pay_load['page'] = str(int(pay_load['page']) + 1)
                        continue
                else:
                    logger.warning('获取开课失败！错误信息：{}'.format(res_json['msg']))
                    break
            return class_list

        pay_load = self.the_pay_load.copy()
        pay_load.update({'page': '1'})
        class_list = []
        if course_list:
            for c in course_list:
                pay_load.update({
                    'courseOpenId': c['courseOpenId'],
                    'openClassId': c['openClassId']
                })
                class_list += get_class()
        else:
            class_list += get_class()
        return class_list

    def get_active(self, active_id):
        # 签到状态
        def sign_status():
            __pay_load = pay_load.copy()

            res = self.__s.get(apis[''])

        # 课堂评论
        def class_comment():
            __pay_load = pay_load.copy()

            res = self.__s.get(apis['class_comment'], params=__pay_load)
            res_json = res.json()

            if res_json['code'] == 1:
                return {'star': res_json['stuEvaluationInfo']['Star'],
                        'content': res_json['stuEvaluationInfo']['StuContent']}
            else:
                logger.warning('获取课堂评论状态失败')
                return {}

        # 自我评论
        def self_comment():
            __pay_load = pay_load.copy()

            res = self.__s.get(apis['self_comment'], params=__pay_load)
            res_json = res.json()

            if res_json['code'] == 1:
                return {'star': res_json['selfEvaluationInfo']['Star'],
                        'content': res_json['selfEvaluationInfo']['Content']}
            else:
                logger.warning('获取自评论状态失败')
                return {}

        pay_load = self.the_pay_load.copy()
        pay_load.update({
            'activityId': active_id,
            # 'classState':'1',   # 1课前 2课中 3课后
        })
        '''
        while int(pay_load['classState']) <=3:
            res = self.__s.get(apis['get_active'],params=pay_load)
            res_json = res.json()
            if res_json['code'] == 1:
                pass
        '''

        return {
            'sign': {},
            'class_comment': class_comment(),
            'self_comment': self_comment()
        }

    def class_comment(self):
        pass


class Sign:
    def __init__(self, user: User):
        self.user = user
        self.__s = user.req
        self.the_pay_load = {
            'sourceType': '3',
        }

    def sign_up(self, class_id, sign_id, lesson_id):
        form_load = self.the_pay_load.copy()
        form_load.update({
            'SignResultType': '3',
            'StuId': self.user.id,
            'OpenClassId': class_id,
            'SignId': sign_id,
            'Id': lesson_id
        })
        # del self.__s.cookies

        res = self.__s.post(apis['change_sign'], data=form_load)
        res_json = res.json()
        if res_json['code'] == 1:
            logger.info('已将 {} 的签到状态改为[已签到]'.format(lesson_id))
        else:
            logger.warning('更改 {0} 的签到状态失败:{1}'.format(lesson_id, res_json['msg']))


if __name__ == '__main__':
    login_info = {
        'appVersion': '2.8.43',
        'clientId': '62f3227a55d811eca5a80a80ff2603de',
        'equipmentApiVersion': '14.8',
        'equipmentAppVersion': '2.8.43',
        'equipmentModel': 'iPhone 11',
        'userName': '2020111136',
        'userPwd': 'SunnyO010216',
    }
    me = User(login_info)
    print(me.login_info)
    print('')
