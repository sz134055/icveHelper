from rich.console import Console
from rich.table import Table
from lite import coon, conf_update, logger
from lite import core
# from lite.update import version_check,set_console
import requests
import time
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn

version = coon.get('version', 'version')
build = coon.get('version', 'build')

console = Console()


# set_console(console)

def check_update(now_version, now_build):
    res = requests.get(url='https://hyasea.top:7002/icve/version', verify=False)
    if res.status_code == 200:
        res_json = res.json()
        if float(now_build) < float(res_json['build']):
            logger.info(f'发现新版本：{res_json["version"]}')
            console.print(
                f'[yellow]->[/yellow]新版本：[red]{res_json["version"]}[/red]\n[green]->[/green]更新说明：\n[green]{res_json["content"]}[/green]')

            console.input('\n[yellow]建议更新[/yellow]输入任意内容或回车继续')

def broadcast():
    res = requests.get(url='https://hyasea.top:7002/icve/broadcast')
    if res.status_code == 200:
        res_json = res.json()
        console.print('[广播]')
        console.print(res_json['time'])
        console.print(res_json['content'],style=res_json['style'])
# 检查更新
check_update(version, build)


def uuid_get(remake=False):
    uuid = coon.get('user', 'clientId')
    if not uuid or remake:
        console.print('正在生成clientId，请稍后...')
        res = requests.get('http://www.uuid.online/uuidbackend/generate/?num=1&uuidversion=UUID1&checkbox=true')

        uuid = res.text.replace('"', '')
        uuid = uuid.replace('[', '')
        uuid = uuid.replace(']', '')

        # 更新
        conf_update('user', 'clientId', uuid)
    return uuid


login_info = {
    'appVersion': '2.8.43',
    'clientId': uuid_get(),
    'equipmentApiVersion': coon.get('user', 'os_version'),
    'equipmentAppVersion': '2.8.43',
    'equipmentModel': coon.get('user', 'model_name'),
    'userName': '',
    'userPwd': '',
}

__the_logo = '''
    /$$$$$$  /$$$$$$  /$$    /$$ /$$$$$$$$
    |_  $$_/ /$$__  $$| $$   | $$| $$_____/
    | $$  | $$  \__/| $$   | $$| $$      
    | $$  | $$      |  $$ / $$/| $$$$$   
    | $$  | $$       \  $$ $$/ | $$__/   
    | $$  | $$    $$  \  $$$/  | $$      
    /$$$$$$|  $$$$$$/   \  $/   | $$$$$$$$
    |______/ \______/     \_/    |________/
    '''


def login_status_check(func):
    def warp(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except BaseException:
            return None

    return warp


def all_my_course(user):
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


# 主循环
while True:
    console.print(f'[right]{__the_logo}[/right]\nWELCOME ICVE！\n本程序仅学习之余制作，用于帮助学习\n如用于盈利后果自负\n', style='bold red')
    # 登陆
    console.print('版本：' + version, style='red')
    broadcast()
    login_info['userName'] = console.input('请输入你的职教云账号\n')
    login_info['userPwd'] = console.input('\n请输入你的职教云密码\n[red]注意：密码不会显示出来[/red]\n', password=True)

    if console.input('是否启用更加详细的高级登陆项？\n默认为不启动，输入任意字符来配置高级启动项\n'):
        __client_id = console.input(
            f'输入CLIENT ID，可以视为你设备的唯一身份证号\n当前为[yellow]{login_info["clientId"]}[/yellow]，留空或不满足32位值将会重新生成')
        if not __client_id or len(__client_id) < 32:
            console.print(f'CLIENT ID 已重新生成为 [yellow]{uuid_get(remake=True)}[/yellow]')
    # 提取进登陆信息
    __client_id = coon.get('user', 'clientId')
    login_info['clientId'] = __client_id
    console.print(f'CLIENT ID 已被选中为 [yellow]{__client_id}[/yellow]')

    # 是否显示密码
    the_pswd = '不显示密码'
    if coon.get('user', 'show_pswd') == 'true':
        console.print('展示密码已被开启，如若关闭请在setting文件中将 user --- show_pswd 选项设置为 false')
        the_pswd = login_info['userPwd']
    elif coon.get('user', 'show_pswd') != 'false':
        console.print('展示密码已被关闭，如若启动请在setting文件中将 user --- show_pswd 选项设置为 true')

    console.print('完整登陆选项如下：')
    login_info_table = Table(show_header=True, header_style="bold magenta")
    login_info_table.add_column("登陆项", justify='center')
    login_info_table.add_column("当前值", justify='center')
    login_info_table.add_column("对应setting文件中选项", justify="center")
    login_info_table.add_column("说明", justify="center")
    login_info_table.add_row(
        "userName",
        login_info['userName'],
        "account",
        "职教云账号"
    )
    login_info_table.add_row(
        "userPwd",
        the_pswd,
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

    console.print(login_info_table)

    if console.input('确认没有问题后回车开始登陆，[red]输入任意值重新输入[/red]'):
        continue

    # print(user_password)

    if login_info['userName'] and login_info['userPwd']:
        console.print('正在尝试登陆...', style='yellow')

    try:
        me = core.User(login_info)
    except requests.exceptions.HTTPError:
        console.print('\n[red]无网络链接或无法链接至职教云服务器，请检查网络或稍后再试[/red]')
        console.input('[red]->[/red]输入任意字符或回车继续')
        continue

    try:
        me.user_info['userId']
    except KeyError:
        console.input('登陆失败！按任意键重试')
        continue
    else:
        console.print('登陆成功！', style='green')
        course_list = all_my_course(user=me)

        course_choose = ''

        course_choose_list = []
        while True:
            def make_course_choose(choose:str):
                global course_choose_list
                if '/' in choose:
                    l,r = choose.split('/')
                    c_choose_list = course_list[int(l)-1:int(r)+1]
                    for c_choose in c_choose_list:
                        course_choose_list.append(c_choose['courseOpenId'])

                else:
                    course_num_list = choose.split(' ')
                    for c in course_num_list:
                        course_choose_list.append(course_list[int(c)-1]['coureseOpenId'])



            if not course_choose:
                course_choose = console.input(
                    '\n[red]->[/red]选择一门课程（其名称或完整的ID）以继续：\n[yellow]->[/yellow]名称可以不填写完全，例如课程 大学生创新创业，可写大学生创新\n[green]->[/green]但对于名称略有重复的课程如 大学语文与大学英语 请至少填写为 大学语或大学英\n'
                    '现在你可以使用[red]d+序号[/red]选课甚至多选（序号见上表,序号选择必须保证第一个是d），用空格分割，如：[red]d1 2 3[/red]，或者使用斜杠(/)分割来选择一个范围，如：[red]d1/3[/red]，表示选中序号[red]1，2，3[/red]这三门课程\n')
                if 'd' == course_choose[0]:
                    # 序号选择
                    course_choose = course_choose.replace('d','')
                    make_course_choose(course_choose)
                    course_choose = 'wait'      # 占位
                    continue
            elif course_choose_list:
                if course_choose == 'wait':
                    course_choose = course_choose_list[0]
                else:
                    course_choose_list.remove(course_choose)
                    course_choose = course_choose_list[0]
            else:
                if console.input(f'\n[red]->[/red]当前默认选择上次课程[yellow] {course_choose}[/yellow]，回车继续，任意字符重新选择'):
                    course_choose = ''
                    continue

            course_choose_info = {}
            if not course_choose:
                continue
            else:
                for c in course_list:
                    if course_choose in c['courseName'] or course_choose == c['courseOpenId']:
                        course_choose = c['courseName']
                        course_choose_info = c.copy()
                        break

                if not course_choose_info:
                    console.print('未能选中任何课程，请重新选择', style='red')
                    continue

            console.print(f'\n当前已选中课程[red] {course_choose} ({course_choose_info["courseOpenId"]})[/red]\n')

            command = console.input(
                '[red]->[/red]请输入对应操作的序号，输入其它非序号来重新选择课程：\n1-自动完成并评论课程下所有课件\n2-显示当前课程的课件完成信息\n3-自动完成对当前课程的所有开课评论\n')

            if command == '1':
                try:
                    star = int(coon.get('courseware','star'))
                    content = coon.get('courseware','content')

                    auto_comment = coon.get('courseware','auto_comment')
                    console.print(f'[red]->[/red]已从设置文件中读取到：打分->[red]{str(star)}分[/red]，评论->[red]{content}[/red]\n[red]->[/red]自动评论设置：[red]{auto_comment}[/red]（设置auto_comment为true将不再询问自动评论，为false时取消自动评论）')
                    if auto_comment == 'true':
                        console.print('[red]自动评论已启动[/red]（设置auto_comment为true将不再询问自动评论，为false时取消自动评论）')
                    else:
                        if console.input('\n确认评论设置无误请直接回车，输入任意字符重新设置（仅对当前选中课程有效）'):
                            raise ValueError
                except ValueError:
                        star = int(console.input('\n批量课件打分（1-5分）：'))
                        content = console.input('批量评论内容：')

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
                    my_course.change_corseware(course_id=course_choose_info['courseOpenId'],
                                               class_id=course_choose_info['openClassId'], cell_id=cell_list[0]['id'],
                                               cell_name=cell_list[0]['name'])

                    # 总进度
                    task_total = progress.add_task('[yellow]总进度', total=len(cell_list))
                    task_cell = progress.add_task('当前课程', total=1)
                    my_course.set_progress_task(task_cell)
                    task_comment = progress.add_task('[red]当前课程评论', total=3)
                    for cell in cell_list:
                        # 单课进度
                        # task_cell = progress.add_task(f'[red]{cell["name"]}',total=10)

                        # progress.update(task_cell,completed=0,description=f'[yellow]{cell["name"]}[视频]',refresh=True)
                        if cell['process'] != 100:
                            my_course.finish_cell(course_id=course_choose_info['courseOpenId'],
                                                  class_id=course_choose_info['openClassId'], cell_id=cell['id'])
                            time.sleep(2)
                        else:
                            progress.update(task_cell, completed=1, description=f'[green]{cell["name"]}(跳过课件)',
                                            refresh=True)
                        # progress.update(task_cell,completed=8,description=f'[rgb(0,128,128)]{cell["name"]}[对比评论]',refresh=True)
                        progress.update(task_comment, completed=0, description=f'[rgb(0,128,128)]{cell["name"]}[获取评论]',
                                        refresh=True)
                        comment_info = my_course.all_comment(cell['id'], course_choose_info['courseOpenId'],
                                                             course_choose_info['openClassId'], 1)
                        progress.update(task_comment, completed=1, description=f'[rgb(0,128,128)]{cell["name"]}[对比评论]',
                                        refresh=True)
                        is_comment = False
                        for comment in comment_info:
                            if me.id == comment['user_id']:
                                # console.print('已经评论过此课件，跳过')
                                is_comment = True
                                # progress.update(task_cell,completed=9,description=f'[rgb(0,128,128)]{cell["name"]}[跳过评论]',refresh=True)
                                progress.update(task_comment, completed=2,
                                                description=f'[rgb(0,128,128)]{cell["name"]}[跳过评论]', refresh=True)

                                break

                        if not is_comment:
                            my_course.add_comment(cell['id'], course_choose_info['courseOpenId'],
                                                  course_choose_info['openClassId'], content, star)
                            progress.update(task_comment, completed=2,
                                            description=f'[rgb(0,128,128)]{cell["name"]}[添加评论]', refresh=True)

                        progress.update(task_comment, completed=3, description=f'[rgb(0,128,128)]{cell["name"]}[完成评论]',
                                        refresh=True)

                        # progress.update(task_cell,completed=9,description=f'[rgb(0,128,128)]{cell["name"]}[添加评论]',refresh=True)
                        # console.print(f'已为课件 {cell["id"]} 添加评论：{content} ({star}星)')
                        # progress.update(task_cell,completed=10,description=f'[green]{cell["name"]}[完成]',refresh=True)
                        progress.update(task_total, advance=1, refresh=True)
                        time.sleep(2)

            elif command == '2':
                cell_list = all_cell(me, course_choose_info['courseOpenId'], course_choose_info['openClassId'])
                console.input('[red]->[/red]输入任意字符或回车继续')
            else:
                console.print('重新选择课程')
                continue
