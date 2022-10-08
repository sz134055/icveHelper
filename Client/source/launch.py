# _*_coding:utf-8_*_
import wx
from layout import main as Layout
from webbrowser import open_new_tab as browser_open_new
from core import User,Course
from uuid import uuid4

# 帮助网页
HELP_PAGE_URL = ''

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

class MainLayout(Layout):
    def __init__(self, parent):
        super().__init__(parent)

        self.me = None

    def login(self, event):
        def login_dlg(title,content):
            dlg = wx.MessageDialog(None, u'{}'.format(content), u'{}'.format(title), wx.YES_DEFAULT | wx.ICON_QUESTION)
            if dlg.ShowModal() == wx.ID_YES:
                pass
            dlg.Close()

        if self.account_input.IsThisEnabled():
            # 视为登录
            account = self.account_input.GetValue()
            pswd = self.pswd_input.GetValue()

            if not account and not pswd:
                login_dlg('登录失败！','账号或密码不能为空!')
            else:
                global login_info
                # 开始登录
                login_info.update({'userName': account,'userPwd': pswd,'clientId':uuid_get()})
                self.me = User(login_info)
                login_status = self.me.login()
                if login_status['code'] == '1':
                    # 登录成功
                    self.account_input.Disable()
                    self.pswd_input.Disable()
                    login_dlg('登录成功！', '请务必在使用前查看使用说明！')
                    # 开始刷新信息
                    self.info_user.SetLabel(self.me.name)
                    self.info_id.SetLabel(self.me.id)
                    self.login_btn.SetLabel('退出登录')
                else:
                    login_dlg('登录失败！',login_status['msg'])
        else:
            # 视为退出登录
            # 清空
            self.me = None
            '''
            self.account_input.Clear()
            self.pswd_input.Clear()
            '''
            self.login_btn.SetLabel('登录')


    def flash_course_list( self, event ):
        pass

    def help(self, event):
        browser_open_new(HELP_PAGE_URL)


app = wx.App()
MainLayout(None).Show()
app.MainLoop()
