import smtplib
from email.mime.text import MIMEText
import os
from configparser import ConfigParser

WORK_PATH = os.path.split(os.path.realpath(__file__))[0]

coon = ConfigParser()
if not os.path.exists(WORK_PATH + '/setting.ini'):
    raise FileNotFoundError('未能找到配置文件，请务必将自带的setting.ini放置于软件同一目录下')
coon.read(WORK_PATH + '/setting.ini')


class Mail:
    def __init__(self):
        self.__host = ''  # 邮箱服务器
        self.__user = ''  # 邮件发送者
        self.__pswd = ''  # 部分邮箱为授权码
        self.__sender = ''  # 邮件发送者地址
        self.__content = ''  # 邮件内容
        self.__title = ''  # 邮件标题
        self.__recv = ''  # 接收者邮箱
        # 更新发送者信息及服务器
        self.update_sender()

    def set_recv(self, recv):
        self.__recv = recv

    def set_content(self, content):
        self.__content = content

    def set_title(self, title):
        self.__title = title

    def update_sender(self):
        self.__host = coon.get('email', 'host')
        self.__user = coon.get('email', 'user')
        self.__pswd = coon.get('email', 'pswd')
        self.__sender = coon.get('email', 'sender')

    def to_admin(self):
        self.set_recv(coon.get('email', 'admin'))

    def send(self):
        def email_it():
            msg = MIMEText(self.__content, 'html', 'utf-8')
            msg['Subject'] = self.__title
            msg['From'] = self.__sender
            msg['To'] = self.__recv

            return msg.as_string()

        # 登录并发送邮件
        try:
            smtp = smtplib.SMTP_SSL(self.__host, 465)
            smtp.login(self.__sender, self.__pswd)
            smtp.sendmail(self.__sender, self.__recv, email_it())

            print('SUCCESS')
        except smtplib.SMTPException as e:
            print('链接错误:' + str(e))


if __name__ == '__main__':
    mail = Mail()
    mail.set_recv('')
    mail.set_content('THIS IS A EMAIL FROM PYTHON!')
    mail.set_title('HELLO EMAIL')
    mail.send()
