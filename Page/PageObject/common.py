"""
@FileName：common.py
@Description：共用的元素操作对象
@Author：Huang Junxiong
@Time：2023/6/30 下午5:08
@Department：测试组
"""
import allure

from Common.read_element import Element
from Page.webpage import WebPage

COMMON = Element('common')


class Common(WebPage):

    @allure.step("进入状态-设备信息-设备基本信息页面")
    def enter_status_deviceinfo_baseinfo_page(self):
        self.is_click(COMMON['状态'])
        self.is_click(COMMON['状态-设备信息'])
        self.is_click(COMMON['状态-设备信息-设备基本信息'])

    @allure.step("进入快速配置页面")
    def enter_quickset_page(self):
        self.is_click(COMMON['快速配置'])

    @allure.step("进入安全-Telnet配置页面")
    def enter_safety_Telnet_page(self):
        self.is_click(COMMON['安全'])
        self.is_click(COMMON['安全-Telnet配置'])
    
    @allure.step("进入应用-语音接口配置-配置页面-宽带电话高级设置")
    def enter_voip_Senior_page(self):
        self.is_click(COMMON['应用'])
        self.is_click(COMMON['语音接口配置'])
        self.is_click(COMMON['宽带电话高级设置'])

    
