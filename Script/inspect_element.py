"""
@FileName：inspect_element.py
@Description：检查所有元素yaml文件正确性
@Author：Huang Junxiong
@Time：2023/6/29 下午1:58
@Department：测试组
"""
import os
import yaml

from Config.conf import CM
from Utils.times import running_time


@running_time
def inspect_element():
    """
    检测所有元素是否正确
    只能做一些简单的语法检查
    @return:
    """
    for files in os.listdir(CM.ELEMENT_PATH):  # 循环校验每个元素文件
        _path = os.path.join(CM.ELEMENT_PATH, files)
        with open(_path, encoding='utf-8') as f:
            data = yaml.safe_load(f)
        for k in data.values():  # 循环校验每个item的值，k即为每个item的值
            try:
                pattern, value = k.split('==')
            except ValueError:
                raise Exception('%s 中【%s】元素表达式中没有’==’' % (_path, k))  # 元素表达式中不包含=号，不符合格式
            if pattern not in CM.LOCATE_MODE:
                raise Exception('%s 中元素【%s】无法识别指定类型' % (_path, k))  # 元素表达式中的定位类型不在记录的类型里面
            elif pattern == 'xpath':
                assert '//' in value, '%s 中元素【%s】xpath类型与值不匹配' % (_path, k)  # xpath定位类型的路径中开头必须包含//
            elif pattern == 'css':
                assert '//' not in value, '%s 中元素【%s】css类型与值不匹配' % (_path, k)  # css定位类型的路径中不包含//
            else:
                assert value, '%s 中元素【%s】类型与值不匹配' % (_path, k)  # 未获取到value值


if __name__ == '__main__':
    inspect_element()