"""
@FileName：test_web_info.py
@Description：测试demo
@Author：Huang Junxiong
@Time：2023/6/29 上午10:45
@Department：测试组
"""
import json
import os

import allure
import pytest

import sys
sys.path.append(r"/home/ydp/work/pytest")

from Common.read_config import CONFIG
from Common.read_devices import DEVICES
from Interface.Network.Wan.wan import Wan
from Page.PageObject.common import Common
from Page.PageObject.status_deviceinfo_baseinfo import StatusDeviceInfoBaseInfo
from Utils.times import dt_strftime, sleep


@allure.feature("web信息测试")
class TestWebInfo:

    # @pytest.fixture(scope='function', autouse=True)
    # def open_url(self, drivers):
    #     common = Common(drivers)
    #     common.get_url(CONFIG.get('Login', 'address'))

    @allure.title("测试用例1")
    @allure.description("web设备基本信息正确\n执行时间：%s" % dt_strftime())
    @pytest.mark.核心用例
    def test_base_info(self, drivers):
        # 进入设备基本信息页面
        common = Common(drivers)
        common.enter_status_deviceinfo_baseinfo_page()

        # 获取设备信息并校验
        status_deviceinfo_baseinfo = StatusDeviceInfoBaseInfo(drivers)
        actual_value = status_deviceinfo_baseinfo.get_device_info()
        assert actual_value == {
            '设备型号': CONFIG.get('DeviceInfo', 'product_class'),
            '设备制造商名称': CONFIG.get('DeviceInfo', 'manufacturer'),
            'PON的序列号': CONFIG.get('DeviceInfo', 'gpon_sn'),
            '软件版本': CONFIG.get('DeviceInfo', 'software_version'),
            '硬件版本': CONFIG.get('DeviceInfo', 'hardware_version'),
            'MAC地址': CONFIG.get('DeviceInfo', 'mac'),
            '当前上行端口类型': CONFIG.get('DeviceInfo', 'uplink_type')
        }

    @allure.title("测试用例2")
    @allure.description("测试用例2描述\n执行时间：%s" % dt_strftime())
    @pytest.mark.扩展用例
    def test_base_info2(self, drivers):
        # 进入设备基本信息页面
        WAN = Wan(DEVICES.get('CIOT00059680'))
        print(WAN.add_wan({
            'Enable': 1,
            'Mode': 'Route',
            'NATEnable': 1,
            'DHCPEnable': 1,
            'ServiceList': 'OTHER',
            'VLANMode': 'TAG',
            'VLANIDMark': 3002,
            'MulticastVlan': -1,
            'Priority': 0,
            'LanInterface': 'LAN4',
            'IPMode': 'IPv4',
            'ConnectionType': 'IP',
            'IdleTime': 1800,
            'MTU': 1500,
        }))
        print(WAN.get_wan_list())

    @allure.title("测试用例3")
    @allure.description("测试用例3描述\n执行时间：%s" % dt_strftime())
    @pytest.mark.核心用例
    def test_base_info3(self, drivers):
        # 进入设备基本信息页面
        assert 1 == 1
