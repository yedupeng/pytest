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
from selenium.webdriver.common.by import By
from Utils.logger import LOG
from Utils.times import sleep
from Common.read_config import CONFIG
COMMON = Element('common')
from selenium.webdriver.support.ui import Select


class Common(WebPage):
    @allure.step("进入快速配置页面")
    def enter_quickset_page(self):
        self.is_click(COMMON['快速配置'])

    @allure.step("进入安全-Telnet配置页面")
    def enter_safety_Telnet_page(self):
        self.is_click(COMMON['安全'])
        self.is_click(COMMON['安全-Telnet配置'])

    @allure.step("获取页面弹窗")
    def get_popup(self, timeout=5):
        message =  self.wait_element(locator=COMMON['页面弹窗'], timeout=timeout).text
        LOG.info("页面弹窗提示：{}".format(message))
        return message
#-----------------------------------状态---------------------------------    
    def enter_state_voip(self):
        self.is_click(COMMON['状态'])
        self.is_click(COMMON['状态-设备信息'])
        self.is_click(COMMON['状态-设备信息-语音口状态'])

    @allure.step("进入状态-设备信息-设备基本信息页面")
    def enter_status_deviceinfo_baseinfo_page(self):
        self.is_click(COMMON['状态'])
        self.is_click(COMMON['状态-设备信息'])
        self.is_click(COMMON['状态-设备信息-设备基本信息'])
#-----------------------------------网络---------------------------------      
    @allure.step("进入网络-新建网络连接")
    def enter_web_wan_internet(self):
        self.is_click(COMMON["网络"])
        self.is_click(COMMON["网络-WAN接口配置"])
        self.is_click(COMMON["网络-WAN接口配置-Internet连接"])
        self.is_click(COMMON["网络-wan连接列表"])

    allure.step("进入网络-新建网络连接-创建voip连接")
    def create_voip_wan(self):
        self.is_click(COMMON["网络-新建waln"])
        self.is_click(COMMON["网络-启用"])
        self.is_click(COMMON["网络-连接模式"])
        self.is_click(COMMON["网络-连接模式-路由"])
        self.is_click(COMMON["承载服务"])
        self.is_click(COMMON["承载服务-VOIPINTERNET"])
        self.is_click(COMMON["启用VLAN"])
        self.is_click(COMMON["启用VLAN-改写"])
        self.input_text(COMMON["Vlan-ID设置"], CONFIG.get('Wlan', 'voip_vlan_id'))
        self.is_click(COMMON["创建"])

    allure.step("进入网络-新建网络连接-检查是否已经具有符合条件的wan连接")
    def check_wan(self, locator):
        self.find_elements(By.ID, "wanForm_WanList")


#--------------------------------------应用-----------------------------------
# 基本页面配置
    @allure.step("进入应用-语音接口配置-宽带电话基本设置页面")
    def enter_voice_base_page(self):
        self.is_click(COMMON['应用'])
        self.is_click(COMMON['应用-语音接口配置'])
        self.is_click(COMMON['应用-语音接口配置-宽带电话基本设置'])

    allure.step("进入网络-语音接口配置-配置编码优先级")
    def change_voip_encode_order(self, id:list):
        self.input_text(COMMON["应用-语音接口配置-宽带电话基本设置-G.711 a-law"], id[0])
        self.input_text(COMMON["应用-语音接口配置-宽带电话基本设置-G.711 u-law"], id[1])
        self.input_text(COMMON["应用-语音接口配置-宽带电话基本设置-G.729"], id[2]) 
        self.input_text(COMMON["应用-语音接口配置-宽带电话基本设置-G.722"], id[3]) 

    allure.step("配置应用-宽带电话基本设置-sip")
    def choose_SIP(self):
        self.is_click(COMMON['应用-语音接口配置-宽带电话基本设置-宽带电话协议'])
        self.is_click(COMMON['应用-语音接口配置-宽带电话基本设置-宽带电话协议-SIP'])

    allure.step("配置应用-宽带电话基本设置-imssip")
    def choose_IMSSIP(self):
        self.is_click(COMMON['应用-语音接口配置-宽带电话基本设置-宽带电话协议'])
        self.is_click(COMMON['应用-语音接口配置-宽带电话基本设置-宽带电话协议-IMSSIP'])

    allure.step("检查配置是否正确")
    def check_data(self, locator, data):
        if(data != self.find_element(locator).text):
            self.input_text(locator, data)

    allure.step("配置应用-宽带电话基本设置-注册服务器")    
    def enable_register(self, data:list):
        flag = self.find_element(COMMON['应用-语音接口配置-宽带电话基本设置-注册服务器']).is_selected()
        if(flag):
            self.check_data(COMMON["应用-语音接口配置-宽带电话基本设置-注册服务器地址"], data[0])
            self.check_data(COMMON["应用-语音接口配置-宽带电话基本设置-注册服务器端口"], data[1])
        else:
            self.is_click(COMMON['应用-语音接口配置-宽带电话基本设置-注册服务器'])
            self.input_text(COMMON["应用-语音接口配置-宽带电话基本设置-注册服务器地址"], data[0]) 
            self.input_text(COMMON["应用-语音接口配置-宽带电话基本设置-注册服务器端口"], data[1]) 

    allure.step("配置应用-宽带电话基本设置-代理服务器")    
    def enable_broker(self, data:list):
        flag = self.find_element(COMMON['应用-语音接口配置-宽带电话基本设置-代理服务器']).is_selected()
        if(flag):
            self.check_data(COMMON["应用-语音接口配置-宽带电话基本设置-代理服务器地址"], data[0])
            self.check_data(COMMON["应用-语音接口配置-宽带电话基本设置-代理服务器端口"], data[1]) 
        else:
            self.is_click(COMMON['应用-语音接口配置-宽带电话基本设置-代理服务器'])
            self.input_text(COMMON["应用-语音接口配置-宽带电话基本设置-代理服务器地址"], data[0]) 
            self.input_text(COMMON["应用-语音接口配置-宽带电话基本设置-代理服务器端口"], data[1]) 

    allure.step("配置应用-宽带电话基本设置-备用代理服务器")    
    def enable_spare(self, data:list):
        flag = self.find_element(COMMON['应用-语音接口配置-宽带电话基本设置-代理服务器']).is_selected()
        if(flag):
            self.check_data(COMMON["应用-语音接口配置-宽带电话基本设置-备用代理服务器地址"], data[0])
            self.check_data(COMMON["应用-语音接口配置-宽带电话基本设置-备用代理服务器端口"], data[1]) 
        else:
            self.is_click(COMMON['应用-语音接口配置-宽带电话基本设置-备用代理服务器'])
            self.input_text(COMMON["应用-语音接口配置-宽带电话基本设置-备用代理服务器地址"], data[0]) 
            self.input_text(COMMON["应用-语音接口配置-宽带电话基本设置-备用代理服务器端口"], data[1]) 

    @allure.step("进入应用-语音接口配置-宽带电话高级设置页面")
    def enter_voice_advanced_page(self):
        self.is_click(COMMON['应用'])
        self.is_click(COMMON['应用-语音接口配置'])
        self.is_click(COMMON['应用-语音接口配置-宽带电话高级设置'])

    @allure.step("进入应用-语音接口配置-宽带电话数图设置页面")
    def enter_voice_graph_page(self):
        self.is_click(COMMON['应用'])
        self.is_click(COMMON['应用-语音接口配置'])
        self.is_click(COMMON['应用-语音接口配置-宽带电话数图设置'])

    @allure.step("进入应用-语音接口配置-配置页面-宽带电话高级设置")
    def enter_voip_Senior_page(self):
        self.is_click(COMMON['应用'])
        self.is_click(COMMON['语音接口配置'])
        self.is_click(COMMON['宽带电话高级设置'])
    
    @allure.step("进入应用-语音接口配置-配置页面-宽带电话基础设置")
    def enter_voip_Basic_page(self):
        self.is_click(COMMON['应用'])
        self.is_click(COMMON['语音接口配置'])
        self.is_click(COMMON['应用-语音接口配置-宽带电话基本设置'])

    allure.step("进入应用-语音接口配置-配置页面-启用语音1")
    def enable_voip1(self):
        flag = self.find_element(COMMON['应用-语音接口配置-宽带电话基本设置-启用1']).is_selected()
        if(~flag):
            LOG.info("\n---flag-------:{}\n".format(flag))
        else:
            self.is_click(COMMON["应用-语音接口配置-宽带电话基本设置-启用1"])
            
    allure.step("进入应用-语音接口配置-配置页面-启用语音2")
    def enable_voip2(self):
        flag = self.find_element(COMMON['应用-语音接口配置-宽带电话基本设置-启用2']).is_selected()
        if(flag):
            LOG.info("\n---flag-------:{}\n".format(flag))
        else:
            self.is_click(COMMON["应用-语音接口配置-宽带电话基本设置-启用2"])
    
    allure.step("进入应用-语音接口配置-配置页面-应用配置")
    def use_para_voip(self):
        self.is_click(COMMON["应用-语音接口配置-宽带电话基本设置-应用"])
    
    allure.step("进入应用-语音接口配置-配置页面-注册配置")
    def register_para_voip(self):
        self.is_click(COMMON["应用-语音接口配置-宽带电话基本设置-注册"])

# 高级设置
    allure.step("进入应用-语音接口配置-宽带电话高级设置-语音编码优先级控制")
    def select_local_first(self):
        self.is_click(COMMON['应用-语音接口配置-宽带电话高级设置-语音编码优先级控制'])  
        self.is_click(COMMON['应用-语音接口配置-宽带电话高级设置-语音编码优先级控制-本地优先'])
        self.is_click(COMMON['应用-语音接口配置-宽带电话高级设置-确定'])

    allure.step("进入应用-语音接口配置-宽带电话高级设置-语音编码优先级控制")
    def select_distal_first(self):
        self.is_click(COMMON['应用-语音接口配置-宽带电话高级设置-语音编码优先级控制'])  
        self.is_click(COMMON['应用-语音接口配置-宽带电话高级设置-语音编码优先级控制-远端优先'])
        self.is_click(COMMON['应用-语音接口配置-宽带电话高级设置-确定'])
    
    allure.step("进入应用-语音接口配置-配置页面-宽带电话高级设置-配置DTMF显示")
    def choose_DTMF(self):
        self.is_click(COMMON["应用-语音接口配置-宽带电话高级设置-来电显示模式"])
        self.is_click(COMMON["应用-语音接口配置-宽带电话高级设置-来电显示模式-DTMF"])
        self.is_click(COMMON['应用-语音接口配置-宽带电话高级设置-确定'])


    




