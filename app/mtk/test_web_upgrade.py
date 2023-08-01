import time

from general.tool import wait_until_device_power_off, \
    wait_switch_frame, wait_until_clickable, wait_until_device_reboot, mtk_web_login
from mtk.output_device_info import get_device_version_dict
from selenium import webdriver


def web_upgrade(project_config, upgrade_file):
    driver = webdriver.Chrome()
    driver.maximize_window()

    mtk_web_login(driver, project_config)

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


def check_version(project_config):
    device_version_dict = get_device_version_dict(project_config)

    if device_version_dict[f'Local_Software_Version'] == f'{project_config["version"]}.cmp':
        return 0
    else:
        return 1


def run(project_config, option_config):
    upgrade_file = f'{project_config["compare_file_path"]}/tclinux_java_osgi_allinone'

    web_upgrade(project_config, upgrade_file)

    wait_until_device_reboot(project_config['telnet_ip'])
    time.sleep(30)

    status = check_version(project_config)

    if status == 0:
        project_config['report_list'].append(['Web页面升级测试', '升级成功', 'OK'])
    else:
        project_config['report_list'].append(['Web页面升级测试', '升级失败', 'ERROR'])

    return status
