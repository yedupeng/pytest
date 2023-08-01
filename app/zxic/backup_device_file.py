from plugin.tool import ZXICTelnetOperation


def backup(project_config, option_config):
    backup_list_str = ''
    telnet = ZXICTelnetOperation(project_config['telnet_ip'],
                                 int(project_config['telnet_port']),
                                 project_config['telnet_username'],
                                 project_config['telnet_password'],
                                 project_config['telnet_su_password'])

    for backup_path in option_config['backup_path']:
        backup_list_str += f' {backup_path}'
    if len(backup_list_str) < 1:
        return 0
    telnet.execute_command(f'tar zcvf {option_config["backup_file_name"]}{backup_list_str}')
    telnet.execute_command(f'tftp -p -l {option_config["backup_file_name"]} {option_config["tftp_server_ip"]}')
    telnet.close()
    return 0


def recovery(project_config, option_config):
    recovery_list_str = ''
    telnet = ZXICTelnetOperation(project_config['telnet_ip'],
                                 int(project_config['telnet_port']),
                                 project_config['telnet_username'],
                                 project_config['telnet_password'],
                                 project_config['telnet_su_password'])

    for backup_path in option_config['backup_path']:
        recovery_list_str += f' {backup_path}'
    if len(recovery_list_str) < 1:
        return 0
    telnet.execute_command(f'tftp -g -r {option_config["backup_file_name"]} {option_config["tftp_server_ip"]}')
    telnet.execute_command(f'tar xzvf {option_config["backup_file_name"]}{recovery_list_str}')
    telnet.close()
    return 0


def run(project_config, option_config):
    if option_config['type'] == 'backup':
        status = backup(project_config, option_config)
    else:
        status = recovery(project_config, option_config)
    return status
