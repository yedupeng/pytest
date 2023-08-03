import allure
import pytest
from Utils.logger import LOG
import sys
sys.path.append(r"/home/ydp/work/pytest")

from Utils.telnet import TELNET
from Utils.times import dt_strftime, sleep
from Page.PageObject.common import Common
from Page.PageObject.login import Login
from Common.read_element import Element
from Common.read_devices import DEVICES
from Interface.Manage.reboot import Reboot
from Page.PageObject.voip_sip_basic_form_CallGetMode import voipsipbasicformCallGetMode

COMMON = Element('common')
@allure.feature("语音")
class Testvoice_general_1:
    device = DEVICES.get('CIOT00059680')
    @allure.title("来显号码获取方式检查")
    @allure.description("web设备基本信息正确\n执行时间：%s" % dt_strftime())
    @pytest.mark.核心用例
    def test_voice_caller_id(self, drivers):
        TELNET.login(DEVICES.get('CIOT00059680'))
        self.cmd1 = "tcapi show VoIPAdvanced"
        self.cmd2 = "tcapi get VoIPAdvanced_Common Starnet_callGetMode"
        TELNET.exec_cmd(command = self.cmd1)
        TELNET.exec_cmd(command = self.cmd2)
        TELNET.close()
        common = Common(drivers)
        common.enter_voip_Senior_page()

        voip_sip_basic_form_CallGetMode = voipsipbasicformCallGetMode(drivers)
        Cid_value = voip_sip_basic_form_CallGetMode.get_cid_value()
        LOG.info("---------------------------Cid_value:{}--------------------------------".format(Cid_value))
        

    @allure.title("打接电话测试")
    @allure.description("web设备基本信息正确\n执行时间：%s" % dt_strftime())
    @pytest.mark.核心用例  
    def test_voice_call(self, drivers):
        common = Common(drivers)
        common.enter_web_wan_internet()
        common.create_voip_wan()
        common.enter_voip_Basic_page()
        common.enable_voip1()
        common.enable_voip2()
        common.use_para_voip()
        sleep(1.0)
        common.register_para_voip()
        sleep(20)
        common.enter_state_voip()
        data = common.get_table_content(COMMON["业务注册状态"], 0)
        LOG.info("\n---data1-------:{}\n".format(data))

    @allure.title("重启后打接电话测试")
    @allure.description("web设备基本信息正确\n执行时间：%s" % dt_strftime())
    @pytest.mark.核心用例  
    def test_voice_reboot_call(self, drivers):
        login = Login(drivers)
        interface_reboot = Reboot(self.device)
        interface_reboot.reboot()
        sleep(120)
        login.refresh()
        login.web_login()
        sleep(20)
        common = Common(drivers)
        common.enter_state_voip()
        data = common.get_table_content(COMMON["业务注册状态"], 0)

    


        



     
