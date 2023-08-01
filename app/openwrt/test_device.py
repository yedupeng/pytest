import json
import time

import numpy as np

from general.tool import OPENWRTTelnetOperation, wait_until_device_power_off, wait_until_device_reboot


def run(project_config, option_config):
    telnet = OPENWRTTelnetOperation(project_config['telnet_ip'],
                                    int(project_config['telnet_port']),
                                    project_config['telnet_username'],
                                    project_config['telnet_password'])

    command = f'cat /etc/wireless/mediatek/mt7915.dbdc.b0.dat | grep SSID1'
    command_result = telnet.execute_command(command)
    command_result = command_result.split('\r\n')[0]
    if 'Starnet5CCBCA9199A1' in command_result:
        command_state = 'OK'
    else:
        command_state = 'NOK'
    project_config['report_list'].append(['校验2.4G配置文件', command_result, command_state])

    command = f'cat /etc/wireless/mediatek/mt7915.dbdc.b1.dat | grep SSID1'
    command_result = telnet.execute_command(command)
    command_result = command_result.split('\r\n')[0]
    if 'Starnet5CCBCA9199A1' in command_result:
        command_state = 'OK'
    else:
        command_state = 'NOK'
    project_config['report_list'].append(['校验5G配置文件', command_result, command_state])

    command = f'iwpriv ra0 stat | grep CurrentTemperature'
    command_result = telnet.execute_command(command)
    command_result = command_result.split('\r\n')[0]
    if int(command_result.replace('CurrentTemperature              = ', '')) > 0:
        command_state = 'OK'
    else:
        command_state = 'NOK'
    project_config['report_list'].append(['校验2.4G无线温度', command_result, command_state])

    command = f'iwpriv rax0 stat | grep CurrentTemperature'
    command_result = telnet.execute_command(command)
    command_result = command_result.split('\r\n')[0]
    if int(command_result.replace('CurrentTemperature              = ', '')) > 0:
        command_state = 'OK'
    else:
        command_state = 'NOK'
    project_config['report_list'].append(['校验5G无线温度', command_result, command_state])

    command = f'ifconfig | grep ra0'
    command_result = telnet.execute_command(command)
    command_result = command_result.split('\r\n')[0]
    if 'HWaddr 5C:CB:CA:91:99:A1' in command_result:
        command_state = 'OK'
    else:
        command_state = 'NOK'
    project_config['report_list'].append(['校验2.4G无线接口', command_result, command_state])

    command = f'ifconfig | grep rax0'
    command_result = telnet.execute_command(command)
    command_result = command_result.split('\r\n')[0]
    if 'HWaddr 5E:CB:CA:81:99:A1' in command_result:
        command_state = 'OK'
    else:
        command_state = 'NOK'
    project_config['report_list'].append(['校验5G无线接口', command_result, command_state])

    telnet.close()

    for i in range(2):
        project_config['report_list'].append([np.nan, np.nan, np.nan])

    return 0
