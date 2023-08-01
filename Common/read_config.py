"""
@FileName：read_config.py
@Description：读取配置文件
@Author：Huang Junxiong
@Time：2023/6/29 上午10:30
@Department：测试组
"""
import configparser

from Config.conf import CM


class ReadConfig(object):

    def __init__(self):
        """
        读取配置文件
        @return:
        """
        self.config = configparser.RawConfigParser()
        self.config.read(CM.CONFIG_FILE, encoding='utf-8')

    def get(self, section, option):
        """
        获取配置文件参数值
        @param section:
        @param option:
        @return: [section]option 的值
        """
        return self.config.get(section, option)

    def set(self, section, option, value):
        """
        设置配置文件参数值
        @param section:
        @param option:
        @param value:
        @return:
        """
        self.config.set(section, option, value)
        with open(CM.CONFIG_FILE, 'w') as f:
            self.config.write(f)


CONFIG = ReadConfig()