# ICVE-Helper

## 版本

**0.1.0-Alpha**

## 使用说明

- 需要的Python版本：至少为Python3版本
- 需要的第三方库：
  - requests
  - rich
- 启动方式：确保`launch.py`和`core`文件夹同处一个目录下， 运行 `launch.py`

**结构：**

```
|- core	# 核心文件目录
|	|-- __init__.py		# 模块初始化文件
|	|-- core.py		# 核心功能文件
|	|-- logs		# 日志保存目录（没有会自动生成）
|	|-- ...日志文件...
|	|-- setting.ini 	# 配置文件
|-launch.py		# 启动脚本
```



### 配置文件说明

|      配置项      |           默认值           | 可选值                     |                             说明                             |
| :--------------: | :------------------------: | -------------------------- | :----------------------------------------------------------: |
|     account      |             空             | 任意                       |                    职教云账号（暂时无用）                    |
|       pswd       |             空             | 任意                       |                    职教云密码（暂时无用）                    |
|    clientid*     | 空（首次运行后会自动生成） | 任意，长度必须满足**32**位 | 相当于设备的身份证号，可以自行填入或自动生成，不影响后续操作 |
|   os_version*    |            14.8            | 任意，但最好为X.X.X的格式  |                    模拟设备登陆的系统版本                    |
|   model_name*    |         iPhone 11          | 任意                       |                       模拟设备的型号名                       |
|    show_pswd     |           false            | true或false                | 是否显示密码，默认为 不显示（false），注意：即使开启显示，也仅仅在最后登陆前询问时显示，输入密码时仍不显示密码，请注意密码的输入 |
|     cookies      |             空             | 任意                       |              登陆后获取到的cookies（暂时无用）               |
|      token       |             空             | 任意                       |               登陆后获取到的token（暂时无用）                |
|      debug       |           false            | true或false                |     是否启用DEBUG模式，默认为不启用（false）（暂时弃用）     |
|    file_save     |            true            | true或false                | 是否保存操作日志，默认为启用（true），启用后会在`core/logs`下保存每次操作的日志，建议启用 |
|   ios_version*   |           2.8.43           | 任意，但建议为X.X.X的格式  |   模拟设备系统是iOS时，登陆的职教云App服务器说携带的版本号   |
|    ios_build*    |         2021042101         | 任意                       |      模拟设备是iOS时，登陆职教云App服务器说携带的版本号      |
| android_version* |           4.5.0            | 任意，但建议为X.X.X的格式  |    模拟设备是Android时，登陆职教云App服务器说携带的版本号    |
|  comments_limit  |             1              | 仅数字，且必须大于0        |            用于控制最多获取的评论页数，见下方解释            |

**说明：**

- 所有带星号（`*`）的配置项，对操作以及后续登陆可能并不会产生影响，视自己情况而定
- 暂时无用以及暂时无用的配置项，表示在脚本运行中可能并不会运用到，因此可以直接无视，但请不要清楚掉后面的等于号（`*`）
- `comments_limit`的配置项用来控制获取到的最多评论页数，脚本一次只会截取到前**20**个评论，获取过多页数可能会导致速度过慢甚至因过于频繁请求而被职教云服务器短时间拒绝服务，如果你从未在某一课件下评论，可以将此值设为`1`，只需获取前20评论即可，从而完成后续的比对并评论操作，减少时间和网络开销



### 详细启动说明

首先请确保系统中已装有Python3版本（[下载Python3](https://www.python.org/downloads/)）

（**可选**）在安装完成Python后，可以给pip（Python包管理工具）换源，方便后续安装第三方库，可以百度`pip 换源`或使用以下推荐的指令来更换pip源为清华大学开源软件镜像站([pypi | 镜像站使用帮助 | 清华大学开源软件镜像站 | Tsinghua Open Source Mirror](https://mirrors.tuna.tsinghua.edu.cn/help/pypi/))：

```shell
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

**换源不是必须的一步**

安装必须的`requests`和`rich`库：

```shell
$ pip install requests
$ pip install rich
```

推荐以下指令，可以在不换源情况下也能加速下载全部必须第三方库：

```shell
$ pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
```

在看到`Successfully installed ...`后说明安装成功

完成安装后，便可使用以下指令启动：

```shell
python3 launch.py
```


