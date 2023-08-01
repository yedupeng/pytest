from time import sleep

from plugin.tool import wait_switch_frame, wait_until_clickable, webpage_move_to_end, click_hide_element
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait


def run(project_config, option_config):
    driver = webdriver.Chrome()
    driver.maximize_window()

    driver.get(project_config['web_address'])
    btn_username = driver.find_element(By.XPATH, '//*[@id="username"]')
    btn_password = driver.find_element(By.XPATH, '//*[@id="logincode"]')
    btn_username.click()
    btn_username.clear()
    btn_username.send_keys(project_config['web_username'])
    btn_password.click()
    btn_password.clear()
    btn_password.send_keys(project_config['web_password'])
    driver.find_element(By.XPATH, '//*[@id="div_login_button"]/a[1]').click()

    wait_switch_frame(driver, 'mainFrame')
    wait_until_clickable(driver, '//*[@id="main_menu"]/table/tbody/tr/td[3]').click()
    wan_select = Select(driver.find_element(By.XPATH, '//*[@id="Frm_WANCName0"]'))
    wan_list = []
    for wan_option in wan_select.options:
        if wan_option.get_attribute('value') == '-1':
            continue
        wan_item = {'text': wan_option.text}
        wan_list.append(wan_item)

    for wan_item in wan_list:
        driver.switch_to.default_content()
        wait_switch_frame(driver, 'mainFrame')
        Select(driver.find_element(By.XPATH, '//*[@id="Frm_WANCName0"]')).select_by_value('0')
        webpage_move_to_end(driver)
        if 'TR069' in wan_item['text']:
            click_hide_element(driver, '//*[@id="Btn_Delete"]')
            WebDriverWait(driver, 10).until(expected_conditions.alert_is_present()).accept()
        else:
            click_hide_element(driver, '//*[@id="Btn_Delete"]')
        sleep(5)
    driver.switch_to.default_content()
    driver.switch_to.frame('mainFrame')
    Select(driver.find_element(By.XPATH, '//*[@id="Frm_WANCName0"]')).select_by_value('-1')
    Select(driver.find_element(By.XPATH, '//*[@id="Frm_protocol"]')).select_by_value('IPv4')
    Select(driver.find_element(By.XPATH, '//*[@id="Frm_ConnMode"]')).select_by_value('ROUTE')
    Select(driver.find_element(By.XPATH, '//*[@id="Frm_mode"]')).select_by_value('DHCP')
    Select(driver.find_element(By.XPATH, '//*[@id="Frm_WBDMode"]')).select_by_value('2')
    driver.find_element(By.XPATH, '//*[@id="Frm_VLANID"]').send_keys('3002')
    driver.find_element(By.XPATH, '//*[@id="Frm_MCVlANID"]').send_keys('-1')
    webpage_move_to_end(driver)
    click_hide_element(driver, '//*[@id="Btn_Add"]')

    sleep(5)

    if not project_config['olt_auth']:
        wait_until_clickable(driver, '//*[@id="main_menu"]/table/tbody/tr/td[1]').click()
        wait_until_clickable(driver, '//*[@id="pwdreg"]').click()
        input_pon_pwd = driver.find_element(By.XPATH, '//*[@id="Frm_PonPwd"]')
        input_pon_pwd.click()
        input_pon_pwd.clear()
        input_pon_pwd.send_keys(project_config['web_pon_password'])
        wait_until_clickable(driver, '//*[@id="pwdRegBtn"]').click()
        while True:
            sleep(5)
            auth_progress = driver.find_element(By.XPATH, '//*[@id="num"]').text.replace('%', '')
            if len(auth_progress) > 1 and int(auth_progress) >= 30:
                project_config['olt_auth'] = True
                driver.refresh()
                wait_switch_frame(driver, 'mainFrame')
                break

    wait_until_clickable(driver, '//*[@id="main_menu"]/table/tbody/tr/td[2]').click()
    wait_until_clickable(driver, '//*[@id="smWanStatu"]').click()
    connect_success = 0
    max_wait_time = 300
    wait_time = 0
    while True:
        sleep(5)
        wait_time += 5
        connect_status = driver.find_element(By.XPATH, '//*[@id="WanIPV4StatusTable"]/tbody/tr[2]/td[7]').text
        if '已连接' in connect_status:
            connect_success = 1
            project_config['static_ip'] = driver.find_element(By.XPATH,
                                                              '//*[@id="WanIPV4StatusTable"]/tbody/tr[2]/td[8]').text
            project_config['static_gateway'] = driver.find_element(By.XPATH,
                                                                   '//*[@id="IPv4GWTable"]/tbody/tr[2]/td[3]').text
            project_config['static_dns_server'] = driver.find_element(By.XPATH,
                                                                      '//*[@id="IPv4GWTable"]/tbody/tr[2]/td[3]').text
            break
        if wait_time > max_wait_time:
            break
    wait_until_clickable(driver, '//*[@id="buttonLogout"]').click()
    driver.quit()
    if connect_success == 1:
        project_config['report_list'].append(['DHCP测试', '已连接', 'OK'])
        return 0
    else:
        project_config['report_list'].append(['DHCP测试', '未连接', 'NOK'])
        return 1
