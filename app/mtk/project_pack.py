import os
import shutil

from general.tool import Shell


def pack_compile_file(project_config, target_path):
    status = 0

    for pack_file in os.listdir(f'{project_config["path"]}/Project/images/'):
        target_file = f'{project_config["path"]}/Project/images/{pack_file}'
        if os.path.exists(target_file) is True:
            shutil.copy(target_file, target_path)
        else:
            status += 1

    return status


def pack_compile_sec_file(project_config, target_path):
    status = 0

    for pack_file in os.listdir(f'{project_config["path"]}/Project/images/'):
        target_file = f'{project_config["path"]}/Project/images/{pack_file}'
        if '.sec' in pack_file and os.path.exists(target_file) is True:
            shutil.copy(target_file, target_path)

    return status


def md5_compile_file(project_config, target_path):
    status = 0
    shell = Shell(project_config['log_path'])

    shell.run(f'cd {target_path} && md5sum * > MD5.txt')

    return status


def run(project_config, option_config):
    status = 0
    if 'cmp' in option_config:
        target_path = project_config['compare_file_path']
        status += pack_compile_file(project_config, target_path)
    elif 'sec' in option_config:
        target_path = project_config['upgrade_file_path']
        status += pack_compile_sec_file(project_config, target_path)

    else:
        target_path = project_config['upgrade_file_path']
        status += pack_compile_file(project_config, target_path)

    status += md5_compile_file(project_config, target_path)

    return status
