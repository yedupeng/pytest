import time

from plugin.tool import ZXICTelnetOperation, wait_until_device_power_on, shellrun
from plugin.tool import ZXICSerialOperation
from plugin.tool import SerialUpgradeThread


def run(project_config, option_config):
    boot_file_path = f'{project_config["pack_path"]}/image/{project_config["boot_name"]}'
    upgrade_file_path = f'{project_config["pack_path"]}/升级文件/{project_config["model"]}_{project_config["version"]}' \
                        f'_UPGRADE_ALL.bin'
    status = shellrun(f'cp --preserve {boot_file_path} {project_config["tftp_path"]}/uboot.bin')
    status += shellrun(f'cp --preserve {upgrade_file_path} {project_config["tftp_path"]}/upgrade.bin')

    if status != 0:
        return 1

    serial = SerialOperation(project_config['serial_port'],
                             int(project_config['serial_baud_rate']),
                             int(project_config['serial_bytesize']),
                             project_config['serial_parity'],
                             int(project_config['serial_stop_bits']))
    telnet = ZXICTelnetOperation(project_config['telnet_ip'],
                                 int(project_config['telnet_port']),
                                 project_config['telnet_username'],
                                 project_config['telnet_password'],
                                 project_config['telnet_su_password'])
    serial_upgrade_thread = SerialUpgradeThread(serial, enter_boot_times=2,
                                                output_log=f'{option_config["serial_log_path"]}/'
                                                           f'{project_config["model"]}_{project_config["version"]}'
                                                           f'_upgrade_log.txt')
    serial_upgrade_thread.setDaemon(True)
    serial_upgrade_thread.start()
    telnet.execute_command('reboot')
    telnet.close()
    time.sleep(10)
    serial.reset_buffer()
    time.sleep(5)
    serial.write('downver boot')
    time.sleep(20)
    serial.write('nand erase.chip')
    time.sleep(60)
    serial.write('downver boot')
    time.sleep(20)
    serial.write('reset')
    time.sleep(15)
    serial.write('downver version')
    time.sleep(120)
    serial.write('reset')
    time.sleep(150)
    serial_upgrade_thread.close()
    serial.close()

    return wait_until_device_power_on(project_config['telnet_ip'])
