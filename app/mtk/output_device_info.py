from general.tool import MTKTelnetOperation


def get_device_version_str(project_config):
    telnet = MTKTelnetOperation(project_config['telnet_ip'],
                                int(project_config['telnet_port']),
                                project_config['telnet_username'],
                                project_config['telnet_password'])
    command_result = telnet.execute_command('factorytool version').split('\r\n', 6)[6].replace('\r', '')
    return command_result


def get_device_version_dict(project_config):
    version_dict = {}
    telnet = MTKTelnetOperation(project_config['telnet_ip'],
                                int(project_config['telnet_port']),
                                project_config['telnet_username'],
                                project_config['telnet_password'])
    command_result = telnet.execute_command('factorytool version').split('\r\n', 6)[6].split('\r\n', 5)
    for version_str in command_result:
        version_str = version_str.split(': ', 1)
        version_dict[version_str[0].replace(' ', '_')] = version_str[1]

    return version_dict


def get_device_info_str(project_config):
    telnet = MTKTelnetOperation(project_config['telnet_ip'],
                                int(project_config['telnet_port']),
                                project_config['telnet_username'],
                                project_config['telnet_password'])
    command_result = telnet.execute_command('factorytool info').replace('\r', '')
    return command_result


def output_text(project_config, device_info):
    target_file_path = f'{project_config["compile_path"]}/{device_info}.txt'
    with open(target_file_path, 'w') as target_file:
        target_file.write(project_config[f'{device_info}_str'])


def run(project_config, option_config):
    project_config['device_version_str'] = get_device_version_str(project_config)
    project_config['device_info_str'] = get_device_info_str(project_config)

    output_text(project_config, 'device_version')
    output_text(project_config, 'device_info')

    return 0
