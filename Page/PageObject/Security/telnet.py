"""
@FileName：telnet.py
@Description：
@Author：Huang Junxiong
@Time：2023/7/31 上午10:54
@Department：测试组
"""
import allure

from Common.read_element import Element
from Page.PageObject.common import Common
from Page.webpage import WebPage
from Utils.times import sleep

TELNET_PAGE = Element('Security/telnet')


class Telnet(Common):

    @allure.step("输入Telnet用户名")
    def input_telnet_username(self, username):
        """
        输入telnet用户名
        :param username: Telnet用户名
        :return:
        """
        self.input_text(TELNET_PAGE['Telnet用户名'], text=username)
        sleep()

    @allure.step("输入Telnet密码")
    def input_telnet_password(self, password):
        """
        输入telnet密码
        :param password: Telnet密码
        :return:
        """
        self.input_text(TELNET_PAGE['Telnet密码'], text=password)
        sleep()

    @allure.step("输入Telnet端口")
    def input_telnet_port(self, port):
        """
        输入telnet密码
        :param port: Telnet端口
        :return:
        """
        self.input_text(TELNET_PAGE['Telnet端口'], text=port)
        sleep()

    @allure.step("获取LAN侧Telnet开关状态")
    def get_lan_telnet_status(self):
        """
        获取LAN侧Telnet开关状态
        :return:
        """
        return self.get_element_select_status(TELNET_PAGE['LAN侧Telnet开关'])

    @allure.step("开启LAN侧Telnet")
    def open_lan_telnet(self, username=None, password=None, port=None):
        """
        开启LAN侧Telnet
        :param username: Telnet用户名
        :param password: Telnet密码
        :param port: Telnet端口
        :return:
        """
        if not self.get_lan_telnet_status():
            self.is_click(TELNET_PAGE['LAN侧Telnet开关'])
        if username:
            self.input_text(TELNET_PAGE['Telnet用户名'], text=username)
        if password:
            self.input_text(TELNET_PAGE['Telnet密码'], text=password)
        if port:
            self.input_text(TELNET_PAGE['Telnet端口'], text=port)
        self.is_click(TELNET_PAGE['确定'])
        assert self.get_popup() == "操作成功"
        sleep()

    @allure.step("关闭LAN侧Telnet")
    def close_lan_telnet(self):
        """
        开启LAN侧Telnet
        :param port: Telnet端口
        :return:
        """
        if self.get_lan_telnet_status():
            self.is_click(TELNET_PAGE['LAN侧Telnet开关'])
            self.is_click(TELNET_PAGE['确定'])
            assert self.get_popup() == "操作成功"
        sleep()
