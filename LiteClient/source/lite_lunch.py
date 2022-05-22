from traceback import format_exc as traceback_exc
from rich.console import Console
from rich.table import Table
from lite import logger
from lite import core
import requests
import time
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from uuid import uuid4

# 适用于打包的的新版本
version = '0.5.2'
build = '20220516'

# 全局Console
console = Console()
# 全局信息加载

# LOGO 
__the_logo = '''
 _   _____   _     _   _____  
| | /  ___| | |   / / | ____| 
| | | |     | |  / /  | |__   
| | | |     | | / /   |  __|  
| | | |___  | |/ /    | |___  
|_| \_____| |___/     |_____| 
'''


def uuid_get():
    console.print('正在生成clientId，请稍后...')
    new_uuid = uuid4()
    new_uuid = str(new_uuid).replace('-', '')
    return new_uuid


def all_my_course(user):
    """
    获取所有课程表单并格式化输出
    : param user: 成功登陆的User类
    : return 获取到的完整课程表单
    """
    console.print('正在拉取你的所有课程')
    course = core.Course(user)

    course_table = Table(show_header=True, header_style="bold magenta")
    course_table.add_column("序号", justify='center', style='green')
    course_table.add_column("课程ID", justify='center', style='red')
    course_table.add_column("课程名", justify='center')
    course_table.add_column("你当前所处班级ID", justify="center", style='red')
    course_table.add_column("教师及其编号", justify="center")
    course_table.add_column("进度(可能不准确)", justify="center")
    course_table.add_column("得分(可能不准确)", justify="center")
    course_table.add_column("邀请码", justify="center")

    course_list = course.all_course
    num = 1
    for c in course_list:
        course_table.add_row(
            str(num),
            c['courseOpenId'],
            c['courseName'],
            c['openClassId'],
            f'{c["mainTeacherName"]}({c["mainTeacherNum"]})',
            str(c['process']),
            str(c['totalScore']),
            c['InviteCode']
        )
        num += 1
    console.print(course_table)
    console.print('->[yellow]进度与得分请以实际APP或网页为，仅供参考[/yellow]\n')

    return course_list


def all_cell(user, course_id, class_id=None):
    """
    获取某一课程的所有课件列表
    : param user : 成功登陆的User类
    : param course_id : 指定的课程ID
    : param class_id : 指定的开课ID 
    : return : 完整的课件列表 
    """
    console.print(f'[yellow]正在拉取课程 {course_id} 下的所有课件[/yellow]')

    course = core.Course(user)

    course_table = Table(show_header=True, header_style="bold magenta")
    course_table.add_column("课件名", justify='center')
    course_table.add_column("课程ID", justify='center', style='red')
    course_table.add_column("课件类型", justify="center", style='yellow')
    course_table.add_column("进度(可能不准确)", justify="center")

    with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            transient=True,
    ) as progress:
        task_all_cell = progress.add_task(description='获取所有课件', total=100, start=False)
        cell_list = course.all_cell(course_id=course_id, class_id=class_id)
        for c in cell_list:
            course_table.add_row(
                c['name'],
                c['id'],
                c['type'],
                str(c['process'])
            )
        progress.update(task_all_cell, completed=100, refresh=True)
        console.print('')  # 避免与进度条重合
        console.print(course_table)
        console.print('->[yellow]进度与得分请以实际APP或网页为，仅供参考[/yellow]\n')

    return cell_list


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
auto_login = False

# 课程选择
course_choose = ''
course_choose_id = None
course_choose_list = []
# 课程指令
command = ''

while True:
    # 主循环
    try:
        console.print(f'[right]{__the_logo}[/right]\nWELCOME ICVE！\n本程序仅学习之余制作，用于帮助学习\n如用于盈利后果自负\n', style='bold red')
        console.print('脚本全程你可以按 [red]CTRL+C或CTRL+Z 并回车[/red] 来返回上一步')

        console.print('版本：' + version, style='red')
        console.print('-' * 20)
        # broadcast()
        console.print('-' * 20)

        # 登陆
        if login_info['userName'] and login_info['userPwd']:
            if not auto_login:
                if console.input('已检测到你之前已经登陆过，是否直接登陆？\n[red]输入任意值来直接登陆[/red]，直接回车将需要重新输入\n'):
                    if console.input('是否开启下次自动登陆？\n下次需要重新登陆时会自动登陆，不会再次询问\n输入任意值来开启\n'):
                        auto_login = True
                else:
                    # 清空表单
                    login_info['userName'] = ''
                    login_info['userPwd'] = ''
                    raise KeyboardInterrupt
            else:
                console.print('自动登陆已启用')

        if not login_info['userName'] or not login_info['userPwd']:
            login_info['userName'] = console.input('请输入你的职教云账号\n')
            login_info['userPwd'] = console.input('\n请输入你的职教云密码\n[red]注意：密码不会显示出来[/red]\n', password=True)

            # need_auto_comment = 'true'
            # auto_comment_info = {}
            auto_comment_info = {
                'star': 5,
                'content': '好'
            }
            need_auto_comment = console.input(
                '\n是否需要对课件自动评论？[red]留空为禁用，输入任意值启用[/red]\n会自动对比前20*[red]1[/red]的评论以避免出现重复评论\n你可以暂时不启用，待稍后在具体到某一课件时再考虑启用与否\n')
            if need_auto_comment:
                auto_comment_info_star = console.input('\n输入课件评论评分（单位星，填写范围1-5）\n回车留空或错误输入默认为[green]5[/green]\n')
                auto_comment_info_content = console.input('\n输入课件评论内容\n回车留空或错误输入默认为[green]好！[/green]\n')
                try:
                    auto_comment_info_star = int(auto_comment_info_star)
                    auto_comment_info['star'] = auto_comment_info_star
                except ValueError:
                    console.print('\n[red]评分未填写有误，已设为默认值[/red]')
                if auto_comment_info_content:
                    auto_comment_info['content'] = auto_comment_info_content
            else:
                console.print('\n[red]自动评论被取消[/red]')
                auto_comment_info = {}

            # 高级登陆
            console.print('\n是否需要更加详细的高级登陆项？此项可以指定你想要模拟登陆的手机型号等\n默认已自动生成无需手动，不影响账号登陆及后续操作')
            if console.input('\n默认为不启动，输入任意字符来配置高级启动项\n'):
                # CLIENTID
                __user_client_id = console.input(f'输入CLIENT ID，可以视为你设备的唯一身份证号\n留空或不满足32位值将会重新生成\n')
                if __user_client_id and len(__client_id) >= 32:
                    __client_id = __user_client_id
                else:
                    __client_id = uuid_get()
                    console.print(f'CLIENT ID 已重新生成为 [yellow]{__client_id}[/yellow]')
                login_info['clientId'] = __client_id

                # MODEL
                __user_device_model = console.input(
                    f'\n输入手机型号\n当前默认设置为[green]{login_info["equipmentModel"]}[/green]\n留空会保持默认\n')
                if __user_device_model:
                    login_info['equipmentModel'] = __user_device_model

                # OS 
                __user_device_os = console.input(
                    f'\n输入手机系统版本\n当前默认设置为[green]{login_info["equipmentApiVersion"]}[/green]\n留空会保持默认\n')
                if __user_device_os:
                    login_info['equipmentApiVersion'] = __user_device_os

            # CLIENT ID 检测
            if not login_info['clientId']:
                login_info['clientId'] = uuid_get()

            # 详细登陆表单展示
            console.print('完整登陆选项如下：')
            login_info_table = Table(show_header=True, header_style="bold magenta")
            login_info_table.add_column("登陆项", justify='center')
            login_info_table.add_column("当前值", justify='center')
            login_info_table.add_column("对应setting文件中选项（弃用）", justify="center")
            login_info_table.add_column("说明", justify="center")
            login_info_table.add_row(
                "userName",
                login_info['userName'],
                "account",
                "职教云账号"
            )
            login_info_table.add_row(
                "userPwd",
                '密码不显示',
                "pswd",
                "职教云密码",
            )

            login_info_table.add_row(
                "appVersion",
                login_info['appVersion'],
                "ios_version和ios_build或android_version",
                "用于指定职教云APP版本[red]（注意当前不支持替换）[/red]",
            )
            login_info_table.add_row(
                "equipmentAppVersion",
                login_info['equipmentAppVersion'],
                "ios_version和ios_build或android_version",
                "用于指定职教云APP版[red]（注意当前不支持替换）[/red]",
            )
            login_info_table.add_row(
                "equipmentApiVersion",
                login_info['equipmentApiVersion'],
                "os_version",
                "用于指定你想要模拟登陆的设备系统版本，如14.8",
            )
            login_info_table.add_row(
                "equipmentModel",
                login_info['equipmentModel'],
                "model_name",
                "模拟登陆的设备名称，如iPhone 11，[red]不影响登陆[/red]",
            )
            login_info_table.add_row(
                "clientId",
                login_info['clientId'],
                "clientId",
                "模拟登陆的设备UUID，[red]不影响登陆[/red]",
            )

            if auto_comment_info:
                login_info_table.add_row(
                    "star",
                    str(auto_comment_info['star']),
                    "star",
                    "用于自动课件评论的评分",
                )
                login_info_table.add_row(
                    "comment",
                    auto_comment_info['content'],
                    "comment",
                    "用于自动课件评论的评论",
                )

            console.print(login_info_table)
            # 详细登陆表单展示
            if console.input('确认没有问题后回车开始登陆，[red]输入任意值重新输入[/red]'):
                continue

        # 开始登陆
        if login_info['userName'] and login_info['userPwd']:
            console.print('正在尝试登陆...', style='yellow')

        try:
            me = core.User(login_info)
            # 登陆检查
            me.user_info['userId']
        except requests.exceptions.HTTPError:
            console.print('\n[red]无网络链接或无法链接至职教云服务器，请检查网络或稍后再试[/red]')
            console.input('[red]->[/red]输入任意字符或回车继续')
            auto_login = False
            continue
        except KeyError:
            console.input('登陆失败！按任意键重试')
            auto_login = False
            continue

        console.print('登陆成功！', style='green')

        while True:
            # 课程主循环

            course_list = all_my_course(user=me)


            # 课程选择
            def make_course_choose(choose: str):
                global course_choose_list
                if '/' in choose:
                    l, r = choose.split('/')
                    c_choose_list = course_list[int(l) - 1:int(r)]
                    for c_choose in c_choose_list:
                        course_choose_list.append(c_choose['courseOpenId'])

                else:
                    course_num_list = choose.split(' ')
                    for c in course_num_list:
                        course_choose_list.append(course_list[int(c) - 1]['courseOpenId'])


            while True:
                # 课程任务主循环
                #global auto_comment_info
                try:
                    if not course_choose_id:
                        course_choose = console.input(
                            '\n[red]->[/red]选择一门课程（其名称或完整的ID）以继续：\n[yellow]->[/yellow]名称可以不填写完全，例如课程 大学生创新创业，可写大学生创新\n[green]->[/green]但对于名称略有重复的课程如 大学语文与大学英语 请至少填写为 大学语或大学英\n'
                            '现在你可以使用[red]d+序号[/red]选课甚至多选（序号见上表,序号选择必须保证第一个是d），用空格分割，如：[red]d1 2 3[/red]，或者使用斜杠(/)分割来选择一个范围，如：[red]d1/3[/red]，表示选中序号[red]1，2，3[/red]这三门课程\n')
                        if 'd' == course_choose[0]:
                            # 序号选择
                            course_choose_num = course_choose.replace('d', '')
                            make_course_choose(course_choose_num)
                            course_choose_id = 'wait'  # 占位
                            continue
                    elif course_choose_list:
                        if course_choose_id == 'wait':
                            # 转载COURSE ID
                            course_choose_id = course_choose_list[0]
                        else:
                            course_choose_list.remove(course_choose_id)
                            try:
                                course_choose_id = course_choose_list[0]
                            except IndexError:
                                course_choose_id = None
                                console.print('已完成所有选择的课程')
                    else:
                        if console.input(f'\n[red]->[/red]当前默认选择上次课程[yellow] {course_choose}[/yellow]，回车继续，任意字符重新选择'):
                            course_choose_id = ''
                            continue
                    # 课程选择

                    course_choose_info = {}
                    if not course_choose_id:
                        continue
                    else:
                        for c in course_list:
                            if course_choose in c['courseName'] or course_choose == c[
                                'courseOpenId'] or course_choose_id == \
                                    c['courseOpenId']:
                                course_choose = c['courseName']
                                course_choose_info = c.copy()
                                break

                        if not course_choose_info:
                            console.print('未能选中任何课程，请重新选择', style='red')
                            continue

                    console.print(f'\n当前已选中课程[red] {course_choose} ({course_choose_id})[/red]\n')
                    if not command:
                        command = console.input(
                            '[red]->[/red]请输入对应操作的序号，输入其它非序号来重新选择课程：\n1-自动完成课程下所有课件\n2-显示当前课程的课件完成信息\n')
                    if command == '1':

                        cell_list = all_cell(me, course_choose_info['courseOpenId'], course_choose_info['openClassId'])

                        with Progress(
                                SpinnerColumn(),
                                TextColumn("[progress.description]{task.description}"),
                                BarColumn(),
                                TimeElapsedColumn(),
                                TextColumn("[progress.percentage]{task.percentage:>3.0f}%")
                        ) as progress:
                            my_course = core.Course(me)
                            # 设置rich progress
                            my_course.set_progress(progress=progress)

                            # 重置当前课件为第一课件
                            try:
                                my_course.change_corseware(course_id=course_choose_info['courseOpenId'],
                                                           class_id=course_choose_info['openClassId'],
                                                           cell_id=cell_list[0]['id'],
                                                           cell_name=cell_list[0]['name'])
                            except IndexError:
                                console.print('[yellow]->[/yellow]课程下无课件，跳过')

                                continue

                            # 总进度
                            task_total = progress.add_task('[yellow]总进度', total=len(cell_list))
                            task_cell = progress.add_task('当前课程', total=1)
                            my_course.set_progress_task(task_cell)
                            if auto_comment_info:
                                task_comment = progress.add_task('[red]当前课程评论', total=3)

                            for cell in cell_list:
                                # 单课进度
                                # task_cell = progress.add_task(f'[red]{cell["name"]}',total=10)

                                # progress.update(task_cell,completed=0,description=f'[yellow]{cell["name"]}[视频]',refresh=True)
                                if cell['process'] != 100:
                                    # 如果课件不为100%进度则开始刷课
                                    my_course.finish_cell(course_id=course_choose_info['courseOpenId'],
                                                          class_id=course_choose_info['openClassId'],
                                                          cell_id=cell['id'])
                                    time.sleep(2)
                                else:
                                    progress.update(task_cell, completed=1, description=f'[green]{cell["name"]}(跳过课件)',
                                                    refresh=True)
                                # progress.update(task_cell,completed=8,description=f'[rgb(0,128,128)]{cell["name"]}[对比评论]',refresh=True)

                                # 评论任务
                                if auto_comment_info:
                                    progress.update(task_comment, completed=0,
                                                    description=f'[rgb(0,128,128)]{cell["name"]}[获取评论]',
                                                    refresh=True)
                                    comment_info = my_course.all_comment(cell['id'], course_choose_info['courseOpenId'],
                                                                         course_choose_info['openClassId'], 1)
                                    progress.update(task_comment, completed=1,
                                                    description=f'[rgb(0,128,128)]{cell["name"]}[对比评论]',
                                                    refresh=True)
                                    is_comment = False
                                    for comment in comment_info:
                                        if me.id == comment['user_id']:
                                            # console.print('已经评论过此课件，跳过')
                                            is_comment = True
                                            # progress.update(task_cell,completed=9,description=f'[rgb(0,128,128)]{cell["name"]}[跳过评论]',refresh=True)
                                            progress.update(task_comment, completed=2,
                                                            description=f'[rgb(0,128,128)]{cell["name"]}[跳过评论]',
                                                            refresh=True)
                                            break

                                    if not is_comment:
                                        progress.update(task_comment, completed=2,
                                                        description=f'[rgb(0,128,128)]{cell["name"]}[添加评论]',
                                                        refresh=True)
                                        my_course.add_comment(cell['id'], course_choose_info['courseOpenId'],
                                                              course_choose_info['openClassId'], auto_comment_info['content'], str(auto_comment_info['star']))

                                        progress.update(task_comment, completed=3,
                                                        description=f'[rgb(0,128,128)]{cell["name"]}[完成评论]',
                                                        refresh=True)

                                progress.update(task_total, advance=1, refresh=True)
                                time.sleep(2)

                            # 课件结束，删除最上端课件ID以让脚本选择下一个课件
                            try:
                                del course_choose_list[0]
                                course_choose_id = 'wait'
                            except IndexError:
                                # 列表已被清空
                                course_choose_id = None
                            finally:
                                continue

                    elif command == '2':
                        cell_list = all_cell(me, course_choose_info['courseOpenId'], course_choose_info['openClassId'])
                        console.input('[red]->[/red]输入任意字符或回车继续')
                    else:
                        console.print('重新选择课程')
                        continue
                except KeyboardInterrupt:
                    # 清空课程选择
                    course_choose = ''
                    course_choose_id = None
                    course_choose_list = []
                    # 清空课程指令
                    command = ''
                    console.print('已清空全部课程选择')
                    continue

    except KeyboardInterrupt:
        console.print('返回登陆')
        continue
    except:
        console.input('\n' + traceback_exc())
        console.input('\n[red]发生错误，报错如上。按任意键继续[/red]')
        continue
