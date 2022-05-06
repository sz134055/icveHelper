from datebase import insert, delet_one, get_one
from .core import User, Course

currentId = 0
currentUserId = 0
currentInfo = ''

nextUser = True


def pushEmail():
    pass


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
        currentId = user_info[0]
        currentUserId = user_info[2]

        currentInfo = '更新登陆状态'
        me = User({
            'userType': user_info[1],
            'userId': user_info[2],
            'userName': user_info[3],
            'userPwd': user_info[4],
            'newToken': user_info[5],
            'displayName': user_info[6],
            'employeeNumber': user_info[7],
            'url': user_info[8],
            'schoolName': user_info[9],
            'schoolId': user_info[10],
            'equipmentModel': user_info[11],
            'equipmentApiVersion': user_info[12],
            'clientId': user_info[13]
        })
        login_status = me.login_from_session()

        if login_status['code'] == '0':
            currentInfo = '用户无法登陆'
            # 删除这个无法登陆的用户
            delet_one()
            continue
        currentInfo = '登陆成功，等待获取所有课程'
        my_course = Course(me)
        currentInfo = '正在获取所有课程'
        all_my_course = my_course.all_course
        if isinstance(all_my_course,list):
            currentInfo = '所有课程获取完毕，准备开始任务...'
        else:
            currentInfo = '获取课程失败'
            delet_one()
            continue



    else:
        currentInfo = '闲置中...'
