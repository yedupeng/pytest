import re
import subprocess

import numpy as np
import pandas as pd
from git.repo import Repo


def get_old_git_key_str(summary, key):
    key_list = ['网关', '运营商', '地区', '产品型号', '类型', '程序', '单号', '描述', '测试', '负责人', '检视人']
    old_key_list = ['网关', '运营商', '省份', '产品', '类型', '进程', '单号', '描述', '测试', '开发者', '检视人']
    git_summary = summary
    for old_key in old_key_list:
        git_summary = git_summary.replace(f'{old_key}：', '').replace(f'{old_key}:', '')
    key_obj = re.findall(r'\[.*?]', git_summary)
    if len(key_obj) < len(key_list):
        return ''
    return key_obj[key_list.index(key)].replace('[', '').replace(']', '').replace(' ', '').upper()


def get_git_key_str(summary, key):
    key_list = ['产品型号', '程序', '类型', '单号', '运营商', '地区', '描述', '负责人', '检视人']

    if ('Merge branch' in summary):
        return ''

    key_obj = re.findall(r'\[(.*?)\]', summary)

    if key_obj[0] == '[企业网关]':
        return get_old_git_key_str(summary, key)
    if key in ['产品型号', '程序', '类型', '运营商', '地区']:
        return key_obj[key_list.index(key)].replace('[', '').replace(']', '').replace(' ', '').upper()
    else:
        for key_temp in key_obj:
            if f'{key}：' in key_temp:
                return key_temp.split('：', 1)[1].replace(']', '').replace(' ', '').upper()
        return ''


def git_summary_to_dict(git_summary_str):
    git_summary_dict = []
    key_list = ['产品型号', '程序', '类型', '单号', '运营商', '地区', '描述', '负责人', '检视人']
    for key in key_list:
        git_key_str = get_git_key_str(git_summary_str, key)
        if (len(git_key_str) > 0):
            git_summary_dict.append(git_key_str)
    return git_summary_dict


def get_version_sheet(excel_writer, project_config, start_tag, end_tag):
    git_repository_list = [project_config["path"], f'{project_config["path"]}/starnet',
                           f'{project_config["path"]}/apps/private/starnet_plan',
                           f'{project_config["path"]}/starnet/userspace/private/apps/webpages']

    git_log_list = []
    git_excel_list = []

    for git_repository in git_repository_list:
        subprocess.check_output(
            f'cd {git_repository} && git config log.date iso-strict-local', shell=True)
        git_log_str = subprocess.check_output(
            f'cd {git_repository} && git log --decorate {start_tag}..{end_tag} --format="%ad  %s"',
            shell=True).decode('utf8')
        git_log = git_log_str.split('\n')
        git_log.remove('')
        if (start_tag == ''):
            git_log = ''
        git_log_list.extend(git_log)

    git_log_list.sort(reverse=True)

    for git_item in git_log_list:
        if 'Merge branch' in git_item:
            break;
        git_dict = git_summary_to_dict(git_item)
        git_excel_list.append(git_dict)

    if end_tag == '':
        end_tag = f'V{project_config["version"]}'
    version_sheet = f'{end_tag}'
    excel_cols = ['产品型号', '程序', '类型', '单号', '运营商', '地区', '描述', '负责人', '检视人']
    pd.DataFrame(git_excel_list, columns=excel_cols).to_excel(excel_writer, sheet_name=version_sheet, index=False)

    excel_writer.sheets[version_sheet].set_column("A:B", 8)
    excel_writer.sheets[version_sheet].set_column("B:C", 20)
    excel_writer.sheets[version_sheet].set_column("C:G", 8)
    excel_writer.sheets[version_sheet].set_column("G:H", 100)
    excel_writer.sheets[version_sheet].set_column("H:I", 8)


def run(project_config, option_config):
    git_tag_str = subprocess.check_output(
        f'cd {project_config["path"]} && git tag --sort=taggerdate', shell=True).decode('utf8')

    git_tag_temp_list = git_tag_str.split('\n')
    git_tag_list = []
    for tag in git_tag_temp_list:
        if option_config['version'].replace('x', '') in tag:
            git_tag_list.append(tag)
    git_tag_list.append('')

    excel_path = f'{project_config["pack_path"]}/{project_config["product"]}_{project_config["chip"]}' \
                 f'_V{project_config["version"]}版本历史说明.xlsx'

    excel_writer = pd.ExcelWriter(excel_path)

    for i in range(len(git_tag_list) - 1, -1, -1):
        get_version_sheet(excel_writer, project_config, git_tag_list[i - 1], git_tag_list[i])

    excel_writer.save()

    return 0
