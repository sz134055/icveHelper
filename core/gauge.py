from logging import Logger
from uuid import uuid4


class GaugeBaseException(Exception):
    def __init__(self, name):
        self.name = name

    def log(self, logger: Logger):
        logger.warning(self.__str__())


class GaugeExisted(GaugeBaseException):
    def __str__(self):
        return f'已经存在一个名为{self.name}的进度'


class GaugeNotExisted(GaugeBaseException):
    def __str__(self):
        return f'不存在一个名为{self.name}的进度'


class GaugeValueError(GaugeBaseException):
    def __str__(self):
        return f'进度{self.name}进度值出错，总进度或当前进度应>=0'


class GaugeOverflow(GaugeBaseException):
    def __str__(self):
        return f'进度{self.name}不允许溢出'


class GaugeChildNotExisted(GaugeExisted):
    def __str__(self):
        return f'不存在名为{self.name}的子进度集合'


class Gauge:
    """
    用于辅助处理进度问题

    通过共用和维护一个全局Gauge对象来达到在任意地方更新和获取某一事件处理进度
    """

    def __init__(self):
        # 进度集合
        self.__gauge_list = {}
        # 子进度对象列表
        self.__childList = {}
        # 别名
        self.__name = self.__random_name()

    def __random_name(self):
        return str(uuid4()).replace('-', '')

    @property
    def name(self):
        """
        获取或修改进度对象的别名

        :return: 当前进度对象的别名
        """
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    def register(self, name: str, total: int | float, initial: int | float = 0, step: int | float = 0,
                 overflow: bool = False,
                 update: bool = False) -> None:
        """
        注册一个进度

        :param name: 进度名
        :param total: 总进度数值，即进度100%时进度的数值
        :param initial: 初始进度，默认为0
        :param step: 步进值，默认为0
        :param overflow: 是否允许进度溢出，即当前进度大于总进度，默认为不允许
        :param update: 更新模式，启用后如已存在进度，则覆盖此进度，如不存在则创建。默认不启用

        :return: 无返回

        :raise GaugeExisted: 重名错误
        :raise GaugeValueError: 进度值错误
        :raise GaugeOverflow: 进度值溢出错误
        """
        if name in self.__gauge_list and not update:
            raise GaugeExisted(name)
        elif total < 0 or initial < 0:
            raise GaugeValueError(name)
        elif not overflow and initial > total:
            # 不允许溢出
            raise GaugeOverflow(name)
        else:
            self.__gauge_list[name] = {'total': total, 'now': initial, 'step': step, 'overflow': overflow}

    def get(self, name: str) -> int | float:
        """
        获取一个进度当前的进度

        :param name: 进度名

        :return: 当前进度

        :raise GaugeNotExisted: 查无进度错误
        """
        try:
            return self.__gauge_list[name]['now']
        except KeyError:
            raise GaugeNotExisted(name)

    def update(self, name, now: int | float) -> None:
        """
        更新一个进度的当前进度

        :param name: 进度名
        :param now: 进度值

        :return: 无返回

        :raise GaugeValueError: 进度值错误
        :raise GaugeOverflow: 进度值溢出错误
        :raise GaugeNotExisted: 查无进度错误
        """
        try:
            if now < 0:
                raise GaugeValueError(name)
            elif not self.__gauge_list[name]['overflow'] and now > self.__gauge_list[name]['total']:
                raise GaugeOverflow(name)
            else:
                self.__gauge_list[name]['now'] = now
        except KeyError:
            raise GaugeNotExisted(name)

    def step(self, name: str, val: int | bool = None) -> int | float:
        """
        在当前进度基础上增加一个进度值。

        当总进度值与当前进度值差小于步进值（即不满足一次完整步进）时，会自动更新当前进度至100%值。
        但当总进度值与当前进度值为0（即不步进空间时）时，即使步进值为0也会触发溢出错误

        :param name: 进度名
        :param val: 步进值，默认为设置时的步进值

        :return: 返回步进后的当前进度值

        :raise GaugeNotExisted: 查无进度错误
        """
        try:
            if not val:
                val = self.__gauge_list[name]['step']

            # 剩余进度空间
            gauge_left = self.__gauge_list[name]['total'] - self.__gauge_list['now']

            if gauge_left <= 0:
                raise GaugeOverflow(name)
            elif val > gauge_left:
                # 直接使其到达100%
                self.update(name, self.__gauge_list[name]['total'])
            else:
                self.update(name, (self.__gauge_list[name]['now'] + val))

            return self.__gauge_list[name]['now']
        except KeyError:
            raise GaugeNotExisted(name)

    def del_gauge(self, name) -> None:
        """
        删除一个进度

        :param name: 进度名

        :return: 无返回

        :raise GaugeNotExisted: 查无进度错误
        """
        try:
            del self.__gauge_list[name]
        except KeyError:
            raise GaugeNotExisted(name)

    def clearUp(self) -> None:
        """
        清空进度列表

        :return: 无返回
        """
        self.__gauge_list.clear()

    def child_bind(self, target_addr, name: str=None) -> None:
        """
        绑定一个子进度对象

        :param target_addr: 子进度对象地址
        :param name: 子进度对象别名，如果此参数不为空则以此参数为准

        :return: 无返回
        """
        if not name:
            name = target_addr.name
        self.__childList.update({name: target_addr})

    def get_child(self, name: str) -> None:
        """
        获取子进度对象

        :param name: 子进度对象别名

        :return: 无返回

        :raise GaugeChildNotExisted: 查无子进度对象错误
        """
        try:
            return self.__childList[name]
        except KeyError:
            raise GaugeChildNotExisted(name)


class GaugeChild(Gauge):
    def __init__(self):
        super().__init__()

    def parent(self, target: Gauge, name: str = None) -> None:
        """
        绑定到父进度集合对象

        :param target: 父进度对象
        :param name: 子进度对象别名，如果此参数不为空则以此参数为准

        :return: 无返回
        """
        target.child_bind(self, name)

