"""
@FileName：login.py
@Description： 登录页的页面对象
@Author：Huang Junxiong
@Time：2023/6/29 下午3:15
@Department：测试组
"""

import allure
import stopit as stopit
from selenium.common import TimeoutException

from Common.read_config import CONFIG
from Common.read_element import Element
from Page.PageObject.common import Common
from Page.webpage import WebPage
from Utils.logger import LOG
from Utils.times import sleep

LOGIN_PAGE = Element('login')


class Login(Common):

    @allure.step("输入用户名")
    def input_username(self, username):
        """
        输入用户名
        :param username: 用户名
        :return:
        """
        self.input_text(LOGIN_PAGE['用户名输入框'], text=username)
        sleep()

    @allure.step("输入密码")
    def input_password(self, password):
        """
        输入密码
        :param password: 密码
        :return:
        """
        self.input_text(LOGIN_PAGE['密码输入框'], text=password)
        sleep()

    @allure.step("点击登录")
    def click_login(self):
        """
        点击登录按钮
        :return:
        """
        self.is_click(LOGIN_PAGE['登录按钮'])

    @allure.step("点击设备注册")
    def click_register(self):
        """
        点击设备注册按钮
        :return:
        """
        self.is_click(LOGIN_PAGE['设备注册按钮'])

    @allure.step("web登录")
    def web_login(self):
        """
        如果在登录界面，则web登录，并返回token，否则回到快速配置页面
        :return:
        """
        try:
            if self.elements_num(LOGIN_PAGE['用户名输入框']):
                self.input_username(CONFIG.get('Login', 'name'))
                self.input_password(CONFIG.get('Login', 'password'))
                self.click_login()
                return self.get_token()
        except TimeoutException:
            self.enter_quickset_page()

    @allure.step("web退出")
    def web_loginout(self):
        """
        web退出
        :return:
        """
        self.is_click(LOGIN_PAGE['退出登录按钮'])