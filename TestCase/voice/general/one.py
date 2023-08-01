import allure
import pytest


from Utils.telnet import TELNET
from Utils.times import dt_strftime, sleep
from Page.PageObject.common import Common
from Page.PageObject.voip_sip_basic_form_CallGetMode import voipsipbasicformCallGetMode

@allure.feature("语音")
class Testvoice_general_1:

    @allure.title("来显号码获取方式检查")
    @allure.description("web设备基本信息正确\n执行时间：%s" % dt_strftime())
    @pytest.mark.核心用例

    def test_voice_caller_id(self, drivers):
        self.ip = "192.168.1.1"
        self.pwd = "ceshi@123"
        self.user = "admin"
        self.port = 23
        self.chip_type = "mtk"
        self.cmd1 = "tcapi show VoIPAdvanced"
        self.cmd2 = "tcapi get VoIPAdvanced_Common Starnet_callGetMode"

        assert TELNET.telnet_login(self.ip, self.port , self.user, self.pwd,
                                    self.chip_type)
        TELNET.exec_cmd(self.cmd1)
        TELNET.exec_cmd(self.cmd2)
        common = Common(drivers)
        common.enter_voip_Senior_page()

        voip_sip_basic_form_CallGetMode = voipsipbasicformCallGetMode(drivers)
        Cid_value = voip_sip_basic_form_CallGetMode.get_cid_value()
        

        
