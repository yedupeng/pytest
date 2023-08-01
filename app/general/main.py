import os
import sys
import time
import traceback
import xml.etree.ElementTree as ElementTree

from tool import SerialOperation, SerialLogThread

import tool


def init_config(project_config):
    project_config['acts_report'] = ''
    project_config['error_log'] = ''
    project_config['subproject_status'] = {'all': 0, 'ok': 0, 'nok': 0, 'error': 0, 'skip': 0}
    project_config['olt_auth'] = False
    project_config['report_list'] = []
    project_config['project_name'] = f'{project_config["model"]}_{project_config["version"].replace(".", "_")}'
    project_config['path'] = f'{project_config["path"]}/{project_config["project_name"]}'
    project_config['docker_path'] = f'{project_config["docker_path"]}/{project_config["project_name"]}'
    project_config['compile_path'] = f'{project_config["path"]}/{project_config["project_name"]}_COMPILE'
    project_config['pack_path'] = f'{project_config["path"]}/{project_config["project_name"]}_OUTPUT'
    project_config['log_path'] = f'{project_config["compile_path"]}/log.txt'
    project_config['upgrade_file_path'] = f'{project_config["pack_path"]}/1提测软件'
    project_config['compare_file_path'] = f'{project_config["pack_path"]}/2对比软件'
    project_config['device_info_backup_path'] = f'{project_config["compile_path"]}/device_info.txt'
    return project_config


def add_default_config(project_config):
    config_tree = ElementTree.parse('default.xml')
    config_root = config_tree.getroot()
    default_config = tool.etree_to_dict(config_root.find('environment'))
    project_config.update(default_config)


def init_interface(project_config):
    sys.path.append(f'app')
    sys.path.append(f'cfg')
    sys.path.append(f'doc')
    sys.path.append(f'etc')

    init_config(project_config)
    sys.path.append(f'app/{project_config["execute"]}')


def guide_interface():
    print('自动化提测系统初始化中...')
    print('请选择要加载的配置文件：')
    config_list = os.listdir('cfg')
    config_list.sort()
    option_max = 0
    for index, config_file in enumerate(config_list, 1):
        print(f'{index} --- {config_file.replace(".xml", "")}')
        option_max += 1
    choose = int(input())
    if choose < 1 or choose > option_max:
        print('配置文件读取失败!')
        return 1
    config_path = f'cfg/{config_list[choose - 1]}'
    print(f'正在从 {config_path} 读取配置文件...')
    if tool.load_config(config_path) != 0:
        print('配置文件读取失败!')
        return 1
    return mode_interface(config_path)


def mode_interface(config_path):
    print('请选择模块执行的模式：')
    option_max = 3
    print(f'1 --- 默认配置')
    print(f'2 --- 全部执行')
    print(f'3 --- 自己选择')
    choose = int(input())
    if choose < 0 or choose > option_max:
        print('模式选择错误!')
        return 1

    return main_interface(choose, config_path)


def stage_interface(stage_mode, config_root):
    if stage_mode == 1:
        return 0
    elif stage_mode == 2:
        for stage in config_root.iter(tag='stage'):
            stage.attrib['enable'] = '1'
        return 0
    elif stage_mode == 3:
        print('请选择要执行的模块：')
        option_max = 0
        for index, stage in enumerate(config_root.iter(tag='stage'), 1):
            print(f'{index} --- {stage.attrib["name"]}')
            stage.attrib['enable'] = '0'
            option_max += 1
        choose_list = input()
        for choose in choose_list.split(' '):
            choose_int = int(choose)
            if choose_int < 0 or choose_int > option_max:
                continue
            for index, stage in enumerate(config_root.iter(tag='stage'), 1):
                if index == choose_int:
                    stage.attrib['enable'] = '1'
                    break
        return 0
    else:
        return 1


def start_serial_log(project_config):
    if os.path.exists(project_config['path']) is False:
        os.mkdir(project_config['path'])

    serial = SerialOperation(project_config['serial_port'],
                             int(project_config['serial_baud_rate']),
                             int(project_config['serial_bytesize']),
                             project_config['serial_parity'],
                             int(project_config['serial_stop_bits']))

    serial_log_thread = SerialLogThread(serial, f'{project_config["path"]}/serial_log.txt')
    serial_log_thread.setDaemon(True)
    serial_log_thread.start()


def main_interface(stage_mode, config_path):
    config_tree = ElementTree.parse(config_path)
    config_root = config_tree.getroot()
    if stage_interface(stage_mode, config_root) == 0:
        print('自动化提测系统初始化成功')
    else:
        return 1
    project_config = tool.etree_to_dict(config_root.find('project'))
    add_default_config(project_config)
    init_interface(project_config)
    skip_stages = False
    forever = True
    acts_start_time = time.time()
    while forever:
        # start_serial_log(project_config)
        forever = False
        for i, stage in enumerate(config_root.iter(tag='stage'), 1):
            skip_this_stage = False
            skip_subprojects = False
            project_config['acts_report'] += f'第{i}阶段：{stage.attrib["name"]}\n'
            if stage.attrib['enable'] != '1' or (skip_stages and stage.attrib["type"] != 'finally'):
                skip_this_stage = True
            if skip_this_stage:
                print(f'跳过第{i}阶段：{stage.attrib["name"]}')
                continue
            print(f'开始第{i}阶段：{stage.attrib["name"]}')
            for subproject in stage:
                skip_this_subproject = False
                if subproject.attrib['enable'] == '0' or skip_subprojects:
                    skip_this_subproject = True
                if skip_this_subproject:
                    project_config['subproject_status']['skip'] += 1
                    print(f'跳过 {subproject.attrib["name"]}')
                    project_config['acts_report'] += '\t{0:{2}<10}\t{1}\n'.format(subproject.attrib["name"], 'SKIP',
                                                                                  chr(12288))
                    continue
                project_config['subproject_status']['all'] += 1
                work_space_path = os.getcwd()
                print(f'开始 {subproject.attrib["name"]}')
                try:
                    program = __import__(subproject.tag)
                    status = program.run(project_config, tool.etree_to_dict(subproject))
                except (Exception, tool.InterruptSystemError) as e:
                    forever = False
                    project_config['subproject_status']['error'] += 1
                    print(f'出现异常 {e}')
                    traceback_log = traceback.format_exc()
                    print(traceback_log)
                    print(f'结束 {subproject.attrib["name"]}, 运行出错!!!')
                    project_config['acts_report'] += '\t{0:{2}<10}\t{1}\n'.format(subproject.attrib["name"], 'ERROR',
                                                                                  chr(12288))
                    if len(project_config['error_log']) < 1:
                        project_config['error_log'] += '报错日志\n'
                    project_config['error_log'] += f'{subproject.attrib["name"]}：{subproject.tag}.py\n'
                    project_config['error_log'] += f'{traceback_log}\n'
                    if stage.attrib["type"] == 'major' or type(e) == 'InterruptSystemError':
                        skip_stages = True
                        skip_subprojects = True
                    elif stage.attrib["type"] == 'default':
                        skip_subprojects = True
                else:
                    if status == 0:
                        project_config['subproject_status']['ok'] += 1
                        project_config['acts_report'] += '\t{0:{2}<10}\t{1}\n'.format(subproject.attrib["name"], 'OK',
                                                                                      chr(12288))
                    else:
                        project_config['subproject_status']['nok'] += 1
                        print(f'结束 {subproject.attrib["name"]}, 运行失败!')
                        project_config['acts_report'] += '\t{0:{2}<10}\t{1}\n'.format(subproject.attrib["name"], 'NOK',
                                                                                      chr(12288))
                        if stage.attrib["type"] == 'major':
                            skip_stages = True
                            skip_subprojects = True
                        elif stage.attrib["type"] == 'default':
                            skip_subprojects = True
                finally:
                    os.chdir(work_space_path)
            print(f'第{i}阶段结束')
    print('所有阶段结束，生成报告\n')
    acts_end_time = time.time()
    acts_run_time = time.gmtime(acts_end_time - acts_start_time)

    project_config['acts_report'] += \
        f'\n提测开始时间：{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(acts_start_time))}\n' \
        f'提测结束时间：{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(acts_end_time))}\n' \
        f'提测运行时间：{acts_run_time.tm_hour}小时{acts_run_time.tm_min}分钟{acts_run_time.tm_sec}秒\n'

    project_config['acts_report'] += f'\n共运行{project_config["subproject_status"]["all"]}个测试，' \
                                     f'其中：通过{project_config["subproject_status"]["ok"]}个，' \
                                     f'未通过{project_config["subproject_status"]["nok"]}个，' \
                                     f'报错{project_config["subproject_status"]["error"]}个，' \
                                     f'跳过{project_config["subproject_status"]["skip"]}个'
    print(f'{project_config["acts_report"]}\n\n')
    print('自动化提测系统运行完毕')
    return 0


if __name__ == '__main__':
    guide_interface()
