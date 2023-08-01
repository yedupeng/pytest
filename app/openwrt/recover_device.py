import time

from selenium import webdriver

from general.tool import wait_until_device_power_off, \
    wait_switch_frame, wait_until_clickable, wait_until_device_reboot, mtk_web_login
from selenium.webdriver.common.by import By


def openwrt_web_login(driver, project_config):
    driver.get(project_config['web_address'])
    time.sleep(2)
    btn_username = driver.find_element(By.XPATH, '//*[@id="maincontent"]/form/div[1]/fieldset/fieldset/div[1]/div/input')
    btn_password = driver.find_element(By.XPATH, '//*[@id="maincontent"]/form/div[1]/fieldset/fieldset/div[2]/div/input')
    btn_username.click()
    btn_username.clear()
    btn_username.send_keys(project_config['web_username'])
    btn_password.click()
    btn_password.clear()
    btn_password.send_keys(project_config['web_password'])
    driver.find_element(By.XPATH, '//*[@id="maincontent"]/form/div[2]/input[1]').click()


def web_upgrade(project_config, upgrade_file):
    driver = webdriver.Chrome()
    driver.maximize_window()

    openwrt_web_login(driver, project_config)

    driver.switch_to.default_content()
    wait_until_clickable(driver, '/html/body/header/div/div/ul/li[2]/a').click()
    wait_until_clickable(driver, '/html/body/header/div/div/ul/li[2]/ul/li[8]/a').click()
    wait_until_clickable(driver, '//*[@id="keep"]').click()
    wait_until_clickable(driver, '//*[@id="image"]').send_keys(upgrade_file)
    wait_until_clickable(driver, '//*[@id="maincontent"]/fieldset/fieldset[2]/form/div[2]/div[2]/div/input[2]').click()

    driver.switch_to.default_content()
    wait_until_clickable(driver, '//*[@id="maincontent"]/div/form/input[5]').click()

    wait_until_device_power_off(project_config['telnet_ip'])

    driver.quit()


def run(project_config, option_config):
    upgrade_file = f'/mnt/sda1_newdisk/tftp/ap_origion.ubin'

    web_upgrade(project_config, upgrade_file)

    wait_until_device_reboot(project_config['telnet_ip'])
    time.sleep(90)

    status = 0

    if status == 0:
        project_config['report_list'].append(['自研还原原厂', '升级成功', 'OK'])
    else:
        project_config['report_list'].append(['自研还原原厂', '升级失败', 'ERROR'])

    return status
