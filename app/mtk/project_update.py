import sys

from general.tool import shellrun
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


def git_clone(git_address, git_branch, clone_path):
    Repo.clone_from(url=git_address, branch=git_branch, to_path=clone_path, progress=CloneProgress())
    Repo(clone_path).git.pull()

    return 0


def run(project_config, option_config):
    git_clone('git@git.zhkj-rd.cn:enterprise_gateway/starnet.git', 'CMCC_MARKET_2023', f'{project_config["path"]}/starnet')
    git_clone('git@git.zhkj-rd.cn:enterprise_gateway/web.git', 'dev', f'{project_config["path"]}/starnet/userspace/private/apps/webpages')
    git_clone('git@git.zhkj-rd.cn:enterprise_gateway/starnet_plan.git', 'CMCC_MARKET_2023', f'{project_config["path"]}/apps/private/starnet_plan')

    return 0
