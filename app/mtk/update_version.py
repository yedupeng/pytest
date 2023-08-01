

def version_replace(file_path, key, value, encoding='utf-8'):
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


def version_str_add_end(end_type, file_path, version, encoding='utf-8'):
    find_key = 0
    with open(f'{file_path}', 'r', encoding=encoding) as file:
        config_list = file.readlines()

    with open(f'{file_path}', 'w', encoding=encoding) as file:
        for item in config_list:
            target_version = item.replace('\n', '').split('=')
            if version == target_version[0]:
                file.write(f'{target_version[0]}={target_version[1]}.{end_type}\n')
                find_key = 1
            else:
                file.write(item)

    return find_key


def version_str_del_end(file_path, version, encoding='utf-8'):
    find_key = 0
    with open(f'{file_path}', 'r', encoding=encoding) as file:
        config_list = file.readlines()

    with open(f'{file_path}', 'w', encoding=encoding) as file:
        for item in config_list:
            target_version = item.replace('\n', '').split('=')
            if version == target_version[0]:
                file.write(f'{target_version[0]}={target_version[1].replace(".cmp", "").replace(".cm", "").replace(".sec", "")}\n')
                find_key = 1
            else:
                file.write(item)

    return 0


def version_all_add_end(end_type, file_path, encoding='utf-8'):
    with open(f'{file_path}', 'r', encoding=encoding) as file:
        lines = file.readlines()

    for i in range(len(lines)):
        if ('\" />' in lines[i]):
            lines[i] = lines[i].strip('\" />\n') + f'.{end_type}\" />\n'

    with open(f'{file_path}', 'w', encoding=encoding) as file:
        file.writelines(lines)

    return 0


def version_all_del_end(file_path, encoding='utf-8'):
    with open(f'{file_path}', 'r', encoding=encoding) as file:
        lines = file.readlines()

    for i in range(len(lines)):
        lines[i] = lines[i].replace(".cmp", "").replace(".cm", "").replace(".sec", "")

    with open(f'{file_path}', 'w', encoding=encoding) as file:
        file.writelines(lines)

    return 0


def version_add_end(project_config, end_type):
    version_all_add_end(end_type, f'{project_config["path"]}/Project/soft_version_make.xml')
    version_str_add_end(end_type, f'{project_config["path"]}/Project/version.make', 'DISPLAY_VERSION')
    version_str_add_end(end_type, f'{project_config["path"]}/Project/version.make', 'LOCAL_VERSION')
    version_str_add_end(end_type, f'{project_config["path"]}/Project/version.make', 'BOOT_VERSION')
    version_str_add_end(end_type, f'{project_config["path"]}/Project/version.make', 'OSGI_VERSION')


def version_del_end(project_config):
    version_all_del_end(f'{project_config["path"]}/Project/soft_version_make.xml')
    version_str_del_end(f'{project_config["path"]}/Project/version.make', 'DISPLAY_VERSION')
    version_str_del_end(f'{project_config["path"]}/Project/version.make', 'LOCAL_VERSION')
    version_str_del_end(f'{project_config["path"]}/Project/version.make', 'BOOT_VERSION')
    version_str_del_end(f'{project_config["path"]}/Project/version.make', 'OSGI_VERSION')


def run(project_config, option_config):

    version_del_end(project_config)
    version_replace(f'{project_config["path"]}/Project/version.make', 'LOCAL_VERSION', project_config['version'])

    if 'cmp' in option_config:
        version_add_end(project_config, 'cmp')

    if 'cm' in option_config:
        version_add_end(project_config, 'cm')

    if 'sec' in option_config:
        version_add_end(project_config, 'sec')

    return 0
