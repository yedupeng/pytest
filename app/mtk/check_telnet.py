import time

from general.tool import wait_until_clickable, MTKTelnetOperation, InterruptSystemError
from selenium import webdriver
from selenium.webdriver.common.by import By


def web_open_telnet(project_config):
    driver = webdriver.Chrome()
    driver.maximize_window()

    driver.get(f'{project_config["web_address"]}/pagesMtkTelnet')

    time.sleep(5)
    switch_telnet = driver.find_element(By.XPATH, '//*[@id="telnetform_LanEnable"]')
    if switch_telnet.is_selected() is False:
        switch_telnet.click()
    wait_until_clickable(driver, '//*[@id="submit"]').click()
    time.sleep(2)

    driver.quit()


def check_telnet(project_config):
    telnet = MTKTelnetOperation(project_config['telnet_ip'],
                                int(project_config['telnet_port']),
                                project_config['telnet_username'],
                                project_config['telnet_password'])
    try:
        telnet.execute_command('echo hello')
    except:
        web_open_telnet(project_config)

    try:
        telnet.execute_command('echo hello')
    except:
        print('Telnet连接失败 !')
        return 1

    return 0


def run(project_config, option_config):
    status = check_telnet(project_config)

    if status != 0:
        raise InterruptSystemError('Telnet开启失败')

    return status
