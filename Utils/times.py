"""
@FileName：times.py
@Description：时间工具类
@Author：Huang Junxiong
@Time：2023/6/29 上午9:42
@Department：测试组
"""
import datetime
import time
from functools import wraps


def timestamp():
    """
    获取时间戳
    @return: 时间戳
    """
    return time.time()


def dt_strftime(fmt="%Y-%m-%d %H:%M:%S"):
    """
    datetime 格式化时间，默认为 %y-%m-%d %H:%M:%S
    @param fmt: 格式
    @return:格式化时间
    """
    return datetime.datetime.now().strftime(fmt)


def sleep(seconds=1.0):
    """
    程序睡眠，默认为1s
    @param seconds: 睡眠时间
    @return:
    """
    time.sleep(seconds)


def running_time(func):
    """
    函数运行时间，用于记录检查页面元素文件合法性的时间
    @param func:
    @return:
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = timestamp()
        res = func(*args, **kwargs)
        print("页面元素检查完成！用时%.3f秒！" % (timestamp() - start))
        return res

    return wrapper


def format_allure_time(allure_time):
    """
    allure报告中的时间格式为Wed Jul 19 15:07:54 GMT+08:00 2023，将其转换成%Y-%m-%d %H:%M:%S
    :param allure_time: 需要转换的时间
    :return: 转换后的时间
    """
    datetime_obj = datetime.datetime.strptime(allure_time, "%a %b %d %H:%M:%S GMT+08:00 %Y")
    return datetime_obj.strftime("%Y-%m-%d %H:%M:%S")

