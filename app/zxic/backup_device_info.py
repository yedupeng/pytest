import json

from plugin.tool import get_vid
from plugin.tool import ZXICTelnetOperation


def run(project_config, option_config):
    device_info_backup = {}
    telnet = ZXICTelnetOperation(project_config['telnet_ip'],
                                 int(project_config['telnet_port']),
                                 project_config['telnet_username'],
                                 project_config['telnet_password'],
                                 project_config['telnet_su_password'])
    operation_dict = {'swversion': 'sidbg 64 uptool swversion',
                      'product': 'sismac 2 32774',
                      'vid': 'sismac 2 32772',
                      'hard_version': 'sismac 2 32775',
                      'sn': 'sismac 2 512',
                      'sn_head': 'sismac 2 2176',
                      'sn_tail': 'sismac 2 2177',
                      'auth_code': 'sismac 2 2816',
                      'factory_name': 'sismac 2 2185',
                      'factory_oui': 'sismac 2 768',
                      'imei': 'sismac 2 32777'}

    for i in range(256, 264):
        operation_dict[f'mac{i - 255}'] = f'sismac 2 {i}'

    for operation in operation_dict:
        command_result = telnet.execute_command(operation_dict[operation]).replace('\r', '')
        if 'erro' in command_result:
            continue
        if operation == 'vid':
            command_result = get_vid(command_result)
        device_info_backup[operation] = command_result

    with open(project_config['device_info_backup_path'], 'w') as file:
        json.dump(device_info_backup, file, indent=4)

    telnet.close()

    return 0
