"""
@FileName：status_deviceinfo_baseinfo.py
@Description：状态-设备信息-设备基本信息的页面对象
@Author：Huang Junxiong
@Time：2023/6/30 下午2:53
@Department：测试组
"""
import allure

from Common.read_element import Element
from Page.webpage import WebPage

STATUS_DEVICEINFO_BASEINFO = Element('status_deviceinfo_baseinfo')


class StatusDeviceInfoBaseInfo(WebPage):

    @allure.step("获取设备型号")
    def get_product_class(self):
        return self.element_text(STATUS_DEVICEINFO_BASEINFO['设备型号'])

    @allure.step("获取设备制造商名称")
    def get_manufacturer(self):
        return self.element_text(STATUS_DEVICEINFO_BASEINFO['设备制造商名称'])

    @allure.step("获取PON的序列号")
    def get_gpon_sn(self):
        return self.element_text(STATUS_DEVICEINFO_BASEINFO['PON的序列号'])

    @allure.step("获取软件版本")
    def get_software_version(self):
        return self.element_text(STATUS_DEVICEINFO_BASEINFO['软件版本'])

    @allure.step("获取硬件版本")
    def get_hardware_version(self):
        return self.element_text(STATUS_DEVICEINFO_BASEINFO['硬件版本'])

    @allure.step("获取MAC地址")
    def get_mac(self):
        return self.element_text(STATUS_DEVICEINFO_BASEINFO['MAC地址'])

    @allure.step("运行时间")
    def get_run_time(self):
        return self.element_text(STATUS_DEVICEINFO_BASEINFO['运行时间'])

    @allure.step("获取当前上行端口类型")
    def get_uplink_type(self):
        return self.element_text(STATUS_DEVICEINFO_BASEINFO['当前上行端口类型'])

    @allure.step("获取CPU占用率")
    def get_cpu_usage(self):
        return self.element_text(STATUS_DEVICEINFO_BASEINFO['CPU占用率'])

    @allure.step("获取内存占用率")
    def get_memory_usage(self):
        return self.element_text(STATUS_DEVICEINFO_BASEINFO['内存占用率'])

    @allure.step("获取设备信息")
    def get_device_info(self):
        return {
            '设备型号': self.get_product_class(),
            '设备制造商名称': self.get_manufacturer(),
            'PON的序列号': self.get_gpon_sn(),
            '软件版本': self.get_software_version(),
            '硬件版本': self.get_hardware_version(),
            'MAC地址': self.get_mac(),
            '当前上行端口类型': self.get_uplink_type()
        }
