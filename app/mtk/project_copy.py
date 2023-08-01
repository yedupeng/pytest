from general.tool import shellrun
from git.repo import Repo


def run(project_config, option_config):
    repo = Repo(option_config['temp_path'])
    repo.git.pull()
    repo.git.checkout(project_config['git_branch'])
    repo.git.pull()

    status = shellrun(f'cd {option_config["temp_path"]} && ./codeinit.sh')

    status += shellrun(f'cp -rf {option_config["temp_path"]} {project_config["path"]}')

    return status
