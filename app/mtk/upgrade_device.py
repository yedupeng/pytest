import time

from general.tool import wait_until_device_power_off, \
    wait_switch_frame, wait_until_clickable, wait_until_device_reboot, mtk_web_login
from selenium import webdriver


def web_upgrade(project_config, upgrade_file):
    driver = webdriver.Chrome()
    driver.maximize_window()

    mtk_web_login(driver, project_config)

    time.sleep(10)
    driver.switch_to.default_content()
    wait_switch_frame(driver, 'contentfrm')
    wait_until_clickable(driver, '//*[@id="main_menu"]/table/tbody/tr/td[7]').click()
    wait_until_clickable(driver, '//*[@id="mag-reset"]').click()
    wait_until_clickable(driver, '//*[@id="设备升级"]').click()
    wait_until_clickable(driver, '//*[@id="设备升级_item"]/form/table/tbody/tr[2]/td/input[3]').click()
    wait_until_clickable(driver, '//*[@id="设备升级_item"]/form/table/tbody/tr[3]/td/input').send_keys(upgrade_file)
    wait_until_clickable(driver, '//*[@id="btnOK"]').click()

    wait_until_device_power_off(project_config['telnet_ip'])
    driver.quit()


def run(project_config, option_config):
    upgrade_file = f'{project_config["upgrade_file_path"]}/tclinux_java_osgi_allinone'

    web_upgrade(project_config, upgrade_file)

    wait_until_device_reboot(project_config['telnet_ip'])
    time.sleep(30)

    return 0
