import json

import numpy as np

from plugin.tool import get_generate_mac
from plugin.tool import ZXICTelnetOperation


def run(project_config, option_config):
    telnet = ZXICTelnetOperation(project_config['telnet_ip'],
                                 int(project_config['telnet_port']),
                                 project_config['telnet_username'],
                                 project_config['telnet_password'],
                                 project_config['telnet_su_password'])

    with open(project_config['device_info_backup_path'], 'r') as file:
        device_info = json.load(file)
    operation_list = [
        ['设置产品型号', device_info.get("product"), f'sismac 1 32774 {device_info.get("product")}', 'sismac success'],
        ['校验产品型号', device_info.get("product"), 'sismac 2 32774', f'{device_info.get("product")}'],
        ['设置VID', device_info.get("vid"), f'sismac 1 32772 {device_info.get("vid")}', 'VID set'],
        ['校验VID', device_info.get("vid"), 'sismac 2 32772', f'{device_info.get("vid")}'],
        ['设置硬件版本号', device_info.get("hard_version"), f'sismac 1 32775 {device_info.get("hard_version")}',
         'sismac success'],
        ['校验硬件版本号', device_info.get("hard_version"), 'sismac 2 32775', f'{device_info.get("hard_version")}'],
        ['写入MAC', device_info.get("mac1"), f'sismac 1 256 {device_info.get("mac1")}', 'sismac success'],
        ['校验MAC_256', device_info.get("mac1"), 'sismac 2 256', f'{device_info.get("mac1")}'],
        ['校验MAC_257', device_info.get("mac1"), 'sismac 2 257', f'{get_generate_mac(device_info.get("mac1"), 1)}'],
        ['校验MAC_258', device_info.get("mac1"), 'sismac 2 258', f'{get_generate_mac(device_info.get("mac1"), 2)}'],
        ['校验MAC_259', device_info.get("mac1"), 'sismac 2 259', f'{get_generate_mac(device_info.get("mac1"), 3)}'],
        ['校验MAC_260', device_info.get("mac1"), 'sismac 2 260', f'{get_generate_mac(device_info.get("mac1"), 4)}'],
        ['校验MAC_261', device_info.get("mac1"), 'sismac 2 261', f'{get_generate_mac(device_info.get("mac1"), 5)}'],
        ['校验MAC_262', device_info.get("mac1"), 'sismac 2 262', f'{get_generate_mac(device_info.get("mac1"), 6)}'],
        ['校验MAC_263', device_info.get("mac1"), 'sismac 2 263', f'{get_generate_mac(device_info.get("mac1"), 7)}'],
        ['设置SN', device_info.get("sn"), f'sismac 1 512 {device_info.get("sn")}', 'sismac success'],
        ['校验SN', device_info.get("sn"), 'sismac 2 512', f'{device_info.get("sn")}'],
        ['校验厂商id', device_info.get("sn") and len(device_info.get("sn")) == 7, 'sismac 2 2176',
         f'{device_info.get("sn")[0:3]}'],
        ['校验GponSn', device_info.get("sn") and len(device_info.get("sn")) == 7, 'sismac 2 2177',
         f'{device_info.get("sn")[4:]}'],
        ['写入授权码', device_info.get("auth_code"), f'sismac 1 2816 {device_info.get("auth_code")}', 'sismac success'],
        ['校验授权码', device_info.get("auth_code"), 'sismac 2 2816', f'{device_info.get("auth_code")}'],
        ['校验授权状态', device_info.get("auth_code"), 'autquary', 'Authentication OK'],
        ['写入厂家名称', device_info.get("factory_name"), f'sismac 1 2185 {device_info.get("factory_name")}',
         'sismac success'],
        ['校验厂家名称', device_info.get("factory_name"), 'sismac 2 2185', f'{device_info.get("factory_name")}'],
        ['写入厂家OUI', device_info.get("factory_oui"), f'sismac 1 768 {device_info.get("factory_oui")}',
         'sismac success'],
        ['校验厂家OUI', device_info.get("factory_oui"), 'sismac 2 768', f'{device_info.get("factory_oui")}'],
        ['写入IMEI', device_info.get("imei"), f'sismac 1 32777 {device_info.get("imei")}', 'sismac success'],
        ['校验IMEI', device_info.get("imei"), 'sismac 2 32777', f'{device_info.get("imei")}']]

    for operation in operation_list:
        if operation[1] is None:
            project_config['report_list'].append([operation[0], '', 'ERROR'])
            continue
        command_result = telnet.execute_command(operation[2]).replace('\r', '')
        if '\n' in command_result:
            command_result = command_result.rsplit('\n', 1)[1]
        if operation[3] in command_result:
            command_state = 'OK'
        else:
            command_state = 'NOK'
        project_config['report_list'].append([operation[0], command_result, command_state])

    for i in range(2):
        project_config['report_list'].append([np.nan, np.nan, np.nan])

    telnet.close()

    return 0
