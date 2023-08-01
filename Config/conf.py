"""
@FileName：conf.py
@Description：配置信息管理
@Author：Huang Junxiong
@Time：2023/6/29 上午9:57
@Department：测试组
"""
import os.path

from selenium.webdriver.common.by import By

from Utils.times import dt_strftime


class ConfigManager(object):
    # 项目目录
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # 页面元素目录
    ELEMENT_PATH = os.path.join(BASE_DIR, 'Page', 'Element')

    # 测试脚本执行后临时保存的测试结果文件目录
    CURRENT_RESULTS_PATH = os.path.join(os.path.abspath('.'), 'temps')

    # allure生成的测试结果保存目录
    ALLURE_RESULTS_PATH = os.path.join(BASE_DIR, 'Results', 'AllureResults')

    # 测试报告结果保存目录
    REPORT_PATH = os.path.join(BASE_DIR, 'Results', 'Report')

    # 原始测试汇总报告的文件路径
    ORIGIN_XLSX_REPORT_DIR = os.path.join(REPORT_PATH, 'data', 'suites.csv')

    # 最终生成的测试汇总报告的文件路径
    FINAL_XLSX_REPORT_DIR = os.path.join(REPORT_PATH, 'report.xlsx')

    # 元素定位的类型
    LOCATE_MODE = {
        'css': By.CSS_SELECTOR,
        'xpath': By.XPATH,
        'name': By.NAME,
        'id': By.ID,
        'class': By.CLASS_NAME
    }

    # 邮件信息
    EMAIL_INFO = {
        'username': '',
        'password': '',
        'smtp_host': '',
        'smtp_port': 465
    }

    # 收件人
    ADDRESSEE = [
        'huangjunxiong@star-net.cn'
    ]

    @property
    def LOG_FILE(self):
        """
        日志文件路径
        @return:
        """
        log_dir = os.path.join(self.BASE_DIR, 'Results', 'Logs')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        return os.path.join(log_dir, '{}.log'.format(dt_strftime()))

    @property
    def CAPTURE_PATH(self):
        """
        抓包报文路径
        :return:
        """
        capture_dir = os.path.join(self.BASE_DIR, 'Results', 'Captures')
        if not os.path.exists(capture_dir):
            os.makedirs(capture_dir)
        return capture_dir

    @property
    def SERIAL_PATH(self):
        """
        抓包报文路径
        :return:
        """
        serial_dir = os.path.join(self.BASE_DIR, 'Results', 'Serials')
        if not os.path.exists(serial_dir):
            os.makedirs(serial_dir)
        return serial_dir

    @property
    def CONFIG_FILE(self):
        """
        配置文件路径
        @return:
        """
        config_file = os.path.join(self.BASE_DIR, 'Config', 'config.ini')
        if not os.path.exists(config_file):
            raise FileExistsError("配置文件%s不存在！" % config_file)
        return config_file

    @property
    def DEVICES_FILE(self):
        """
        设备配置信息文件路径
        @return:
        """
        devices_file = os.path.join(self.BASE_DIR, 'Data', 'devices.xlsx')
        if not os.path.exists(devices_file):
            raise FileExistsError("设备文件%s不存在！" % devices_file)
        return devices_file


CM = ConfigManager()

