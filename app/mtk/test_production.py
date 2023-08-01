import json
import time

import numpy as np
from general.tool import MTKTelnetOperation, wait_until_device_reboot
from mtk.check_telnet import check_telnet
from mtk.output_device_info import get_device_info_str, get_device_version_str


def backup_device_info(project_config):
    project_config['device_version_str'] = get_device_version_str(project_config)
    project_config['device_info_str'] = get_device_info_str(project_config)


def run(project_config, option_config):
    telnet = MTKTelnetOperation(project_config['telnet_ip'],
                                int(project_config['telnet_port']),
                                project_config['telnet_username'],
                                project_config['telnet_password'])

    with open(project_config['device_info_backup_path'], 'r') as file:
        device_info = json.load(file)

    device_info_default = {
        'productclass': 'STARNET_DEVICE',
        'vid': '0x00060000',
        'mac': '5C:CB:CA:91:99:A1',
        'sn': 'CMCC200F731C',
        'productstyle': 'cmcc',
        'areacode': '0',
        'authcode': '01B70BAE0BBF3F569401AD649250B5B7E14EF9257E560B8C749D564F01E37EF2',
        'hardversion': 'HV1.0.0',
        'manufacturer': 'Star-Net',
        'oui': '001122',
        'imei': '001122334456789',
        'ssid2': 'STARNET_DEVICE_WIFI',
        'ssid2pwd': '12345678',
        'ssid5': 'STARNET_DEVICE_WIFI',
        'ssid5pwd': '12345678',
        'webacct': 'userAdmin',
        'webpwd': 'aDm8H%MdA',
        'ponmac': '5C:CB:CA:91:99:A1',
        'gponsn': 'CMCC200F731C',
        'egponswitch': 'gpon',
        'oem': 'starnet'
    }

    operation_list = [
        ['清除factory分区参数', 'clear', '', 'Factorytool Clear Success'],
        ['写入产品型号', 'set', 'productclass', 'Factorytool Write Success'],
        ['校验产品型号', 'get', 'productclass', ''],
        ['写入产品风格', 'set', 'productstyle', 'Factorytool Write Success'],
        ['校验产品风格', 'get', 'productstyle', ''],
        ['写入VID', 'set', 'vid', 'Factorytool Write Success'],
        ['校验VID', 'get', 'vid', ''],
        ['写入MAC', 'set', 'mac', 'Factorytool Write Success'],
        ['校验MAC', 'get', 'mac', ''],
        ['写入SN', 'set', 'sn', 'Factorytool Write Success'],
        ['校验SN', 'get', 'sn', ''],
        ['写入授权码', 'set', 'authcode', 'Factorytool Write Success'],
        ['校验授权码', 'get', 'authcode', ''],
        ['校验授权状态', 'check authcode', '', 'Auth State: Authentication OK'],
        ['写入硬件版本号', 'set', 'hardversion', 'Factorytool Write Success'],
        ['校验硬件版本号', 'get', 'hardversion', ''],
        ['写入厂家名称', 'set', 'manufacturer', 'Factorytool Write Success'],
        ['校验厂家名称', 'get', 'manufacturer', ''],
        ['写入厂家OUI', 'set', 'oui', 'Factorytool Write Success'],
        ['校验厂家OUI', 'get', 'oui', ''],
        ['写入IMEI', 'set', 'imei', 'Factorytool Write Success'],
        ['校验IMEI', 'get', 'imei', ''],
        ['写入2.4G频段SSID', 'set', 'ssid2', 'Factorytool Write Success'],
        ['校验2.4G频段SSID', 'get', 'ssid2', ''],
        ['写入2.4G频段SSID的密码', 'set', 'ssid2pwd', 'Factorytool Write Success'],
        ['校验2.4G频段SSID的密码', 'get', 'ssid2pwd', ''],
        ['写入5G频段SSID', 'set', 'ssid5', 'Factorytool Write Success'],
        ['校验5G频段SSID', 'get', 'ssid5', ''],
        ['写入5G频段SSID的密码', 'set', 'ssid5pwd', 'Factorytool Write Success'],
        ['校验5G频段SSID的密码', 'get', 'ssid5pwd', ''],
        ['写入Web页面登录账号', 'set', 'webacct', 'Factorytool Write Success'],
        ['校验Web页面登录账号', 'get', 'webacct', ''],
        ['写入Web页面登录密码', 'set', 'webpwd', 'Factorytool Write Success'],
        ['校验Web页面登录密码', 'get', 'webpwd', ''],
        ['写入PON MAC', 'set', 'ponmac', 'Factorytool Write Success'],
        ['校验PON MAC', 'get', 'ponmac', ''],
        ['写入GPON SN', 'set', 'gponsn', 'Factorytool Write Success'],
        ['校验GPON SN', 'get', 'gponsn', ''],
        ['写入EGPON自适应参数', 'set', 'egponswitch',
         f'Factorytool Change EGPON Switch to {device_info["egponswitch"]} Success'],
        ['校验EGPON自适应参数', 'get', 'egponswitch', ''],
        ['写入OEM参数', 'set', 'oem', 'Factorytool Write Success'],
        ['校验OEM参数', 'get', 'oem', ''],
        ['写入地区码', 'set', 'areacode', f'Factorytool Change AreaCode to {device_info["areacode"]} Success']
    ]

    for operation in operation_list:
        command_state = 'NOK'
        if len(operation[2]) > 0 and len(device_info[operation[2]]) <= 0:
            device_info[operation[2]] = device_info_default.get(operation[2], '')
        if operation[1] == 'set':
            command_result = telnet.execute_command(f'factorytool set {operation[2]} {device_info[operation[2]]}')
            if operation[3] in command_result:
                command_result = operation[3]
                command_state = 'OK'
        elif operation[1] == 'get':
            command_result = telnet.execute_command(f'factorytool get {operation[2]}')
            command_result = command_result.split('\r\n', 3)[3]
            if device_info[operation[2]] in command_result:
                command_state = 'OK'
        else:
            command_result = telnet.execute_command(f'factorytool {operation[1]}')
            if operation[3] in command_result:
                command_result = operation[3]
                command_state = 'OK'

        project_config['report_list'].append([operation[0], command_result, command_state])

    telnet.close()

    wait_until_device_reboot(project_config['telnet_ip'])
    time.sleep(30)

    check_telnet(project_config)
    command_state = 'NOK'
    command_result = telnet.execute_command(f'factorytool get areacode')
    command_result = command_result.split('\r\n', 3)[3]
    if f'Area Code: {device_info["areacode"]}' in command_result:
        command_state = 'OK'
    project_config['report_list'].append(['校验地区码', command_result, command_state])

    for i in range(2):
        project_config['report_list'].append([np.nan, np.nan, np.nan])

    return 0
