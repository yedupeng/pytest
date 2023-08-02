"""
@FileName：general.py
@Description：
@Author：Ding Zhibin
@Time：2023/7/31 上午10:54
@Department：测试组
"""

import allure

from Common.read_element import Element
# noinspection PyUnresolvedReferences
from Page.PageObject.common import Common
# noinspection PyUnresolvedReferences
from Page.webpage import WebPage
# noinspection PyUnresolvedReferences
from Utils.times import sleep

VOICE_BASE_PAGE = Element('Voice/base')

class Voice_Base(Common):

    @allure.step("输入Telnet用户名")