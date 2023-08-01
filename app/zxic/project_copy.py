
from git.repo import Repo
from plugin.tool import shellrun


def run(project_config, option_config):
    repo = Repo(option_config['temp_path'])
    repo.git.checkout(project_config['git_branch'])

    repo.git.pull()

    status = shellrun(f'cp -rf {option_config["temp_path"]} {project_config["path"]}')

    return status
