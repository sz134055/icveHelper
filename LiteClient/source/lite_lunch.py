from traceback import format_exc as traceback_exc
from rich.console import Console
from rich.table import Table
from core import logger, User, Course
import requests
from time import sleep as time_sleep
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from os import listdir
from threading import Thread,enumerate

# 适用于打包的的新版本
version = '0.6.0'
build = '20221214'

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

def progress_func(p: Progress, task_len: int,c:Course):
    """
    用于自动更新进度条

    :param p: console.Progress
    :param task_len: 总任务长度
    :param c: core.Course
    :return: None
    """
    # 上一任务
    __last_task = ''
    # 当前任务
    __now_task = ''

    # 进度条 总任务
    task_total = p.add_task('[yellow]总进度', total=task_len)
    task_cell = p.add_task(f'[green]当前课程', total=1)
    # 进度条 当前任务
    while not p.finished:
        # 当总任务并未结束时
        while c.process_name:
            # 当有任务时
            __now_task = c.process_name
            p.update(task_cell,total=c.process_total,description=f'[yellow]{c.process_name}',refresh=True)
            while c.process_now <= c.process_total and __now_task != __last_task:
                # 当当前任务为完成时
                p.update(task_cell, completed=c.process_now, description=f'[yellow]{c.process_name}', refresh=True)
                if c.process_now == c.process_total:
                    p.update(task_cell,completed=c.process_total,description=f'[yellow]{c.process_name}',refresh=True)
                    # 总进度步进1
                    p.update(task_total,advance=1,refresh=True)
                    # 保存已经完成的任务名，防止重复刷新总进度导致其100%
                    __last_task = c.process_name
                    break
            time_sleep(0.4)
        else:
            # 修复任务完成时while循环不退出导致高占用
            break

# 登陆表单
auto_login = False

# 课程指令
command = ''

me = User()
while True:
    # 主循环
    try:
        console.print(f'[right]{__the_logo}[/right]\nWELCOME ICVE！\n本程序仅学习之余制作，用于帮助学习\n如用于盈利后果自负\n', style='bold red')
        console.print('[red]发生任何报错请截图并配合logs下日志文件提交至仓库issue\n')
        console.print('登录超时请多试几次...')
        console.print('版本：' + version, style='red')
        console.print('-' * 20)
        # broadcast()
        console.print('-' * 20)

        # 查询存档
        try:
            __save_list = listdir('save')
            if __save_list:
                console.print('发现已保存的登录记录')
                __save_user_table = Table(show_header=False, header_style="bold magenta")
                __save_user_table.add_column("序号", justify='center')
                __save_user_table.add_column("账户", justify='center')
                for __save_user in __save_list:
                    __save_user_table.add_row(str(__save_list.index(__save_user) + 1), __save_user.replace('.json', ''))

                console.print(__save_user_table)

                command = console.input('输入对应序号直接登录，或直接回车输入账号密码进行登录\n在此输入：')
                if command:
                    if int(command) < 1 or int(command) > len(__save_list):
                        console.print('你输入了错误的序号')
                    else:
                        __save_info = me.get_save(__save_list[int(command) - 1].replace('.json', ''))
                        me.login_setting({
                            "appVersion": __save_info['info']["appVersion"],
                            "clientId": __save_info['info']["clientId"],
                            "equipmentApiVersion": __save_info['info']["equipmentApiVersion"],
                            "equipmentAppVersion": __save_info['info']["equipmentAppVersion"],
                            "equipmentModel": __save_info['info']["equipmentModel"],
                            "userName": __save_info['info']["userName"],
                            "userPwd": __save_info['info']["userPwd"],
                        })
                        auto_login = True
                else:
                    auto_login = False
        except FileNotFoundError:
            # 无存档
            pass

        # 手动登陆
        if not auto_login:
            login_info = {}
            login_info['userName'] = console.input('请输入你的职教云账号\n在此输入：')
            login_info['userPwd'] = console.input('\n请输入你的职教云密码\n[red]注意：密码不会显示出来[/red]\n在此输入：', password=True)
            # 高级登陆
            console.print('\n是否需要更加详细的高级登陆项？此项可以指定你想要模拟登陆的手机型号等\n默认已自动生成无需手动，不影响账号登陆及后续操作')
            if console.input('\n默认为不启动，输入任意字符来配置高级启动项\n在此输入或回车跳过：'):
                # CLIENTID
                __user_client_id = console.input(f'输入CLIENT ID，可以视为你设备的唯一身份证号\n留空或不满足32位值将会重新生成\n在此输入：')
                if __user_client_id and len(__user_client_id) == 32:
                    __client_id = __user_client_id
                else:
                    __client_id = me.gen_client_id()
                    console.print(f'CLIENT ID 已重新生成为 [yellow]{__client_id}[/yellow]')
                login_info['clientId'] = __client_id

                # MODEL
                __user_device_model = console.input(
                    f'\n输入手机型号\n当前默认设置为[green]{login_info["equipmentModel"]}[/green]\n留空会保持默认\n在此输入：')
                if __user_device_model:
                    login_info['equipmentModel'] = __user_device_model

                # OS 
                __user_device_os = console.input(
                    f'\n输入手机系统版本\n当前默认设置为[green]{login_info["equipmentApiVersion"]}[/green]\n留空会保持默认\n在此输入：')
                if __user_device_os:
                    login_info['equipmentApiVersion'] = __user_device_os

            me.login_setting(login_info)


            # CLIENT ID
            me.gen_client_id()


            # 详细登陆表单展示
            console.print('完整登陆选项如下：')
            login_info_table = Table(show_header=True, header_style="bold magenta")
            login_info_table.add_column("登陆项", justify='center')
            login_info_table.add_column("当前值", justify='center')
            login_info_table.add_column("对应setting文件中选项（弃用）", justify="center")
            login_info_table.add_column("说明", justify="center")
            login_info_table.add_row(
                "userName",
                me.login_info['userName'],
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
                me.login_info['appVersion'],
                "ios_version和ios_build或android_version",
                "用于指定职教云APP版本[red][/red]",
            )
            login_info_table.add_row(
                "equipmentAppVersion",
                me.login_info['equipmentAppVersion'],
                "ios_version和ios_build或android_version",
                "用于指定职教云APP版[red][/red]",
            )
            login_info_table.add_row(
                "equipmentApiVersion",
                me.login_info['equipmentApiVersion'],
                "os_version",
                "用于指定你想要模拟登陆的设备系统版本，如14.8",
            )
            login_info_table.add_row(
                "equipmentModel",
                me.login_info['equipmentModel'],
                "model_name",
                "模拟登陆的设备名称，如iPhone 11，[red]不影响登陆[/red]",
            )
            login_info_table.add_row(
                "clientId",
                me.login_info['clientId'],
                "clientId",
                "模拟登陆的设备UUID，[red]不影响登陆[/red]",
            )

            console.print(login_info_table)
            # 详细登陆表单展示
            if console.input('确认没有问题后回车开始登陆，[red]输入任意值并按回车重新输入[/red]\n在此输入或回车开始登录：'):
                continue

        # 开始登陆
        me.login()

        try:
            __my_name = me.name
            if isinstance(__my_name, str):
                console.print(f'已登录->{me.name}（{me.number}）', style='green')
            else:
                console.input('登录失败！请查阅logs目录下日志\n按回车键重试')
                continue
        except requests.exceptions.HTTPError:
            console.print('\n[red]无网络链接或无法链接至职教云服务器，请检查网络或稍后再试[/red]')
            console.input('[red]->[/red]按回车键重试')
            auto_login = False
            continue

        course = me.my_courses()
        while True:
            # 课程主循环

            console.print('正在拉取你的所有课程')
            course_list = course.all_courses
            # 展示所有课程
            course_table = Table(show_header=True, header_style="bold magenta")
            course_table.add_column("序号", justify='center', style='green')
            course_table.add_column("课程ID", justify='center', style='red')
            course_table.add_column("课程名", justify='center')
            course_table.add_column("你当前所处班级ID", justify="center", style='red')
            course_table.add_column("教师及其编号", justify="center")
            course_table.add_column("进度(可能不准确)", justify="center")
            course_table.add_column("得分(可能不准确)", justify="center")
            course_table.add_column("邀请码", justify="center")

            for c in course_list:
                course_table.add_row(
                    str(course_list.index(c) + 1),
                    c['courseOpenId'],
                    c['courseName'],
                    c['openClassId'],
                    f'{c["mainTeacherName"]}({c["mainTeacherNum"]})',
                    str(c['process']),
                    str(c['totalScore']),
                    c['InviteCode']
                )
            console.print(course_table)
            console.print('->[yellow]进度与得分请以实际APP或网页为，仅供参考[/yellow]\n')


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
                # global auto_comment_info
                course_choose_list = []

                command = console.input('输入序号选择课程；若多选，序号与序号之间必须留有空格，例如：\n1 3 4代表选择序号1、3、4这三门课\n在此输入：')
                __course_choose_list = command.split(' ')
                # 序号检查

                for __choose in __course_choose_list:
                    try:
                        if int(__choose) < 1 and int(__choose) > len(course_list):
                            raise ValueError
                        else:
                            course_choose_list.append(course_list[int(__choose) - 1])
                    except ValueError:
                        logger.warning(f'用户{me.number}选课时，输入了错误的序号->{__choose}')
                        console.print(f'你输入了一个错误的序号：{__choose}', style='red')

                console.print('你选择了以下课件...')
                __course_choose_table = __save_user_table = Table(show_header=False, header_style="bold magenta")
                __course_choose_table.add_column("课程名", justify='center')
                for course_choose in course_choose_list:
                    __course_choose_table.add_row(course_choose['courseName'])

                console.print(__course_choose_table)

                comment_info = {'content':'','star':5}
                __need_commant = False
                if console.input('你需要为你选择的课程所有课件进行评论吗？\n如果需要请输入评论内容，不评论请直接按回车键\n在此输入或直接回车：'):
                    # 需要评论
                    __need_commant = True
                    comment_info['content'] = command
                    command = console.input('输入评分（星）仅整数，最大5，最小1，默认为5\n例如输入5，表示给打5星\n在此输入：')
                    if int(command) and int(command) > 0 and int(command) < 6:
                        comment_info['star'] = int(command)
                    else:
                        comment_info['star'] = 5

                    console.print(f'评论内容：{comment_info["content"]} 评论打分：{comment_info["star"]}')
                else:
                    __need_commant = False


                console.print('准备开始完成课程...')
                for course_choose in course_choose_list:
                    console.print(f'开始课程 -> {course_choose["courseName"]}\n')

                    all_cell_list = course.all_cell(course_choose['courseOpenId'], course_choose['courseName'],
                                                    course_choose['openClassId'])
                    # 展示课件
                    __cell_table = Table(show_header=True, header_style="bold magenta")
                    __cell_table.add_column("课件名", justify='center')
                    __cell_table.add_column("课程ID", justify='center', style='red')
                    __cell_table.add_column("课件类型", justify="center", style='yellow')
                    __cell_table.add_column("进度(可能不准确)", justify="center")

                    for c in all_cell_list:
                        __cell_table.add_row(
                            c['name'],
                            c['id'],
                            c['type'],
                            str(c['process'])
                        )
                    console.print(__cell_table)

                    # 重置当前课件为第一课件
                    course.change_courseware(course_choose['courseOpenId'], course_choose['openClassId'],
                                             all_cell_list[0]['id'], all_cell_list[0]['name'])

                    # 进度条

                    with Progress(
                        SpinnerColumn(),
                        TextColumn("[progress.description]{task.description}"),
                        BarColumn(),
                        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                        transient=True,
                    ) as progress:
                        p_t = Thread(target=progress_func, args=(progress, len(all_cell_list),course),daemon=True)
                        p_t.start()

                        for c in all_cell_list:
                            t = Thread(target=course.finish_cell,
                                       args=(course_choose['courseOpenId'], course_choose['openClassId'], c['id']),daemon=True)
                            t.start()
                            t.join()

                            #__need_commant = False
                            if __need_commant:
                                __all_comment_list = course.all_comment(c['id'], course_choose['courseOpenId'],
                                                                        course_choose['openClassId'])
                                for __coment in __all_comment_list:
                                    if me.id == __coment['user_id']:
                                        logger.info(f'用户{me.number}已经在课件{c["name"]}({c["id"]})评论，跳过评论')
                                        __need_commant = False
                                        break

                                if course.add_comment(c['id'],course_choose['courseOpenId'],course_choose['openClassId'],comment_info['content'],comment_info['star']):
                                    logger.info(f'用户{me.number}已经在课件{c["name"]}({c["id"]})评论，跳过评论')
                                else:
                                    logger.warning(f'为用户{me.number}在课件{c["name"]}({c["id"]})下添加评论失败')
                        # 重置任务进度
                        course.progress_clear()

                console.input('所选课程及其课件已经全部完成，按回车键返回初始界面')
                break

    except KeyboardInterrupt:
        console.print('返回登陆')
        continue
    except Exception as e:
        console.input('\n' + traceback_exc())
        logger.exception(e)
        console.input('\n[red]发生错误，报错如上。按任意键继续[/red]')
        continue
