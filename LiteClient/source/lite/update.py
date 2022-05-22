import requests
from . import coon
from . import logger

s = requests.session()
s.verify = False
requests.packages.urllib3.disable_warnings()

url = 'https://hyasea.top:7002/icve/'
now_version = coon.get('version','version')
now_build = coon.get('version','build')

console = None
def set_console(con):
    global console
    console = con

def version_check():
    res = s.get(url=url+'version')
    res_json = res.json()
    if float(now_build) < float(res_json['build']):
        # 新版本
        logger.info(f'发现新版本：{res_json["version"]}')
        console.print(f'[yellow]->[/yellow]需要更新：[red]{res_json["version"]}[/red]\n[green]->[/green]更新说明：\n[green]{res_json["content"]}[/green]')

        command = console.input('\n[yellow]回车进行更新，输入任意字符退出程序[/yellow]')

        if not command:
            pass
        else:
            exit()

    else:
        # 放行
        return True

def __get_update():
    try:
        requests
    except OSError:
        logger.warning('更新失败')