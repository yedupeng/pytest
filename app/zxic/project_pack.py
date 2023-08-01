import os

from plugin.tool import shellrun


def run(project_config, option_config):
    os.chdir(f'{project_config["path"]}/Release/{project_config["pon"]}')
    status = shellrun(
        f'tar -zcvf {project_config["pon"]}_{project_config["version"]}_{project_config["product"]}.tar.gz '
        f'{project_config["model"]}_{project_config["version"]}')

    return status.returncode
