"""
@FileName：conftest.py
@Description： 胶水文件，每次用例执行都会执行的共用方法
@Author：Huang Junxiong
@Time：2023/6/29 下午3:53
@Department：测试组
"""
import atexit
import csv
import datetime
import os.path
import allure
import pandas as pd
import pytest
from selenium import webdriver

from Common.read_config import CONFIG
from Config.conf import CM
from Page.PageObject.login import Login
from Utils.Serial import serial_list, Serial, SERIAL
from Utils.logger import LOG
from Utils.times import sleep, format_allure_time

driver = None


@pytest.fixture(scope='function', autouse=True)
def case(request):
    """
    每个测试用例执行前后的操作，fn()为用例执行结束后的操作
    @param request:获取用例信息的request
    @return:
    """
    case_name = request.keywords.node.nodeid
    LOG.info("---------------用例执行：{}---------------".format(case_name))
    case_name = case_name.split("::")[-1]
    SERIAL.start(case_name)

    def fn():
        SERIAL.stop()
        LOG.info("---------------用例结束：{}---------------".format(request.keywords.node.nodeid))

    request.addfinalizer(fn)


@pytest.fixture(scope='session', autouse=True)
def all_init():
    """
    初始化函数，在所有用例执行前执行
    @return:
    """
    LOG.info("测试环境初始化，删除{}".format(CM.ALLURE_RESULTS_PATH))
    os.system('rm -rf %s' % CM.ALLURE_RESULTS_PATH)
    LOG.info("测试环境初始化，删除{}".format(CM.REPORT_PATH))
    os.system('rm -rf %s' % CM.REPORT_PATH)


@pytest.fixture(scope='session', autouse=True)
def drivers(request):
    """
    driver的初始化及退出
    @param request:
    @return:
    """
    global driver
    if driver is None:
        driver = webdriver.Chrome()
        driver.maximize_window()
    login = Login(driver)
    login.get_url(CONFIG.get('Login', 'address'))
    login.web_login()

    def fn():
        driver.quit()

    request.addfinalizer(fn)
    return driver


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    获取每个用例状态的钩子函数
    @param item: 测试用例
    @param call: 测试步骤
    @return:
    """
    out_come = yield
    rep = out_come.get_result()  # 从钩子方法的调用结果中获取测试报告
    # rep.when表示测试步骤，仅仅获取用例call 执行结果是失败的情况, 不包含 setup/teardown
    if rep.when == 'call' and rep.failed:
        mode = "a" if os.path.exists("failures") else "w"
        with open("failures", mode) as f:
            if "tmpdir" in item.fixturenames:
                extra = "（%s）" % item.funcargs["tmpdir"]
            else:
                extra = ""
            f.write((rep.nodeid + extra + "\n"))
        if hasattr(driver, "get_screenshot_as_png"):  # 添加allure报告截图
            with allure.step("用例执行失败，添加失败截图。。。"):
                LOG.error("用例执行失败，捕获当前页面...")
                allure.attach(driver.get_screenshot_as_png(), "失败截图", allure.attachment_type.PNG)


@atexit.register
def general_report():
    """
    生成测试结果、测试报告、测试汇总报告
    @return:
    """
    os.system('mv %s %s && allure generate %s -o %s --clean' %
              (CM.CURRENT_RESULTS_PATH, CM.ALLURE_RESULTS_PATH, CM.ALLURE_RESULTS_PATH, CM.REPORT_PATH))
    try:
        while not os.path.exists(CM.ORIGIN_XLSX_REPORT_DIR):
            # LOG.info("测试报告生成中，请稍等")
            sleep()
        # LOG.info("测试报告生成成功，测试报告存放地址：{}".format(CM.REPORT_PATH))
        generate_xlsx_report()
    except Exception:
        pass


def generate_xlsx_report():
    """
    生成测试汇总报告
    :return:
    """
    columns_dict = {
        "Suite": "测试文件",
        "Sub Suite": "测试类",
        "Name": "测试用例",
        "Status": "用例结果",
        "Test Class": "测试结果",
        "Start Time": "开始时间",
        "Stop Time": "结束时间",
        "Duration in ms": "耗时"
    }

    dataset = pd.read_csv(CM.ORIGIN_XLSX_REPORT_DIR)
    df = pd.DataFrame(dataset, columns=columns_dict.keys())
    df.rename(columns=columns_dict, inplace=True)
    for index, row in df.iterrows():
        df.loc[index, '开始时间'] = format_allure_time(row['开始时间'])
        df.loc[index, '结束时间'] = format_allure_time(row['结束时间'])
        df.loc[index, '耗时'] = str(row['耗时']) + ' ms'
        if row['用例结果'] == 'failed':
            df.loc[index, '测试结果'] = 'NOK'
        elif row['用例结果'] == 'passed':
            df.loc[index, '测试结果'] = 'OK'
        else:
            df.loc[index, '测试结果'] = '异常'
    df['测试文件'] = df['测试文件'] + '.py'
    df.to_excel(CM.FINAL_XLSX_REPORT_DIR, index=False, encoding="utf-8")
    while not os.path.exists(CM.FINAL_XLSX_REPORT_DIR):
        # LOG.info("测试汇总报告生成中，请稍等")
        sleep()
    # LOG.info("测试汇总报告生成成功，测试汇总报告文件路径：{}".format(CM.FINAL_XLSX_REPORT_DIR))
