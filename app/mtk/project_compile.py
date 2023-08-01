import os

from general.tool import Shell


def clean_software_version(project_config):
    status = 0
    shell = Shell(project_config['log_path'])

    clean_object_list = ['cfg_ng_clean', 'libs_starnet_mtk_clean']
    for clean_object in clean_object_list:
        cmd = f'docker exec -w {project_config["docker_path"]} {project_config["docker_name"]}' \
              f' ./build.sh {project_config["pon"]} {clean_object}'
        status += shell.run(f'echo {project_config["su_password"]} | sudo -S {cmd}')

    return status


def compile_software(project_config):
    shell = Shell(project_config['log_path'])

    compile_script = f'{project_config["compile_path"]}/compile.sh'

    compile_file = open(compile_script, 'w')
    compile_file.write('#!/usr/bin/expect\n\n')
    compile_file.write('set timeout 5400\n\n')
    compile_file.write(f'spawn sudo docker exec -it {project_config["docker_name"]} bash\n')
    compile_file.write('expect "*密码*"\n')
    compile_file.write(f'send "{project_config["su_password"]}\\r"\n')
    compile_file.write('expect "*#*"\n')
    compile_file.write(f'send "cd {project_config["docker_path"]}\\r"\n')
    compile_file.write('expect "*#*"\n')
    compile_file.write(f'send "./build.sh {project_config["pon"]} All\\r"\n')
    compile_file.write('expect {\n')
    compile_file.write('    timeout {exit 0}\n')
    compile_file.write('	"*/Project/images/tclinux_allinone.sec*" {exit 0}\n')
    compile_file.write('	"*make*recipe for target \'All\' failed*" {exit -1}\n')
    compile_file.write('}\n')
    compile_file.close()
    os.chmod(compile_script, 0o777)

    status = shell.run(compile_script)
    return status


def run(project_config, option_config):
    status = 0
    status += clean_software_version(project_config)

    status += compile_software(project_config)

    if status != 0:
        print('检测到编译可能失败')
        # raise InterruptSystemError('编译失败')

    return 0
