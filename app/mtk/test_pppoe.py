from time import sleep

from general.tool import mtk_webpage_move_to_end, mtk_webpage_move_to_top, mtk_input_text
from general.tool import wait_until_clickable, mtk_web_login
from selenium import webdriver
from selenium.webdriver.common.by import By


def run(project_config, option_config):
    driver = webdriver.Chrome()
    driver.maximize_window()

    mtk_web_login(driver, project_config)

    driver.switch_to.default_content()
    wait_until_clickable(driver, '//*[@id="htmlBody"]/div[2]/div/div[3]/img').click()
    wait_until_clickable(driver, '//*[@id="311"]/span').click()

    mtk_webpage_move_to_end(driver)
    while '删 除' in driver.find_element(By.XPATH,
                                       '//*[@id="maincontent"]/section/main/div/div/div/div[2]/button/span').text:
        mtk_webpage_move_to_end(driver)
        wait_until_clickable(driver, '//*[@id="maincontent"]/section/main/div/div/div/div[2]/button').click()
        sleep(1)
        driver.refresh()

    mtk_webpage_move_to_top(driver)
    wait_until_clickable(driver, '//*[@id="ServiceList-col"]/div/div[2]/div').click()
    wait_until_clickable(driver, '//*[contains(@class, "ant-select-item-option-content") '
                                 'and text()="TR069_INTERNET"]').click()

    wait_until_clickable(driver, '//*[@id="VLANMode-col"]/div/div[2]/div').click()
    wait_until_clickable(driver, '//*[contains(@class, "ant-select-item-option-content") '
                                 'and text()="改写（tag）"]').click()

    sleep(1)

    mtk_input_text(driver, '//*[@id="wanForm_VLANIDMark"]', '3002')

    wait_until_clickable(driver, '//*[@id="ConnectionType-col"]/div/div[2]/div').click()
    wait_until_clickable(driver, '//*[contains(@class, "ant-select-item-option-content") '
                                 'and text()="PPPoE"]').click()

    mtk_webpage_move_to_end(driver)

    driver.find_element(By.XPATH, '//*[@id="wanForm_Username"]').send_keys(project_config['web_pppoe_username'])
    driver.find_element(By.XPATH, '//*[@id="wanForm_Password"]').send_keys(project_config['web_pppoe_password'])
    wait_until_clickable(driver, '//*[@id="ConnectionTrigger-col"]/div/div[2]/div').click()
    wait_until_clickable(driver, '//*[contains(@class, "ant-select-item-option-content") '
                                 'and text()="自动拨号"]').click()

    wait_until_clickable(driver, '//*[@id="maincontent"]/section/main/div/div/div/div[1]/button').click()

    mtk_webpage_move_to_top(driver)

    sleep(5)

    if not project_config['olt_auth']:
        wait_until_clickable(driver, '//*[@id="buttonLogout"]').click()
        wait_until_clickable(driver, '//*[@id="gotoRegister"]').click()
        sleep(5)
        driver.switch_to.default_content()
        input_pon_pwd = driver.find_element(By.XPATH, '//*[@id="pwd"]')
        input_pon_pwd.click()
        input_pon_pwd.clear()
        input_pon_pwd.send_keys(project_config['web_pon_password'])
        wait_until_clickable(driver, '//*[@id="submit"]').click()
        while True:
            sleep(5)
            auth_progress = \
                driver.find_element(By.XPATH, '//*[@id="Cmcc_Register_From"]/table/tr[2]/td').text.replace('%', '')
            if len(auth_progress) > 1 and int(auth_progress) >= 30:
                project_config['olt_auth'] = True
                mtk_web_login(driver, project_config)
                sleep(3)
                break

    connect_success = 0
    max_wait_time = 300
    wait_time = 0
    while True:
        driver.refresh()
        wait_until_clickable(driver, '//*[@id="htmlBody"]/div[2]/div/div[2]/img').click()
        wait_until_clickable(driver, '//*[@id="22"]/div/span').click()
        wait_until_clickable(driver, '//*[@id="221"]/span').click()
        sleep(5)
        wait_time += 5
        connect_status = driver.\
            find_element(By.XPATH, '//*[@id="maincontent"]/section/main/div[2]/div[1]/div[2]'
                                   '/div/div/div/div/div/table/tbody/tr/td[3]').text
        if '已连接' in connect_status:
            connect_success = 1
            break
        if wait_time > max_wait_time:
            break

    wait_until_clickable(driver, '//*[@id="buttonLogout"]').click()
    driver.quit()
    if connect_success == 1:
        project_config['report_list'].append(['PPPOE测试', '已连接', 'OK'])
        return 0
    else:
        project_config['report_list'].append(['PPPOE测试', '未连接', 'NOK'])
        return 1
