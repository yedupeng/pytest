
from general.tool import MTKTelnetOperation


def run(project_config, option_config):
    telnet = MTKTelnetOperation(project_config['telnet_ip'],
                                int(project_config['telnet_port']),
                                project_config['telnet_username'],
                                project_config['telnet_password'])

    telnet.execute_command(f'tcapi set deviceAccount_Entry registerStatus 0')
    telnet.execute_command(f'tcapi set deviceAccount_Entry registerResult 1')
    telnet.execute_command(f'tcapi set deviceAccount_QuickRegister Active Yes')
    telnet.execute_command(f'tcapi set deviceAccount_QuickRegister Status 1')

    telnet.execute_command(f'tcapi commit deviceAccount')

    telnet.close()

    return 0
