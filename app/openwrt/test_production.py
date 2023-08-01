import json
import time

import numpy as np

from general.tool import OPENWRTTelnetOperation, wait_until_device_power_off, wait_until_device_reboot


def run(project_config, option_config):
    for i in range(2):
        project_config['report_list'].append([np.nan, np.nan, np.nan])

    telnet = OPENWRTTelnetOperation(project_config['telnet_ip'],
                                    int(project_config['telnet_port']),
                                    project_config['telnet_username'],
                                    project_config['telnet_password'])

    device_info = {
        'mac': '5CCBCA9199A1',
        'sn': 'CMCC200F731C',
        'imei': '001122334456789',
        'authcode': '01B70BAE0BBF3F569401AD649250B5B7E14EF9257E560B8C749D564F01E37EF2',
        'model': 'SU1120G-AX188',
        'hwver': 'HV1.0.0',
        'areacode': '0'
    }

    operation_list = [
        ['写入MAC', 'set', 'mac', ''],
        ['校验MAC', 'get', 'mac', ''],
        ['写入SN', 'set', 'sn', ''],
        ['校验SN', 'get', 'sn', ''],
        ['写入IMEI', 'set', 'imei', ''],
        ['校验IMEI', 'get', 'imei', ''],
        ['写入授权码', 'set', 'authcode', ''],
        ['校验授权码', 'get', 'authcode', ''],
        ['写入产品型号', 'set', 'model', ''],
        ['校验产品型号', 'get', 'model', ''],
        ['写入硬件版本号', 'set', 'hwver', ''],
        ['校验硬件版本号', 'get', 'hwver', ''],
        ['写入地区码', 'set', 'areacode', ''],
        ['校验地区码', 'get', 'areacode', '']
    ]

    for operation in operation_list:
        command_state = 'NOK'
        if operation[1] == 'set':
            command_result = telnet.execute_command(f'idmanager set {operation[2]} {device_info[operation[2]]}')
            if operation[3] in command_result:
                command_result = operation[3]
                command_state = 'OK'
        elif operation[1] == 'get':
            command_result = telnet.execute_command(f'idmanager get {operation[2]}')
            command_result = command_result.split('\r\n')[0]
            command_state = 'OK'
        else:
            command_result = telnet.execute_command(f'idmanager {operation[1]}')
            if operation[3] in command_result:
                command_result = command_result.split('\r\n')[0]
                command_state = 'OK'

        project_config['report_list'].append([operation[0], command_result, command_state])

    telnet.execute_command('jffs2reset -y && reboot -d 5')
    wait_until_device_power_off(project_config['telnet_ip'])

    telnet.close()

    wait_until_device_reboot(project_config['telnet_ip'])
    time.sleep(90)

    for i in range(2):
        project_config['report_list'].append([np.nan, np.nan, np.nan])

    return 0
