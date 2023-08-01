from general.tool import OPENWRTTelnetOperation


def run(project_config, option_config):
    telnet = OPENWRTTelnetOperation(project_config['telnet_ip'],
                                    int(project_config['telnet_port']),
                                    project_config['telnet_username'],
                                    project_config['telnet_password'])

    telnet.execute_command('idmanager set mac 44D1FAB80AA6')

    return 0
