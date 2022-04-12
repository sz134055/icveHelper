# ICVE-HELPER
## 如果有任何地方侵犯了您的权益，请在issue留言，我会及时处理、删除。
## INTRO
此仓库代码仅由本人出于学习研究所写，发布目的为学习交流，其中包含的第三方API等均为通过网络调试工具获取到的公共开放API，本人没有通过任何反编译等破解手段获取。
同时关于登陆处的加密代码来自互联网上他人公开的代码片段。
禁止任何人用于商业用途，后果自负。

代码都为大一至大二期间自学、研究学习所积累而成，因此代码可能会有很多繁琐复杂的"屎山"，以及幼稚的写法等，请见谅。

由于目前学业繁重，加上我这个野路子，是时候学习和转成"正规军"了（跑去学基础理论加C和单片机玩去了），所以现在这个仓库基本处于缓慢更新甚至停更的状态，如果有想法自行编写、维护吧。
其实ICVE这个APP并不难，非常适合作为新手练习对象（毕竟我就是这么学过来的） ~~但可不要把自己学进去了，违法的事咱别干~~

## 涵盖的功能
目前涵盖了登陆、退出等功能，以及课堂、课程、课件相关的功能。这些功能基本封装在`core`中，你可以参考lite对其调用。

**MOOC学院相关功能暂时没有更新**

## 关于文档
在`docs`目录，包含了我在学习过程中对ICVE API的研究、记录与见解，可供参考，也欢迎补充。

## 关于所谓的Lite
你懂的。

如何启动？
请自行百度如何启动python脚本。
需要的三方库为：`rich` & `requests`，你可以使用以下指令安装：
`pip install rich requests -i https://pypi.tuna.tsinghua.edu.cn/simple`
（注意你的pip指令是`pip`还是`pip3`）

**本人承若未使用该脚本以及该仓库下的所有代码进行过盈利活动**
