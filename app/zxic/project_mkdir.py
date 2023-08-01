import os
import shutil
from general.tool import Shell


def run(project_config, option_config):
    if os.path.exists(project_config['compile_path']) is True:
        shutil.rmtree(project_config['compile_path'])
    os.mkdir(project_config['compile_path'])

    if os.path.exists(project_config['pack_path']) is True:
        shutil.rmtree(project_config['pack_path'])
    os.mkdir(project_config['pack_path'])

    if os.path.exists(project_config['upgrade_file_path']) is True:
        shutil.rmtree(project_config['upgrade_file_path'])
    os.mkdir(project_config['upgrade_file_path'])

    if os.path.exists(project_config['compare_file_path']) is True:
        shutil.rmtree(project_config['compare_file_path'])
    os.mkdir(project_config['compare_file_path'])

    shell = Shell(project_config['log_path'])
    shell.clean_shell_log()

    return 0
