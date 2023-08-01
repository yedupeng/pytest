import os
from plugin.tool import InterruptSystemError, shellrun


def run(project_config, option_config):
    os.chdir(project_config['path'])
    shellrun(f'echo {project_config["su_password"]} | sudo -S chmod 777 autoMake_git.sh')
    shellrun(f'echo {project_config["su_password"]} | sudo -S chmod 777 -R compatible_branch')

    command = f'docker exec {project_config["docker_name"]}' \
              f' ./{project_config["docker_path"]}/autoMake_git.sh {project_config["pon"]}'
    print(command)
    status = shellrun(f'echo {project_config["su_password"]} | sudo -S {command}')
    status += shellrun(f'echo {project_config["su_password"]} | sudo -S chmod 777 -R {project_config["pack_path"]}')

    if status.returncode != 0:
        raise InterruptSystemError('编译失败')

    return status.returncode
