import os
import threading
import time
import serial
import requests
import telnetlib
import subprocess
import xml.etree.ElementTree as ElementTree
from collections import defaultdict

from selenium import webdriver
from selenium.common import TimeoutException, NoSuchFrameException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class InterruptSystemError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f'{self.value}'


class ZXICTelnetOperation:
    def __init__(self, host_ip, host_port, username, password, su_password):
        self.host_ip = host_ip
        self.host_port = host_port
        self.username = username
        self.password = password
        self.su_password = su_password
        self.telnet = telnetlib.Telnet()
        self.is_login = False

    def login(self):
        try:
            self.telnet.open(self.host_ip, port=self.host_port)
        except OSError:
            return False
        self.telnet.read_until(b'Login: ', timeout=10)
        self.telnet.write(self.username.encode('ascii') + b'\n')
        self.telnet.read_until(b'Password: ', timeout=10)
        self.telnet.write(self.password.encode('ascii') + b'\n')
        self.telnet.read_until(b'~ $ ', timeout=10)
        self.telnet.write('su'.encode('ascii') + b'\n')
        self.telnet.read_until(b'Password: ', timeout=10)
        self.telnet.write(self.su_password.encode('ascii') + b'\n')
        time.sleep(2)
        command_result = self.telnet.read_very_eager().decode('gbk')
        if '/ # ' in command_result:
            self.is_login = True
            return True
        else:
            return False

    def close(self):
        self.telnet.write(b"exit\n")
        self.telnet.close()
        self.is_login = False

    def execute_command(self, command, wait_time=20):
        if not self.is_login:
            self.login()
        self.telnet.write(f'{command}\n'.encode())
        result = self.telnet.read_until(b'/ # ', timeout=wait_time).decode('ascii') \
            .replace(f'{command}\r\n', '').replace('\n/ # ', '')
        return result


class MTKTelnetOperation:
    def __init__(self, host_ip, host_port, username, password):
        self.host_ip = host_ip
        self.host_port = host_port
        self.username = username
        self.password = password
        self.telnet = telnetlib.Telnet()
        self.is_login = False

    def login(self):
        try:
            self.telnet.open(self.host_ip, port=self.host_port)
        except OSError:
            return False
        self.telnet.read_until(b'Login: ', timeout=10)
        self.telnet.write(self.username.encode('ascii') + b'\n')
        self.telnet.read_until(b'Password: ', timeout=10)
        self.telnet.write(self.password.encode('ascii') + b'\n')
        self.telnet.read_until(b' > ', timeout=10)
        self.telnet.write('sh'.encode('ascii') + b'\n')
        time.sleep(2)
        command_result = self.telnet.read_very_eager().decode('gbk')
        if '# ' in command_result:
            self.is_login = True
            return True
        else:
            return False

    def close(self):
        self.telnet.write(b"exit\n")
        self.telnet.close()
        self.is_login = False

    def execute_command(self, command, wait_time=20):
        if not self.is_login:
            self.login()
        self.telnet.write(f'{command}\n'.encode())
        result = self.telnet.read_until(b'# ', timeout=wait_time).decode('ascii') \
            .replace(f'{command}\r\n', '').replace('\r\n# ', '')
        return result


class OPENWRTTelnetOperation:
    def __init__(self, host_ip, host_port, username, password):
        self.host_ip = host_ip
        self.host_port = host_port
        self.username = username
        self.password = password
        self.telnet = telnetlib.Telnet()
        self.is_login = False

    def login(self):
        try:
            self.telnet.open(self.host_ip, port=self.host_port)
        except OSError:
            return False
        self.telnet.read_until(b'LEDE login: ', timeout=10)
        self.telnet.write(self.username.encode('ascii') + b'\n')
        self.telnet.read_until(b'Password: ', timeout=10)
        self.telnet.write(self.password.encode('ascii') + b'\n')
        self.telnet.read_until(b'# ', timeout=10)
        self.telnet.write('sh'.encode('ascii') + b'\n')
        time.sleep(1)
        command_result = self.telnet.read_very_eager().decode('gbk')
        if '# ' in command_result:
            self.is_login = True
            return True
        else:
            return False

    def close(self):
        self.telnet.write(b"exit\n")
        self.telnet.close()
        self.is_login = False

    def execute_command(self, command, wait_time=20):
        if not self.is_login:
            self.login()
        self.telnet.write(f'{command}\n'.encode())
        result = self.telnet.read_until(b'# ', timeout=wait_time).decode('ascii') \
            .replace(f'{command}\r\n', '').replace('\r\n# ', '')
        return result


class SerialOperation:
    def __init__(self, port, baud_rate, bytesize, parity, stop_bits):
        self.serial = serial.Serial(port, baud_rate, bytesize, parity, stop_bits)

    def read(self):
        try:
            return str(self.serial.readline(), encoding='utf-8').replace('\n', '')
        except Exception:
            return ''

    def readline(self):
        return str(self.serial.readline(), encoding='utf-8')

    def write(self, cmd):
        return self.serial.write(f'{cmd}\n'.encode())

    def reset_buffer(self):
        self.serial.reset_input_buffer()
        self.serial.reset_output_buffer()
        return 0

    def close(self):
        self.serial.close()
        return 0


class SerialLogThread(threading.Thread):
    def __init__(self, serial_object, output_log_path='serial_log.txt'):
        super(SerialLogThread, self).__init__()
        self.serial = serial_object
        self.log_file_path = output_log_path
        self.isRun = True

    def run(self):
        while self.isRun is True:
            serial_str = self.serial.readline()
            with open(self.log_file_path, 'a') as file:
                file.write(serial_str)

    def close(self):
        self.isRun = False
        self.serial.close()


class SerialUpgradeThread(threading.Thread):
    def __init__(self, serial_object, enter_boot_times=0, output_log=''):
        super(SerialUpgradeThread, self).__init__()
        self.serial = serial_object
        self.enter_boot_times = enter_boot_times
        self.isRun = True
        if len(output_log) > 0:
            self.output_log = True
            self.log_file_path = output_log
            self.log = ''
        else:
            self.output_log = False

    def run(self):
        while self.isRun is True:
            serial_str = self.serial.read()
            if 'Hit 1 to upgrade software version' in serial_str and self.enter_boot_times > 0:
                self.serial.write('1')
                self.enter_boot_times -= 1
            if self.output_log is True:
                self.log = self.log + serial_str

    def close(self):
        self.isRun = False
        if self.output_log is True:
            with open(self.log_file_path, 'w') as file:
                file.write(self.log)


class Shell:
    def __init__(self, log_path='log.txt'):
        self.shell_log_path = log_path

    def set_log_path(self, log_path):
        self.shell_log_path = log_path
        self.clean_shell_log()

    def clean_shell_log(self):
        open(self.shell_log_path, 'w')

    def run(self, cmd):
        log = open(self.shell_log_path, 'a')
        process = subprocess.Popen(cmd, stdout=log, stderr=log, shell=True)
        return process.wait()


def load_config(path):
    try:
        config_tree = ElementTree.parse(path)
        config_root = config_tree.getroot()
        config_root.iter()
    except Exception as e:
        print(f'配置文件解析失败: {e}')
        return 1
    else:
        return 0


def etree_to_dict_with_parent(t):
    d = {t.tag: {} if t.attrib else None}
    children = list(t)
    if children:
        dd = defaultdict(list)
        for dc in map(etree_to_dict_with_parent, children):
            for k, v in dc.items():
                dd[k].append(v)
        d = {t.tag: {k: v[0] if len(v) == 1 else v
                     for k, v in dd.items()}}
    if t.text:
        text = t.text.strip()
        if children or t.attrib:
            if text:
                d[t.tag]['#text'] = text
        else:
            d[t.tag] = text
    return d


def etree_to_dict(t):
    return etree_to_dict_with_parent(t)[t.tag]


def get_vid(vid_str):
    flash_vid = vid_str.split('\n')[0].split(':')[1].replace(' ', '')
    tag_vid = vid_str.split('\n')[1].split(':')[1].replace(' ', '')
    if flash_vid != tag_vid:
        print(f'错误：flash_vid（{flash_vid}）与tag_vid（{tag_vid}）不一致!')
    return flash_vid


def get_generate_mac(first_mac, num):
    mac_address = '{:012X}'.format(int(first_mac.replace('-', '').replace(':', ''), 16) + num)
    format_mac = [mac_address[x:x + 2] for x in range(0, len(mac_address), 2)]
    return ':'.join(format_mac)


def config_str_to_dict(config_str, separator):
    config_dict = {}
    config_item_list = config_str.split('\n')
    for config_item in config_item_list:
        config_key_value = config_item.split(separator)
        if len(config_key_value) >= 2:
            config_dict[config_key_value[0].strip()] = config_key_value[1].strip()
    return config_dict


def wait_until_device_power_on(target_ip, max_wait_time=300):
    start_time = int(time.time())
    while True:
        if shellrun(f'ping -c 3 {target_ip}') == 0:
            return 0
        if int(time.time()) - start_time > max_wait_time:
            return 1


def wait_until_device_power_off(target_ip, max_wait_time=150):
    start_time = int(time.time())
    while True:
        if shellrun(f'ping -c 3 {target_ip}') == 1:
            return 0
        if int(time.time()) - start_time > max_wait_time:
            return 1


def wait_until_device_web_on(target_url, max_wait_time=150):
    driver = webdriver.Chrome()
    start_time = int(time.time())
    while True:
        try:
            driver.maximize_window()
            driver.get(target_url)
            WebDriverWait(driver, 5).until(expected_conditions.title_contains('Login'))
            driver.close()
            time.sleep(10)
            return 0
        except TimeoutException:
            driver.close()
            time.sleep(10)
        except Exception:
            time.sleep(10)

        if int(time.time()) - start_time > max_wait_time:
            return 1


def wait_until_device_reboot(target_ip, max_power_off_wait_time=150, max_power_on_wait_time=300):
    wait_until_device_power_off(target_ip, max_power_off_wait_time)
    wait_until_device_power_on(target_ip, max_power_on_wait_time)


def wait_until_device_reboot_web_on(target_ip, target_url, max_wait_time=450):
    wait_until_device_power_off(target_ip, max_wait_time)
    wait_until_device_power_on(target_ip, max_wait_time)
    wait_until_device_web_on(target_url, max_wait_time)


def zxic_webpage_move_to_end(driver):
    driver.switch_to.default_content()
    driver.find_element_by_id('mainFrame').send_keys(Keys.END)
    driver.switch_to.frame('mainFrame')


def mtk_webpage_move_to_top(driver):
    driver.execute_script('window.scrollTo(0, 0);')
    time.sleep(1)


def mtk_webpage_move_to_end(driver):
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(1)


def mtk_input_text(driver, xpath, text):
    driver.find_element(By.XPATH, xpath).send_keys(Keys.CONTROL, 'a')
    driver.find_element(By.XPATH, xpath).send_keys(Keys.BACK_SPACE)
    driver.find_element(By.XPATH, xpath).send_keys(text)


def wait_until_clickable(driver, xpath):
    return WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.XPATH, xpath)))


def click_hide_element(driver, xpath):
    element = driver.find_element(By.XPATH, xpath)
    driver.execute_script('arguments[0].click()', element)


def mtk_web_login(driver, project_config):
    driver.get(project_config['web_address'])
    time.sleep(2)
    btn_username = driver.find_element(By.XPATH, '//*[@id="div_name"]/input')
    btn_password = driver.find_element(By.XPATH, '//*[@id="logincode"]')
    btn_username.click()
    btn_username.clear()
    btn_username.send_keys(project_config['web_username'])
    btn_password.click()
    btn_password.clear()
    btn_password.send_keys(project_config['web_password'])
    driver.find_element(By.XPATH, '//*[@id="loginSubmit"]').click()


def wait_switch_frame(driver, frame_name):
    time.sleep(3)
    try:
        driver.switch_to.frame(frame_name)
    except NoSuchFrameException:
        driver.refresh()
        time.sleep(3)
        driver.switch_to.frame(frame_name)


def shellrun(cmd):
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    return process.wait()
