import yagmail


def run(project_config, option_config):
    mail = yagmail.SMTP(user='acts_mail_system@163.com', password='GNRQIDBVMWLNFDYV', host='smtp.163.com')

    acts_report = project_config['acts_report']
    acts_report += '\t{0:{2}<10}\t{1}\n\n'.format('发送结果邮件', 'OK', chr(12288))
    acts_report += f'\n共运行{project_config["subproject_status"]["all"]}个测试，' \
                   f'其中：通过{project_config["subproject_status"]["ok"] + 1}个，' \
                   f'未通过{project_config["subproject_status"]["nok"]}个，' \
                   f'报错{project_config["subproject_status"]["error"]}个，' \
                   f'跳过{project_config["subproject_status"]["skip"]}个'

    mail_subject = f'ACTS版本提测报告：{project_config["product"]}_{project_config["version"]}'
    mail_contents = f'<html><pre>{acts_report}\n\n\n{project_config["error_log"]}</pre></html>'
    mail.send(option_config['mail'], mail_subject, mail_contents)
    return 0
