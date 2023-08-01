import allure
import pytest

from Utils.times import dt_strftime, sleep
@allure.feature("语音")
class Testvoice_general_1:

    @allure.title("来显号码获取方式检查")
    @allure.description("web设备基本信息正确\n执行时间：%s" % dt_strftime())
    @pytest.mark.核心用例
    def test_voice_caller_id(self, drivers):
        