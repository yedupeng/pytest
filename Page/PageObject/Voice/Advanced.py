
import allure

from Common.read_element import Element
# noinspection PyUnresolvedReferences
from Page.PageObject.common import Common
# noinspection PyUnresolvedReferences
from Page.webpage import WebPage
# noinspection PyUnresolvedReferences
from Utils.times import sleep

VOICE_ADVANCED_PAGE = Element('Voice/Advanced')

class Voice_Advanced(Common):

    @allure.step("获取CID获取方式值")
    def get_CID_value(self):
        """
        获取CID获取方式
        :return:
        """
        value = self.element_text(VOICE_ADVANCED_PAGE['CID获取方式'])
        if value == 'URL':
            return 0
        elif value == 'DisplayName':
            return 1
        elif value == 'PAI':
            return 2



