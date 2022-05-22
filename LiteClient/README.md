# 关于Lite
现在已经基于`pyinstaller`对启动文件以及核心文件进行了一些修改（太屎了，简直折磨），并进行了打包（仅EXE，其它平台请自行打包），可以直接启动

## 注意事项
**使用此脚本很可能导致你的设备被封锁！！！**
**使用此脚本很可能导致你的设备被封锁！！！**
**使用此脚本很可能导致你的设备被封锁！！！**

目前发现在评论这块，开启自动评论极大概率会导致设备被封锁

### 被封锁有什么影响？
目前唯一发现的影响便是，脚本启用自动评论功能会直接报错（报HTML源码）

### 仅仅是针对设备吗？
并不确定

## 直接运行
打包后的EXE文件被保存在dist目录下，直接双击打开即可运行

## 源码
源码被包含在`source`目录中，启动文件为`lite_launch.py`
在启动或打包前，请务必安装以下两个三方库：
```
rich
requests
```
安装完毕后即可通过`python lite_launch.py`启动

如果需要打包，还需要安装`pyinstaller`，随后便可使用以下指令打包生成：
```shell
pyinstaller -F lite_launch.py -n ICVE-HELPER
```