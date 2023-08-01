"""
@FileName：read_element.py
@Description：获取页面元素
@Author：Huang Junxiong
@Time：2023/6/29 上午11:57
@Department：测试组
"""
import os.path
import yaml

from Config.conf import CM


class Element(object):

    def __init__(self, name):
        """
        读取页面元素文件
        @param name: 页面元素文件名
        """
        self.file_name = "%s.yaml" % name
        self.element_path = os.path.join(CM.ELEMENT_PATH, self.file_name)
        if not os.path.exists(self.element_path):
            raise FileExistsError("%s 文件不存在！" % self.element_path)
        with open(self.element_path, encoding='utf-8') as f:
            self.data = yaml.safe_load(f)

    def __getitem__(self, item):
        """
        获取属性值
        @param item: 页面元素item，如 密码框
        @return: 元素对应的类型和值，如 ('id', 'logincode')
        """
        data = self.data.get(item)
        if data:
            name, value = data.split('==')
            return name, value
        raise ArithmeticError("{}中不存在关键字：{}".format(self.file_name, item))


if __name__ == "__main__":
    element = Element('login_page')
    print(element['密码框'])