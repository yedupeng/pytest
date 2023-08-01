

def file_key_value_replace(file_path, encoding, key, value):
    find_key = 0
    with open(f'{file_path}', 'r', encoding=encoding) as file:
        config_list = file.readlines()

    with open(f'{file_path}', 'w', encoding=encoding) as file:
        for item in config_list:
            if key == item.split('=')[0]:
                file.write(f'{key}={value}\n')
                find_key = 1
            else:
                file.write(item)

    return find_key


def run(project_config, option_config):
    file_key_value_replace(
        f'{project_config["path"]}/compatible_branch/make/config_cmcc/{project_config["pon"]}/version.sh',
        'utf-8', 'LOCAL_VERSION', project_config['version'])

    file_key_value_replace(f'{project_config["path"]}{option_config["boot_path"]}', 'gb2312', 'STR_UBOOT_NUMBERS',
                           project_config['boot_version'])

    with open(f'{project_config["path"]}{option_config["osgi_path"]}', 'w', encoding='gb2312') as file:
        file.write(project_config['osgi_version'])

    return 0
