from core import User

def test_core(account,pswd):
    me = User()
    login_form = {
        'appVersion': '2.8.43',
        'clientId': '',
        'equipmentApiVersion': '15.0',
        'equipmentAppVersion': '2.8.43',
        'equipmentModel': 'iPhone 11',
    }
    me.login_setting(login_form)
    me.login(account,pswd)
    course = me.my_courses()
    if course:
        all_course = course.all_course
        print(all_course)
        course_choose_index = int(input('COURSE_CHOOSE_INDEX'))
        course_choose = all_course[course_choose_index]
        all_cell = course.all_cell(course_choose['courseOpenId'],class_id=course_choose['openClassId'])
        print(all_cell)
        cell_choose_index = int(input('CELL_CHOOSE_INDEX'))
        cell_choose = all_cell[cell_choose_index]
        print('START FINISH CELL')
        course.finish_cell(course_choose['courseOpenId'],course_choose['openClassId'],cell_choose['id'])
        print('DONE')
        print(course.task_process)
        comment = course.all_comment(cell_choose['id'],course_choose['courseOpenId'],course_choose['openClassId'])
        print(f'评论列表：{comment}')
        add_comment = course.add_comment(cell_choose['id'],course_choose['courseOpenId'],course_choose['openClassId'],input('COMMENT'),int(input('STAR')))
        if add_comment:
            print('ADD COMMENT SUCCESSFULLY')
        else:
            print('FAIL TO ADD COMMENT')
        print('ALL DONE')


if __name__ == '__main__':
    account = ''
    pswd = ''
    test_core(account,pswd)
