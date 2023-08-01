import json

from general.tool import MTKTelnetOperation


def run(project_config, option_config):
    device_info_backup = {}
    telnet = MTKTelnetOperation(project_config['telnet_ip'],
                                int(project_config['telnet_port']),
                                project_config['telnet_username'],
                                project_config['telnet_password'])
    operation_list = {'productclass',
                      'vid',
                      'mac',
                      'sn',
                      'productstyle',
                      'areacode',
                      'authcode',
                      'hardversion',
                      'manufacturer',
                      'oui',
                      'imei',
                      'ssid2',
                      'ssid2pwd',
                      'ssid5',
                      'ssid5pwd',
                      'webacct',
                      'webpwd',
                      'ponmac',
                      'gponsn',
                      'egponswitch',
                      'oem'}

    for operation in operation_list:
        command_result = telnet.execute_command(f'factorytool get {operation}').split('\r\n')[3].replace('-5G', '')
        if 'is not set' in command_result:
            command_value = ''
        else:
            if ': ' in command_result:
                command_value = command_result.split(': ')[1]
            else:
                continue
        device_info_backup[operation] = command_value

    with open(project_config['device_info_backup_path'], 'w') as file:
        json.dump(device_info_backup, file, indent=4)

    telnet.close()

    return 0
