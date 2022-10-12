# _*_coding:utf-8_*_
import wx
from layout import main as Layout
from webbrowser import open_new_tab as browser_open_new
from core import User, Course
from uuid import uuid4
from concurrent.futures import ThreadPoolExecutor

# 线程池
threads = ThreadPoolExecutor(max_workers=10)

# 帮助网页
HELP_PAGE_URL = ''

# User对象
me = None
# 全局Course对象
course = None

# 课件信息存储
courses_info = {
    'courses': [],  # 所有课程列表
    'cells':[]  # 选中的课件列表
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

    # 禁用BTN
    wx.CallAfter(target.flash_course_btn.Disable)

    # 清空列表
    wx.CallAfter(target.course_list.Clear)

    # 修改课程提示信息
    wx.CallAfter(target.func_tips_1.SetLabel, '刷新课程列表中')

    course = Course(me)
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

    if course:
        courses_info['cells'].clear()
        cell_list = course.all_cell(course_id=courses_info['courses'][choose_index]['courseOpenId'])
        if cell_list:
            courses_info['cells'] = cell_list
            for c in cell_list:
                c_info = f"[{c['type']}]{c['name']}  {c['process']}"
                wx.CallAfter(target.cell_list.Append,c_info)
        else:
            wx.CallAfter(target._login_dlg,'课程获取', '课程无课件或获取课件失败。如果获取失败，请前往项目地址反馈。')
    else:
        wx.CallAfter(target._login_dlg,'获取课件失败', '登录似乎失效！')
    # 解禁用列表
    wx.CallAfter(target.course_list.Enable)


class MainLayout(Layout):
    def __init__(self, parent):
        super().__init__(parent)

        # 初始禁用
        self.flash_course_btn.Disable()
        self.func_start_btn.Disable()
        self.course_list.Disable()
        self.cell_list.Disable()

        # self.course_list.Append(['APEX', 'BF5'])


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
            dlg = wx.MessageDialog(None, u'{}'.format('你确定要重新登录吗？重新登录会清楚当前已获取到的课程课件信息，但是你可以重新登录为其它账号'),
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


app = wx.App()
MainLayout(None).Show()
app.MainLoop()
