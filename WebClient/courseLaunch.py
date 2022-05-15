import time

from web.datebase import insert, delet_one, get_one
from web.core import User, Course
from web.email2c import Mail
from web.config import coon
# from web.logger import Logger
from web.logger import Logger
import traceback

log = Logger(name='COURSE', file=True)
logger = log.get_logger()


class Current:
    def __init__(self):
        self.now_info = ''
        self.now_id = 0
        self.now_user = 0

    @property
    def info(self):
        return self.now_info

    @info.setter
    def info(self, value):
        self.now_info = value
        logger.info(self.now_info)

    @property
    def id(self):
        return self.now_id

    @id.setter
    def id(self, value):
        self.now_id = value

    @property
    def user(self):
        return self.now_user

    @user.setter
    def user(self, value):
        self.now_user = value


now = Current()
'''
currentId = 0  # 当前用户序号
currentUserId = 0  # 当前用户ID
currentInfo = '课程程序未启动'  # 当前状态
'''
# 以下进度针对单个课件
currentProcess = 0  # 当前进度
currentTotalProcess = 0  # 当前总进度

nextUser = True


def pushEmail(recv, title, main_content, to_admin=False):
    content = """
    <div style="text-align:center;margin:50px 0">
    <h1>此邮件来自ICVE-HELPER WEB端程序</h1>
    <span>由程序自动发送，请不要回复</span>
    </div>
    """
    content = content + main_content
    mail = Mail()
    mail.set_content(content)
    mail.set_title(title)
    if not to_admin:
        mail.set_recv(recv)
    else:
        mail.to_admin()
    mail.send()


def fakeTest():
    while True:
        user_info = get_one()
        if user_info:
            now.id = user_info[0]
            now.info = f'目前用户序号为 {user_info[0]}'
            time.sleep(1)
            now.info = '更新登陆状态'
            time.sleep(1)
            now.info = '当前任务：ABC123'
            time.sleep(3)
            now.info = '任务完成'
            time.sleep(1)
            now.info = '准备切换用户'
            time.sleep(1)
        else:
            insert(1, '123', 'TheName', '112233', 'IAMTOKEN', 'JOJO', '2020123456', 'https://www.noexist.com',
                   'TheSchool', 'ID123', 'iPhone 11', '15.0', 'ashdkahasjkdsa', 'eamil@.com')


if __name__ == '__main__':
    if coon.get('debug', 'fake') == 'true':
        logger.info('FAKE运行模式')
        print('FAKE运行模式')
        fakeTest()

    else:
        while True:
            # 程序主循环
            # 元组,(
            #         id,
            #         userType,
            #         userId,
            #         userName,
            #         userPwd,
            #         newToken,
            #         displayName,
            #         employeeNumber,
            #         url,
            #         schoolName,
            #         schoolId,
            #         equipmentModel,
            #         equipmentApiVersion,
            #         clientId
            #         )

            user_info = get_one()  # 获取表顶部用户信息
            if user_info:
                # 更新状态
                now.id = user_info['id']
                now.user = user_info['userId']
                user_email = user_info['email']
                now.info = f"目前用户序号为 {user_info['id']}"

                now.info = '更新登陆状态'
                me = User({
                    'equipmentAppVersion':user_info['appVersion'],
                    'appVersion':user_info['appVersion'],
                    'userName': user_info['userName'],
                    'userPwd': user_info['userPwd'],
                    'equipmentModel': user_info['equipmentModel'],
                    'equipmentApiVersion': user_info['equipmentApiVersion'],
                    'clientId': user_info['clientId']
                })
                try:
                    #login_status = me.login_from_session()
                    login_status = me.login()

                    if login_status['code'] == '0':
                        now.info = f'序号 {now.id} 的用户无法登陆'
                        # 删除这个无法登陆的用户
                        delet_one()

                        mail_info = f"""
                        <div style="text-align:center;margin:50px 0">
                        <p>你的账户 <b>{me.account}</b> 在登陆时候发生错误</p>
                        <p>为了不阻塞整个队列，现已将你的账户从队列中<b>移除（包括数据库）</b></p>
                        <p>你可以重新登陆验证并开始排队等待</p>
                        <p>或者在此处下载所有文件自助完成相应操作<a href='https://gitee.com/saucer216/icve-helper/tree/main/release/Lite/source'>ICVE-HELPER LITE</a></p>
                        </div>
                        """
                        pushEmail(user_email, 'OoOpS~ 你的ICVE账户登陆遇到问题', mail_info)
                        continue

                    now.info = f'序号 {now.id} 用户登陆成功，等待获取所有课程'
                    my_course = Course(me)
                    now.info = f'正在获取序号 {now.id} 用户所有课程'
                    all_my_course = my_course.all_course
                    if not isinstance(all_my_course, list):
                        now.info = f'获取序号 {now.id} 用户课程失败'
                        delet_one()

                        mail_info = f"""
                                   <div style="text-align:center;margin:50px 0">
                                   <p>你的账户 <b>{me.account}</b> 在获取所有课程时候发生错误</p>
                                   <p>为了不阻塞整个队列，现已将你的账户从队列中<b>移除（包括数据库）</b></p>
                                   <p>你可以重新登陆验证并开始排队等待</p>
                                   <p>或者在此处下载所有文件自助完成相应操作<a href='https://gitee.com/saucer216/icve-helper/tree/main/release/Lite/source'>ICVE-HELPER LITE</a></p>
                                   </div>
                                   """
                        pushEmail(user_email, 'OoOpS~ 你的ICVE账户登陆遇到问题', mail_info)
                        continue

                    now.info = f'所有序号 {now.id} 用户课程获取完毕，准备开始任务...'

                    mail_info = f"""
                               <div style="text-align:center;margin:50px 0">
                               <p>你的账户 <b>{me.account}</b> 现在已经开始进行自动完成课件操作</p>
                               <p>预计整个流程会持续一到两个小时，<b>并且会在完毕时给你发送邮件</b>，因此如果你在收到此邮件后超过四五小时后仍未继续收到来信<b>（请先检查垃圾邮箱）</b>，这表示程序出现异常，请自行检查你的课件进度</p>
                               <p style="margin-top:10px">整个过程中，可能会因频率过高（已尽可能优化）导致程序中断，为了不阻塞整个队列，会将你的账户从队列中<b>移除（包括数据库）</b></p>
                               <p>大部分情况下，这个情况并不会发生，但是某些课程，可能会多次触发此异常，暂时无解</p>
                               <p>同时你的账户可能会触发某些机制导致账户异常，如无法评论等，会持续半小时左右，你可以继续登陆验证提交等待重新开始任务</p>
                               <p><b>在未来一至两小时内或在收到结果邮件前，最好不要对课件进行相关操作，如查看课件，评论等，这会与程序冲突！</b></p>
                               </div>
                               """
                    pushEmail(user_email, '你的ICVE任务现已开启运行', mail_info)

                    for course in all_my_course:
                        now.info = f'获取课程 {course["courseName"]} 下所有课件中...'
                        all_course_cell = my_course.all_cell(course['courseOpenId'])
                        now.info = '获取成功！初始化任务中...'
                        # 重置当前课件为第一课件
                        try:
                            my_course.change_corseware(course_id=course['courseOpenId'],
                                                       class_id=course['openClassId'], cell_id=all_course_cell[0]['id'],
                                                       cell_name=all_course_cell[0]['name'])
                        except IndexError:
                            # 无课件，跳过
                            now.info = '无课件，跳过...'
                            continue

                        for cell in all_course_cell:
                            now.info = f'当前课件 {course["courseName"]} - {cell["name"]}({cell["id"]}) 课件任务开始'
                            if cell['process'] != 100:
                                my_course.finish_cell(course_id=course['courseOpenId'],
                                                      class_id=course['openClassId'], cell_id=cell['id'])
                                time.sleep(2)

                            time.sleep(2)
                            if not user_info['comment_star'] or not user_info['comment_content']:
                                now.info = '用户选择跳过评论'
                                continue

                            now.info = f'当前课件 {course["courseName"]} - {cell["name"]}({cell["id"]}) 评论任务开始'
                            comment_info = my_course.all_comment(cell['id'], course['courseOpenId'],
                                                                 course['openClassId'],
                                                                 1)
                            is_comment = False
                            for comment in comment_info:
                                if me.id == comment['user_id']:
                                    # 已经评论过此课件，跳过
                                    is_comment = True
                                    break
                            if not is_comment:
                                my_course.add_comment(cell['id'], course['courseOpenId'], course['openClassId'],
                                                      user_info['comment_content'], user_info['comment_star'])
                            now.info = f'当前课件 {course["courseName"]} - {cell["name"]}({cell["id"]}) 任务结束'
                            time.sleep(2)

                    now.info = f'序号 {now.id} 的用户任务已全部完成，准备切换至下一位用户'
                    mail_info = f"""
                    <div style="text-align:center;margin:50px 0">
                    <p>你的账户 <b>{me.account}</b> 所有任务已经完成！</p>
                    <p>请自行查看你的课程进度及相应课件评论情况</p>
                    <br>
                    <h4>Q:为什么有的课件不是100%完成？</h4>
                    <p><b>A:</b></p>
                    <p>目前原因不明，且因人而异，可能与开课设置有关，实际上你的课件进度基本全部到达100%状态（至少程序判断如此）</p>
                    <p>这并不会影响你多少平时分，如果你发现确实有课件未能达到100%，你可以再次提交，或自行手动完成</p>
                    <p>或者你也可以在此处下载所有文件自助完成相应操作<a href='https://gitee.com/saucer216/icve-helper/tree/main/release/Lite/source'>ICVE-HELPER LITE</a></p>
                    """
                    pushEmail(user_email, '你的ICVE任务已全部完成！', mail_info)

                except Exception as e:
                    mail_info = f"""
                    <div style="text-align:center;margin:50px 0">
                    <p>用户 {me.account} 任务失败</p>
                    <p>异常如下：</p>
                    {e}
                    详细：
                    {traceback.format_exc()}
                    <p>当时任务进度信息：</p>
                    {now.info}
                    </div>
                    """
                    pushEmail('', '出现异常！', mail_info, to_admin=True)

                    mail_info = f"""
                    <div style="text-align:center;margin:50px 0">
                   <p>你的账户 <b>{me.account}</b> 任务在运行时发生错误</p>
                   <p>当时任务进度信息:</p>
                   {now.info}
                   <br>
                   <p>此错误已通知管理员</p>
                   <p>为了不阻塞整个队列，现已将你的账户从队列中<b>移除（包括数据库）</b></p>
                   <p>你可以重新登陆验证并开始排队等待任务开始</p>
                   <p>或者在此处下载所有文件自助完成相应操作<a href='https://gitee.com/saucer216/icve-helper/tree/main/release/Lite/source'>ICVE-HELPER LITE</a></p>
                   </div>
                    """
                    pushEmail(user_email, 'OoOpS~ 你的ICVE任务发生错误！', mail_info)
                    # 删除该账户
                    delet_one()
            else:
                now.info = '闲置中...'
                time.sleep(3)