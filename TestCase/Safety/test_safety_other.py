"""
@FileName：test_safety_other.py
@Description：安全功能-其他 相关用例集
@Author：Huang Junxiong
@Time：2023/7/28 上午9:16
@Department：测试组
"""
import allure
import pytest

from Common.read_devices import DEVICES
from Interface.Manage.reboot import Reboot
from Page.PageObject.Safety.telnet import Telnet
from Page.PageObject.common import Common
from Page.PageObject.login import Login
from Utils.telnet import TELNET
from Utils.times import dt_strftime, sleep


@allure.feature("安全功能-其他用例集")
class TestSafetyOther:
    device = DEVICES.get('CIOT00059680')

    @pytest.fixture(scope='function', autouse=True)
    def case_init(self, drivers):
        login = Login(drivers)
        login.web_login()

    @allure.title("端口安全-页面开关Lan侧Telnet")
    @allure.description("网页开关LAN侧，检查开启，关闭状态，重启验证\n执行时间：%s" % dt_strftime())
    # @pytest.mark.usefixtures('case_init')
    @pytest.mark.核心用例
    def test_lan_telnet_switch_by_page(self, drivers):
        telnet_page = Telnet(drivers)
        interface_reboot = Reboot(self.device)
        login = Login(drivers)

        # 进入安全-Telnet页面
        telnet_page.enter_safety_Telnet_page()
        # 关闭Telnet开关
        telnet_page.close_lan_telnet()
        # 页面校验telnet开关为关闭状态
        assert telnet_page.get_lan_telnet_status() == False
        # 校验telnet登录失败
        assert TELNET.login(self.device) == False

        # 通过接口重启设备
        interface_reboot.reboot()
        sleep(90)

        # 重启后校验telnet为关闭状态
        login.refresh()
        login.web_login()
        # 进入安全-Telnet页面
        telnet_page.enter_safety_Telnet_page()
        # 校验Telnet为关闭及状态
        assert telnet_page.get_lan_telnet_status() == False
        assert TELNET.login(self.device) == False

        # 打开telnet
        telnet_page.open_lan_telnet()
        # 页面校验telnet开关为开启状态
        assert telnet_page.get_lan_telnet_status() == True
        # 校验telnet登录成功
        assert TELNET.login(self.device) == True

        # 通过接口重启设备
        interface_reboot.reboot()
        sleep(90)

        # 重启后校验telnet为开启状态
        login.refresh()
        login.web_login()
        # 进入安全-Telnet页面
        telnet_page.enter_safety_Telnet_page()
        # 校验Telnet为开启状态
        assert telnet_page.get_lan_telnet_status() == True
        assert TELNET.login(self.device) == True
