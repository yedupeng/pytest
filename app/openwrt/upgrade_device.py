import time
import pyautogui as ui

from selenium import webdriver

from general.tool import wait_until_device_power_off, \
    wait_switch_frame, wait_until_clickable, wait_until_device_reboot, mtk_web_login
from selenium.webdriver.common.by import By


def openwrt_web_login(driver, project_config):
    driver.get(project_config['web_address'])
    time.sleep(2)
    btn_password = driver.find_element(By.XPATH, '//*[@id="app"]/div[3]/div[1]/div/input')
    btn_password.click()
    btn_password.clear()
    btn_password.send_keys('admin')
    driver.find_element(By.XPATH, '//*[@id="app"]/div[3]/div[1]/div/span/span/button').click()


def web_upgrade(project_config, upgrade_file):
    driver = webdriver.Chrome()
    driver.maximize_window()

    openwrt_web_login(driver, project_config)

    driver.switch_to.default_content()
    wait_until_clickable(driver, '//*[@id="app"]/div[3]/button[4]').click()
    wait_until_clickable(driver, '//*[@id="app"]/div[2]/div/div/form/div[2]/div/div/span').click()
    wait_until_clickable(driver, '//*[@id="app"]/div[2]/div/div/form/div[3]/div/div/div/div').click()

    time.sleep(2)
    ui.click(954, 533)
    time.sleep(2)
    ui.press('right', 20)
    time.sleep(1)
    ui.press('enter', 2)
    wait_until_clickable(driver, '//*[@id="app"]/div[3]/button[1]').click()

    wait_until_device_power_off(project_config['telnet_ip'])

    driver.quit()


def run(project_config, option_config):
    upgrade_file = f'/mnt/sda1_newdisk/tftp/SU1120G-AX18_V1.0.0.10_AX_NOR_UPGRADE.ubin'

    web_upgrade(project_config, upgrade_file)

    wait_until_device_reboot(project_config['telnet_ip'])
    time.sleep(90)

    status = 0

    if status == 0:
        project_config['report_list'].append(['原厂升级自研', '升级成功', 'OK'])
    else:
        project_config['report_list'].append(['原厂升级自研', '升级失败', 'ERROR'])

    return status
