import hashlib
import os

import numpy as np
import pandas as pd
from git.repo import Repo


def get_file_md5(file_name):
    m = hashlib.md5()
    with open(file_name, 'rb') as file:
        while True:
            data = file.read(4096)
            if not data:
                break
            m.update(data)
    return m.hexdigest()


def get_file_list(dir_path, target_file_info=None):
    if target_file_info is None:
        target_file_info = []
    item_list = os.listdir(dir_path)
    item_list.sort()
    for item_name in item_list:
        item_path = dir_path + '/' + item_name
        if os.path.isfile(item_path) and item_name.endswith('.txt') is not True:
            item_size = os.path.getsize(item_path)
            if item_size < 1024:
                item_size_str = '{:,}'.format(item_size) + '字节'
            elif item_size < 1024 * 1024:
                item_size_str = '{:,.1f}'.format(item_size / 1024) + 'KB(' + '{:,}'.format(item_size) + '字节)'
            else:
                item_size_str = '{:,.1f}'.format(item_size / 1024 / 1024) + 'MB(' + '{:,}'.format(item_size) + '字节)'
            target_file_info.append(
                [item_name, item_size_str, get_file_md5(item_path)])

    return target_file_info


def run(project_config, option_config):
    excel_cols = ['文件名', '大小', 'MD5']
    file_list_path = f'{project_config["pack_path"]}'
    excel_path = f'{project_config["pack_path"]}/{project_config["product"]}_{project_config["chip"]}' \
                 f'_V{project_config["version"]}提测文件列表.xlsx'

    # 获取项目当前的commit的哈希值
    git_id = Repo(project_config['path']).git.log('--pretty=%H', max_count=1)

    # 遍历升级文件夹
    upgrade_rom_file = [['提测软件', np.nan, np.nan]]
    upgrade_rom_file = get_file_list(file_list_path + '/1提测软件', upgrade_rom_file)
    for i in range(3):
        upgrade_rom_file.append([np.nan, np.nan, np.nan])

    upgrade_rom_file.append(['对比软件', np.nan, np.nan])
    upgrade_rom_file = get_file_list(file_list_path + '/2对比软件', upgrade_rom_file)
    for i in range(5):
        upgrade_rom_file.append([np.nan, np.nan, np.nan])
    upgrade_rom_file.append(['内部软件版本', np.nan, project_config['version']])
    upgrade_rom_file.append(['git id', np.nan, git_id])

    excel_writer = pd.ExcelWriter(excel_path)
    pd.DataFrame(upgrade_rom_file, columns=excel_cols).to_excel(excel_writer, sheet_name='提测文件', index=False)

    excel_writer.sheets['提测文件'].set_column("A:C", 60)

    excel_writer.save()

    return 0
