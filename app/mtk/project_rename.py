import os


def rename_compile_file(target_path, head_str):
    for file_name in os.listdir(target_path):
        new_file_name = f'{head_str}{file_name}'
        os.rename(os.path.join(target_path, file_name), os.path.join(target_path, new_file_name))


def run(project_config, option_config):
    f'10_23_0_30_MARKET_CMP_tclinux.bin'
    rename_compile_file(project_config['upgrade_file_path'], 
        f'{project_config["version"].replace(".", "_")}_{project_config["git_branch"].split("_")[1]}_')

    rename_compile_file(project_config['compare_file_path'], 
        f'{project_config["version"].replace(".", "_")}_{project_config["git_branch"].split("_")[1]}_CMP_')

    return 0
