from core import User


def test_core(account, pswd):
    # 初始化一个User对象
    me = User()

    # 可自定义登录表单，表单的用处请见 docs目录下的 职教云API-DOC.md 中登录一章，不是必须步骤
    login_form = {
        'appVersion': '2.8.43',
        'clientId': '',
        'equipmentApiVersion': '15.0',
        'equipmentAppVersion': '2.8.43',
        'equipmentModel': 'iPhone 11',
        'userName': '',
        'userPwd': ''
    }
    # 设置登录表单，不是必须步骤
    me.login_setting(login_form)

    # 设置登录密码，可在上一步就设置账号密码然后直接调用login()方法，不用填入账号密码
    # 不设置登录表单，直接调用login()方法并填入账号与密码也可登录，会使用或生成相应的登录表单项
    me.login(account, pswd)

    # 获取一个Course对象，其它生成办法请自行查询源码
    course = me.my_courses()

    if course:
        # 获取用户名下的所有课程列表
        all_courses = course.all_courses
        print(all_courses)

        course_choose_index = int(input('COURSE_CHOOSE_INDEX'))
        course_choose = all_courses[course_choose_index]

        # 获取选定课程下所有课件列表
        all_cell = course.all_cell(course_choose['courseOpenId'], class_id=course_choose['openClassId'])
        print(all_cell)
        cell_choose_index = int(input('CELL_CHOOSE_INDEX'))
        cell_choose = all_cell[cell_choose_index]
        print('START_FINISH_CELL')

        # 完成用户选定的一个课件（刷课）
        course.finish_cell(course_choose['courseOpenId'], course_choose['openClassId'], cell_choose['id'])
        print('DONE')

        # 查看Course对象自维护的任务对象
        # 当finish_cell()方法被调用后，会自动更新task_process来汇报课件完成进度
        print(course.task_process)

        # 获取选定课件下的所有评论
        comment = course.all_comment(cell_choose['id'], course_choose['courseOpenId'], course_choose['openClassId'])
        print(f'评论列表：\n{comment}')

        # 为选定的课件添加一个评论
        add_comment = course.add_comment(cell_choose['id'], course_choose['courseOpenId'], course_choose['openClassId'],
                                         input('COMMENT'), int(input('STAR')))

        # 是否成功添加评论
        if add_comment:
            print('ADD_COMMENT_SUCCESSFULLY')
        else:
            print('FAIL_TO_ADD_COMMENT')
        print('ALL_DONE')


if __name__ == '__main__':
    # 账号
    account = ''
    # 密码
    pswd = ''

    test_core(account, pswd)
