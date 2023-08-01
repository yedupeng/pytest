import time

from selenium import webdriver
from selenium.webdriver.common.by import By

from plugin.tool import ZXICTelnetOperation, wait_until_device_power_on, wait_until_device_power_off, config_str_to_dict, \
    wait_switch_frame, wait_until_clickable


def get_device_version(telnet):
    while True:
        cmd_res = telnet.execute_command('sidbg 64 uptool swversion')
        if 'local version' in cmd_res:
            break
        else:
            time.sleep(10)
    return config_str_to_dict(cmd_res, ':')['local version']


def web_upgrade(project_config, bin_path):
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
    wait_until_clickable(driver, '//*[@id="main_menu"]/table/tbody/tr/td[6]').click()
    wait_until_clickable(driver, '//*[@id="smSysMgr"]').click()
    wait_until_clickable(driver, '//*[@id="ssmSoftwareUpr"]').click()
    wait_until_clickable(driver, '//*[@id="VersionUpload"]').send_keys(bin_path)
    wait_until_clickable(driver, '//*[@id="upload"]').click()

    wait_until_device_power_off(project_config['telnet_ip'])
    driver.quit()


def run(project_config, option_config):
    telnet = ZXICTelnetOperation(project_config['telnet_ip'],
                                 int(project_config['telnet_port']),
                                 project_config['telnet_username'],
                                 project_config['telnet_password'],
                                 project_config['telnet_su_password'])

    bin_default_path = f'{project_config["pack_path"]}/升级文件/{project_config["model"]}_{project_config["version"]}' \
                       f'{option_config["bin_default"]}'

    bin_path_list = []
    for bin_path in option_config['bin']:
        bin_path_list.append(f'{project_config["pack_path"]}/升级文件/对比升级软件/'
                             f'{project_config["model"]}_{project_config["version"]}{bin_path}')

    for bin_path in bin_path_list:
        web_upgrade(project_config, bin_path)

        wait_until_device_power_on(project_config['telnet_ip'])
        time.sleep(20)
        compare_version = get_device_version(telnet)
        telnet.close()

        web_upgrade(project_config, bin_default_path)

        wait_until_device_power_on(project_config['telnet_ip'])
        time.sleep(20)
        origin_version = get_device_version(telnet)
        telnet.close()

        if compare_version != f'{origin_version}.cmp':
            project_config['report_list'].append(['Web页面升级测试', '升级失败', 'NOK'])
            return 1

    project_config['report_list'].append(['Web页面升级测试', '升级成功', 'OK'])
    return 0
