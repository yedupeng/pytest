import sys

from git import RemoteProgress
from git.repo import Repo
from tqdm import tqdm


class CloneProgress(RemoteProgress):
    def __init__(self):
        super().__init__()
        self.pbar = tqdm(file=sys.stdout)

    def update(self, op_code, cur_count, max_count=None, message=''):
        self.pbar.total = max_count
        self.pbar.n = cur_count
        self.pbar.refresh()


def run(project_config, option_config):
    Repo.clone_from(url=project_config['git_address'], to_path=project_config['path'],
                    branch=project_config['git_branch'], progress=CloneProgress())
    Repo(project_config['path']).git.pull()

    return 0
