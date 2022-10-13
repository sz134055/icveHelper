# _*_coding:utf-8_*_
from random import randint, uniform
import wx
from layout import main as Layout
from webbrowser import open_new_tab as browser_open_new
from core import User, Course, logger,the_headers
from uuid import uuid4
from concurrent.futures import ThreadPoolExecutor
import time
from json.decoder import JSONDecodeError
import requests

# 版本信息
version = '0.1.0-Alpha'

# 线程池
threads = ThreadPoolExecutor(max_workers=10)

# 帮助网页
HELP_PAGE_URL = 'file://../README.md'

# User对象
me = None
# 全局Course对象
course = None

# 课件信息存储
courses_info = {
    'courses': [],  # 所有课程列表
    'cells': [],  # 选中的课件列表
    'now_cell': {}  # 当前课件
}

# 登陆表单
login_info = {
    'appVersion': '2.8.43',
    'clientId': '',
    'equipmentApiVersion': '14.8',
    'equipmentAppVersion': '2.8.43',
    'equipmentModel': 'iPhone 11',
    'userName': '',
    'userPwd': '',
}


class CourseForClient(Course):
    def __init__(self, user):
        super().__init__(user)
        self._target = None
        # 由于父类私有属性无法继承，手动实现
        self.__s = user.req
        # 更新Headers
        self.new_headers = the_headers.copy()
        self.__s.headers.clear()
        self.__s.headers.update(self.new_headers)

    def finish_cell(self, course_id, class_id, cell_id):
        def gauge_update(now: int):
            # 课件进度更新
            # wx.CallAfter(target.cell_gauge.SetRange, total)
            wx.CallAfter(self._target.cell_gauge.SetValue, int(now))
            wx.CallAfter(self._target.cell_gauge_persentage.SetLabel,
                         f'{(self._target.cell_gauge.GetValue() / self._target.cell_gauge.GetRange()) * 100:.2f}%')

        time.sleep(1)
        cell_info = self.cell_info(course_id, class_id, cell_id)

        # 解决异常学习导致无法获取课件信息问题
        # task_cell = self.progress_task

        # self.now_cell['total'] = 1
        if cell_info:
            # 课件信息成功获取
            if int(cell_info['process']) == 100:
                # 课件进度已达到100%
                # 更新当前进度
                # self.now_cell['now'] = 1
                wx.CallAfter(self._target.cell_gauge.SetRange, 1)
                gauge_update(1)

                logger.info(f'课件 {cell_info["name"]}({cell_info["id"]}) 已达到100%完成度，将不会进行添加时长或页数操作')
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
                    'token': self.user.token,
                    'dtype': '1',
                }

                if '频' in cell_info['type']:
                    # 视频、音频类型
                    # task_cell = self.progress.add_task(f'[red]{cell_info["name"]}', total=int(cell_info['long']))

                    # self.progress.update(task_cell, completed=0,description=f'[yellow]{cell_info["name"]}({cell_info["type"]})', refresh=True)

                    # 更新进度
                    # self.now_cell['total'] = cell_info['long']
                    # self.now_cell['now'] = cell_info['now_long']
                    wx.CallAfter(self._target.cell_gauge.SetRange, int(cell_info['long']))
                    gauge_update(int(cell_info['now_long']))

                    def get_next_long(num, long):
                        if num == long:
                            # 防止卡循环
                            return long + 1
                        else:
                            new_num = num + uniform(18, 19.5)
                            if (new_num) < long:
                                if new_num - num > 20:
                                    return new_num - 1
                                else:
                                    return new_num
                            else:
                                return long

                    # 视频课件
                    num = cell_info['now_long']
                    long = cell_info['long']

                    num = get_next_long(num, long)
                    while num <= long:

                        self.__s.cookies.clear()

                        form_load['studyNewlyTime'] = num

                        res = self.__s.post(url='https://zjy2.icve.com.cn/api/common/Directory/stuProcessCellLog',
                                            data=form_load, headers=headers)

                        res_json = {}
                        try:
                            res_json = res.json()
                        except requests.exceptions.JSONDecodeError or JSONDecodeError:
                            logger.warning(f'课件{cell_info["name"]}({cell_id})意外返回：\n{res.content}')
                            raise Exception(f'课件{cell_info["name"]}({cell_id})意外返回：\n{res.content}\n')

                        if res_json['code'] == 1:
                            logger.info(
                                f'成功为课件 {cell_info["name"]}({cell_id}) 添加时长至 {num} ，总时长 {long} (注意此时长非真正意义上视频时长)')

                            # self.progress.update(task_cell, completed=num / long, description=f'[yellow]{cell_info["name"]}({cell_info["type"]})',refresh=True)
                            # self.now_cell['now'] = num
                            # 更新进度
                            gauge_update(num)

                            # 随机等待时长
                            wait = randint(5, 10)
                            logger.info(f'随机等待{wait}秒')
                            time.sleep(wait)

                            num = get_next_long(num, long)
                            continue
                        elif res_json['code'] == -2:
                            num = num - 0.00123
                            time.sleep(randint(2, 4))
                            continue
                        else:
                            logger.warning(f'返回信息：[{res.status_code}]：\n{res.content}')
                            logger.warning(f'为课件 {cell_info["name"]}({cell_id}) 添加时长失败：{res_json["msg"]}')

                            # 更新提示信息
                            wx.CallAfter(self._target.running_tips.SetLabel, f'课件 {cell_info["name"]}课程完成失败！')

                            break
                    # self.progress.update(task_cell, completed=1, description=f'[green]{cell_info["name"]}(完成课件)',refresh=True)
                    # 完成课件，使其进度到达100
                    gauge_update(self._target.cell_gauge.GetRange())
                    logger.info(f'已为课件 {cell_info["name"]}({cell_id}) 添加时长至{num}秒，目标时长{long}秒')
                else:
                    # 文档类型
                    # task_cell = self.progress.add_task(f'[red]{cell_info["name"]}', total=int(cell_info['page']))
                    # self.progress.update(task_cell, completed=0,description=f'[yellow]{cell_info["name"]}({cell_info["type"]})', refresh=True)

                    def get_next_page(now, page):
                        if now == page:
                            return page + 1
                        else:
                            if (now + 5) <= page:
                                return now + 5
                            else:
                                return page

                    now_page = cell_info['now_page']
                    page_long = cell_info['page']

                    # 设置进度
                    # self.now_cell['total'] = page_long
                    # self.now_cell['now'] = now_page
                    wx.CallAfter(self._target.cell_gauge.SetRange, page_long)
                    gauge_update(now_page)

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
                                            data=form_load, headers=headers)
                        # res = requests.post(url=apis['finish_cell'],headers=headers,data=form_load)
                        res_json = res.json()
                        if res_json['code'] == 1:
                            logger.info(f'成功为课件 {cell_info["name"]}({cell_id}) 添加页数至 {now_page} ，总页数 {page_long}')
                            # self.progress.update(task_cell, completed=now_page / page_long,description=f'[yellow]{cell_info["name"]}({cell_info["type"]})',refresh=True)
                            # 更新进度
                            # self.now_cell['now'] = now_page
                            gauge_update(now_page)

                            # 随机等待时长
                            wait = randint(5, 10)
                            logger.info(f'随机等待{wait}秒')
                            time.sleep(wait)

                            now_page = get_next_page(now_page, page_long)
                            continue
                        else:
                            logger.warning(f'为课件 {cell_info["name"]}({cell_id}) 添加页数失败：{res_json["msg"]}')
                            # 更新提示信息
                            wx.CallAfter(self._target.running_tips.SetLabel, f'课件 {cell_info["name"]}课程完成失败！')

                            break
                    # self.progress.update(task_cell, completed=1, description=f'[green]{cell_info["name"]}(完成课件)',refresh=True)

                    # 完成课件，使其进度到达100
                    gauge_update(self._target.cell_gauge.GetRange())

                    logger.info(f'已为课件 {cell_info["name"]}({cell_id}) 添加页数至 {now_page} ，目标页数 {page_long}')
        else:
            wx.CallAfter(self._target._login_dlg, '操作失败！', '登录可能已失效！')

    def target_set(self, target):
        self._target = target


def uuid_get():
    """
    生成用于登录的clientId
    """
    new_uuid = uuid4()
    new_uuid = str(new_uuid).replace('-', '')
    return new_uuid


def login(target, account, pswd):
    global me
    global login_info

    # 禁用掉登录控件
    wx.CallAfter(target.account_input.Disable)
    wx.CallAfter(target.pswd_input.Disable)
    wx.CallAfter(target.login_btn.Disable)

    wx.CallAfter(target.login_btn.SetLabel, '登录中...')
    wx.CallAfter(target.info_user.SetLabel, '登录中...')
    wx.CallAfter(target.info_id.SetLabel, '登录中...')

    login_info.update({
        'userName': account,
        'userPwd': pswd,
        'clientId': uuid_get()
    })
    me = User(login_info)
    login_status = me.login()
    if login_status['code'] == '1':
        # 登录成功
        # 开始更新GUI
        wx.CallAfter(target.login_btn.Enable)
        wx.CallAfter(target.login_btn.SetLabel, '重新登录')
        wx.CallAfter(target.info_user.SetLabel, me.name)
        wx.CallAfter(target.info_id.SetLabel, me.id)

        # 修改课程提示信息
        wx.CallAfter(target.func_tips_1.SetLabel, '请刷新课程列表')
        # 顺带刷新课程列表
        # wx.CallAfter(target.flash_course_list)
        # 解禁课程按钮
        wx.CallAfter(target.flash_course_btn.Enable)
        # wx.CallAfter(target.func_start_btn.Enable)
        # 解禁课程列表
        wx.CallAfter(target.course_list.Enable)
        wx.CallAfter(target.cell_list.Enable)
        # 加载Course对象
        global course
        course = Course(me)

    else:
        wx.CallAfter(target.account_input.Enable)
        wx.CallAfter(target.pswd_input.Enable)


def get_all_courses(target):
    global me
    global course
    # 禁用BTN
    wx.CallAfter(target.flash_course_btn.Disable)

    # 清空列表
    wx.CallAfter(target.course_list.Clear)

    # 修改课程提示信息
    wx.CallAfter(target.func_tips_1.SetLabel, '刷新课程列表中')

    # course = Course(me)
    course = CourseForClient(user=me)
    course_list = course.all_course

    if course_list['code'] == '1':
        # 成功获取
        global courses_info
        courses_info['courses'] = course_list['data']
        for c in courses_info['courses']:
            c_info = f"{courses_info['courses'].index(c) + 1} {c['courseName']} {c['mainTeacherName']} [{c['process']}%:{c['totalScore']}分]"
            wx.CallAfter(target.course_list.Append, c_info)
        # 解禁BTN
        wx.CallAfter(target.flash_course_btn.Enable)
        # 修改课程提示信息
        wx.CallAfter(target.func_tips_1.SetLabel, '选择一个课程')
    else:
        # 解禁BTN
        wx.CallAfter(target.flash_course_btn.Enable)
        wx.CallAfter(target._login_dlg, '获取课程列表失败！', course_list['msg'])
        # 修改课程提示信息
        wx.CallAfter(target.func_tips_1.SetLabel, '请刷新课程列表')


def get_all_cells(target, choose_index: int):
    global course
    global courses_info

    # 禁用课程刷新按钮
    wx.CallAfter(target.flash_course_btn.Disable)
    # 禁用func_start按钮
    wx.CallAfter(target.func_start_btn.Disable)
    if course:
        # 更新提示
        wx.CallAfter(target.func_tips_1.SetLabel, '获取课件中')
        # 清空课件列表
        courses_info['cells'].clear()
        wx.CallAfter(target.cell_list.Clear)

        cell_list = course.all_cell(course_id=courses_info['courses'][choose_index]['courseOpenId'],
                                    class_id=courses_info['courses'][choose_index]['openClassId'])
        if cell_list:
            courses_info['cells'] = cell_list
            for c in cell_list:
                c_info = f"[{c['type']}]{c['name']}  {c['process']}%"
                wx.CallAfter(target.cell_list.Append, c_info)
            # 解禁func_start按钮
            wx.CallAfter(target.func_start_btn.Enable)
        else:
            wx.CallAfter(target._login_dlg, '课程获取', '课程无课件或获取课件失败。如果获取失败，请前往项目地址反馈。')
            # 禁用func_start按钮
            wx.CallAfter(target.func_start_btn.Disable)
    else:
        wx.CallAfter(target._login_dlg, '获取课件失败', '登录似乎失效！')
        # 禁用func_start按钮
        wx.CallAfter(target.func_start_btn.Disable)
    # 解禁列表
    wx.CallAfter(target.course_list.Enable)
    # 解禁课程刷新按钮
    wx.CallAfter(target.flash_course_btn.Enable)
    # 重置提示
    wx.CallAfter(target.func_tips_1.SetLabel, '选择一个课程')


def finish_all_courses(target, course_index: int):
    global course

    course.target_set(target)

    now_course_id = courses_info['courses'][course_index]['courseOpenId']
    now_class_id = courses_info['courses'][course_index]['openClassId']

    # 总进度更新
    wx.CallAfter(target.total_gauge.SetRange, len(courses_info['cells']))
    wx.CallAfter(target.total_gauge.SetValue, 0)
    wx.CallAfter(target.total_gague_persentage.SetLabel,
                 f'{(target.total_gauge.GetValue() / target.total_gauge.GetRange()) * 100:.2f}%')

    for c in courses_info['cells']:
        # 指定为当前课件
        courses_info['now_cell'] = c
        # 提示更新
        wx.CallAfter(target.running_tips.SetLabel, f'{c["name"]}')
        # 主操作

        course.finish_cell(now_course_id, now_class_id, courses_info['now_cell']['id'])
        # 重置课件进度
        # wx.CallAfter(target.cell_gauge.SetValue, 0)
        # 更新总进度
        wx.CallAfter(target.total_gauge.SetValue, target.total_gauge.GetValue() + 1)
        wx.CallAfter(target.total_gague_persentage.SetLabel,
                     f'{(target.total_gauge.GetValue() / target.total_gauge.GetRange()) * 100:.2f}%')

    # 让进度到100%
    wx.CallAfter(target.total_gauge.SetValue,target.total_gauge.GetRange())
    wx.CallAfter(target._login_dlg, '任务结束', '已完成所有课件！')
    # 刷新列表
    get_all_cells(target, course_index)
    # 解禁列表
    wx.CallAfter(target.course_list.Enable)
    wx.CallAfter(target.cell_list.Enable)
    # 解禁按钮
    wx.CallAfter(target.flash_course_btn.Enable)
    wx.CallAfter(target.func_start_btn.Enable)

class MainLayout(Layout):
    def __init__(self, parent):
        super().__init__(parent)

        # 标题
        self.version_info()

        # 初始禁用
        self.flash_course_btn.Disable()
        self.func_start_btn.Disable()
        self.course_list.Disable()
        self.cell_list.Disable()

    def version_info(self):
        self.SetTitle(f'ICVE-HELPER [{version}]')

    def _login_dlg(self, title, content):
        dlg = wx.MessageDialog(None, u'{}'.format(content), u'{}'.format(title), wx.YES_DEFAULT | wx.ICON_QUESTION)
        if dlg.ShowModal() == wx.ID_YES:
            pass
        dlg.Close()

    def login(self, event):
        if self.account_input.IsThisEnabled():
            # 视为登录
            account = self.account_input.GetValue()
            pswd = self.pswd_input.GetValue()
            if account and pswd:
                # 提交登录任务
                threads.submit(login, self, account, pswd)

            else:
                self._login_dlg('登录失败！', '账号或密码不能为空！')
        else:
            # 视为重新登录
            dlg = wx.MessageDialog(None, u'{}'.format('你确定要重新登录吗？重新登录会清楚当前已获取到的课程课件信息，但是你可以重新登录为其它账号。'),
                                   u'{}'.format('退出登录'), wx.YES_NO | wx.ICON_QUESTION)
            if dlg.ShowModal() == wx.ID_YES:
                # 解禁账户输入
                self.account_input.Enable()
                self.pswd_input.Enable()
                # 清楚课程列表
                self.course_list.Clear()
                self.cell_list.Clear()
                global courses_info
                courses_info['courses'].clear()
                # 重置提示信息
                self.info_user.SetLabel('等待登录')
                self.info_id.SetLabel('等待登录')
                self.login_btn.SetLabel('登录')
                self.func_tips_1.SetLabel('等待登录')
                # 禁用按钮
                self.flash_course_btn.Disable()
                self.func_start_btn.Disable()
            else:
                pass
            dlg.Close()

    def flash_course_list(self, event):
        global me
        if me:
            threads.submit(get_all_courses, self)

    def help(self, event):
        browser_open_new(HELP_PAGE_URL)

    def get_cell_list(self, event):
        # 开始禁用列表，直到获取完毕
        self.course_list.Disable()
        threads.submit(get_all_cells, self, self.course_list.GetSelection())

    def finish_course(self, event):
        # 禁用所有列表
        self.course_list.Disable()
        self.cell_list.Disable()
        # 禁用按钮
        self.flash_course_btn.Disable()
        self.func_start_btn.Disable()

        threads.submit(finish_all_courses, self, self.course_list.GetSelection())

if __name__ == '__main__':
    app = wx.App()
    MainLayout(None).Show()
    app.MainLoop()
