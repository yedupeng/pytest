import allure

from Common.read_element import Element
from Page.webpage import WebPage

Voip_sip_basic_form_CallGetMode = Element('voip_sip_basic_form_CallGetMode')

class voipsipbasicformCallGetMode(WebPage):
    @allure.step("获取CID获取方式")
    def get_cid_value(self):
        return self.element_text(Voip_sip_basic_form_CallGetMode['CID获取方式'])