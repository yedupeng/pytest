"""
@FileName：webpage.py
@Description：selenium基类封装
@Author：Huang Junxiong
@Time：2023/6/29 下午2:35
@Department：测试组
"""
import json

from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Config.conf import CM
from Interface.common import Common
from selenium.webdriver.common.keys import Keys
from Utils.logger import LOG
from Utils.times import sleep, timestamp
from selenium.webdriver.common.by import By
from selenium import webdriver


class WebPage(object):

    def __init__(self, driver):
        self.driver = driver
        self.timeout = 20
        self.wait = WebDriverWait(self.driver, self.timeout)

    def get_url(self, url):
        """
        打开网页
        @param url:
        @return:
        """
        self.driver.maximize_window()
        self.driver.set_page_load_timeout(60)
        try:
            self.driver.get(url)
            self.driver.implicitly_wait(10)
            LOG.info("打开网页：%s" % url)
        except TimeoutError:
            raise TimeoutError("打开%s超时，请检查网络或网址是否正确！" % url)

    @staticmethod
    def element_locator(func, locator):
        """
        元素定位器
        @param func:
        @param locator: 定位器（元素表达式），如 ('id', 'logincode')
        @return:
        """
        name, value = locator
        return func(CM.LOCATE_MODE[name], value)

    def find_element(self, locator):
        """
        寻找单个元素
        @param locator: 定位器（元素表达式），如 ('id', 'logincode')
        @return:
        """
        return WebPage.element_locator(lambda *args: self.wait.until(EC.presence_of_element_located(args)), locator)

    def get_element_select_status(self, locator):
        """
        获取元素选中状态
        :param locator: 定位器（元素表达式），如 ('id', 'logincode')
        :return: 如果已经被选中返回 True 没有则返回 False
        """
        return WebPage.element_locator(lambda *args: self.wait.until(EC.presence_of_element_located(args)), locator) \
            .is_selected()

    def find_elements(self, locator):
        """
        寻找多个相同元素
        @param locator: 定位器(元素表达式),如 ('id', 'logincode')
        @return:
        """
        return WebPage.element_locator(lambda *args: self.wait.until(EC.presence_of_all_elements_located(args)),
                                       locator)

    def wait_element(self, locator, timeout=10):
        """
        等待页面元素出现
        :param locator: 元素定位器
        :param timeout: 超时时间
        :return: 元素存在返回钙元素，不存在返回False
        """
        try:
            return WebPage.element_locator(lambda *args: WebDriverWait(self.driver, timeout)
                                           .until(EC.presence_of_element_located(args)), locator)
        except TimeoutException:
            return False

    def elements_num(self, locator):
        """
        获取相同元素的个数
        @param locator: 定位器(元素表达式),如 ('id', 'logincode')
        @return: 相同元素的个数
        """
        number = len(self.find_elements(locator))
        LOG.info("相同元素：{}".format((locator, number)))
        return number

    def input_text(self, locator, text):
        """
        输入文本，输入前先清空
        @param locator: 定位器(元素表达式),如 ('id', 'logincode')
        @param text: 输入的文本
        @return:
        """
        sleep(0.5)
        element = self.find_element(locator)
        element.send_keys(Keys.CONTROL,"a")#光标向右移方便删除
        element.send_keys(Keys.DELETE)#删除键
        element.clear()
        element.send_keys(text)
        LOG.info("输入文本：{}".format(text))

    def is_click(self, locator):
        """
        点击元素
        @param locator: 定位器(元素表达式),如 ('id', 'logincode')
        @return:
        """
        self.find_element(locator).click()
        sleep()
        LOG.info("点击元素:{}".format(locator))

    def element_text(self, locator):
        """
        获取元素文本
        @param locator: 定位器(元素表达式),如 ('id', 'logincode')
        @return: 元素文本
        """
        _text = self.find_element(locator).text
        LOG.info("获取元素文本:{}".format(_text))
        return _text

    def element_value(self, locator):
        """
        获取元素值
        @param locator: 定位器(元素表达式),如 ('id', 'logincode')
        @return: 元素值
        """
        _value = self.find_element(locator).get_attribute('value')
        LOG.info("获取元素值:{}".format(_value))
        return _value

    def get_token(self, timeout=20):
        """
        获取token
        :return: 超时时间
        :return: token值
        """
        end_time = timestamp() + timeout
        while True:
            session_storage = json.loads(self.driver.execute_script
                                         (f'return sessionStorage.getItem("persist:gateway")'))['global']
            token = json.loads(session_storage)['token']
            if token:
                Common.token = token
                LOG.info("获取登录token:{}".format(token))
                return token
            if timestamp() > end_time:
                raise TimeoutException("获取token超时，session_storage：{}".format(session_storage))
            sleep(0.5)


    @property
    def get_source(self):
        """
        获取网页源代码
        @return: 网页源代码
        """
        LOG.info("获取网页源代码")
        return self.driver.page_source

    def refresh(self):
        """
        刷新页面
        @return:
        """
        self.driver.refresh()
        self.driver.implicitly_wait(30)
        LOG.info("刷新页面")

    def click_by_xpath(self, locator):
        a = self.find_element(locator)
        self.driver.execute_script("arguments[0].click();", a)

    def get_table_content(self, locator, i):
        table = self.find_elements(locator)[0]
        res = {}
        tds = table.find_elements_by_tag_name('td')
        for i,td in enumerate(tds):
            res[i] = td

        table1 = self.find_elements(locator)[1]
        res1 = {}
        tds1 = table1.find_elements_by_tag_name('td')
        for i,td in enumerate(tds1):
            res1[i] = td
        return res,res1
