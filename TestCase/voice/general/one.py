import allure
import pytest
from Utils.logger import LOG
import sys
sys.path.append(r"/home/ydp/work/pytest")

from Utils.telnet import TELNET
from Utils.capture import Capture
from Utils.times import dt_strftime, sleep
from Page.PageObject.common import Common
from Page.PageObject.login import Login
from Common.read_element import Element
from Common.read_devices import DEVICES
from Interface.Manage.reboot import Reboot
from Page.PageObject.voip_sip_basic_form_CallGetMode import voipsipbasicformCallGetMode
from Interface.Network.Wan.wan import Wan

COMMON = Element('common')
@allure.feature("语音")
class Testvoice_general_1:
    device = DEVICES.get('CIOT00059680')
    # @allure.title("来显号码获取方式检查")
    # @allure.description("web设备基本信息正确\n执行时间：%s" % dt_strftime())
    # @pytest.mark.核心用例
    # def test_voice_caller_id(self, drivers):
    #     TELNET.login(DEVICES.get('CIOT00059680'))
    #     self.cmd1 = "tcapi show VoIPAdvanced"
    #     self.cmd2 = "tcapi get VoIPAdvanced_Common Starnet_callGetMode"
    #     TELNET.exec_cmd(command = self.cmd1)
    #     TELNET.exec_cmd(command = self.cmd2)
    #     TELNET.close()
    #     common = Common(drivers)
    #     common.enter_voip_Senior_page()

    #     voip_sip_basic_form_CallGetMode = voipsipbasicformCallGetMode(drivers)
    #     Cid_value = voip_sip_basic_form_CallGetMode.get_cid_value()
    #     LOG.info("---------------------------Cid_value:{}--------------------------------".format(Cid_value))

    # @allure.title("打接电话测试")
    # @allure.description("web设备基本信息正确\n执行时间：%s" % dt_strftime())
    # @pytest.mark.核心用例  
    # def test_voice_call(self, drivers):
    #     data1 = ["star-net.cn", 5060]
    #     data2 = ["192.168.76.111", 5065]
    #     common = Common(drivers)
    #     common.enter_web_wan_internet()
    #     common.create_voip_wan()
    #     common.enter_voip_Senior_page()
    #     common.choose_DTMF()
    #     common.enter_voip_Basic_page()
    #     common.choose_SIP()
    #     common.enable_register(data1)
    #     common.enable_broker(data2)
    #     common.enable_voip1()
    #     common.enable_voip2()
    #     common.use_para_voip()
    #     sleep(1.0)
    #     common.register_para_voip()
    #     sleep(20)
    #     common.enter_state_voip()
    #     data = common.get_table_content(COMMON["业务注册状态"], 0)
    #     LOG.info("\n---data1-------:{}\n".format(data))

    # @allure.title("重启后打接电话测试")
    # @allure.description("web设备基本信息正确\n执行时间：%s" % dt_strftime())
    # @pytest.mark.核心用例  
    # def test_voice_reboot_call(self, drivers):
    #     login = Login(drivers)
    #     interface_reboot = Reboot(self.device)
    #     interface_reboot.reboot()
    #     sleep(120)
    #     login.refresh()
    #     login.web_login()
    #     sleep(20)
    #     common = Common(drivers)
    #     common.enter_state_voip()
    #     data = common.get_table_content(COMMON["业务注册状态"], 0)

    # @allure.title("sip 语音编码检查(主叫优先)")
    # @allure.description("web设备基本信息正确\n执行时间：%s" % dt_strftime())
    # @pytest.mark.核心用例  
    # def test_sip_caller_test_local_first(self, drivers):
    #     common = Common(drivers)
    #     common.enter_voip_Senior_page()
    #     common.select_local_first()
    #     common.enter_voip_Basic_page()
    #     id = [2, 1, 3, 4]
    #     common.change_voip_encode_order(id)
    #     common.use_para_voip()
    #     sleep(1.0)
    #     common.register_para_voip()
    #     CAPTURE = Capture()
    #     CAPTURE.start("主叫本机优先报文1")

    #     sleep(1)
    #     CAPTURE.stop()
    #     id = [3, 2, 1, 4]
    #     common.change_voip_encode_order(id)
    #     common.use_para_voip()
    #     sleep(1.0)
    #     common.register_para_voip()
    #     CAPTURE.start("主叫本机优先报文2")
    #     sleep(1)
    #     CAPTURE.stop() 

    # @allure.title("sip 语音编码检查(被叫优先)")
    # @allure.description("web设备基本信息正确\n执行时间：%s" % dt_strftime())
    # @pytest.mark.核心用例  
    # def test_sip_caller_test_distal_first(self, drivers):
    #     common = Common(drivers)
    #     common.enter_voip_Senior_page()
    #     common.select_distal_first()
    #     common.enter_voip_Basic_page()
    #     id = [2, 1, 3, 4]
    #     common.change_voip_encode_order(id)
    #     common.use_para_voip()
    #     sleep(1.0)
    #     common.register_para_voip()
    #     CAPTURE = Capture()
    #     CAPTURE.start("被叫优先报文1")

    #     sleep(1)
    #     CAPTURE.stop()
    #     id = [3, 2, 1, 4]
    #     common.change_voip_encode_order(id)
    #     common.use_para_voip()
    #     sleep(1.0)
    #     common.register_para_voip()
    #     CAPTURE.start("被叫优先报文2")
    #     sleep(1)
    #     CAPTURE.stop() 

    @allure.title("双栈语音测试（打接电话）")
    @allure.description("web设备基本信息正确\n执行时间：%s" % dt_strftime())
    @pytest.mark.核心用例  
    def test_Dual_stack(self, drivers):
        login = Login(drivers)
        common = Common(drivers)
        common.enter_web_wan_internet()
        common.check_wan(COMMON["网络-wan连接列表"])
        login.web_loginout()





    


        



     
