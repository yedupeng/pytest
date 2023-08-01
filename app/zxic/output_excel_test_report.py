import pandas as pd


def run(project_config, option_config):
    report_excel_path = f'{project_config["pack_path"]}/{project_config["product"]}_{project_config["chip"]}' \
                        f'_V{project_config["version"]}测试报告.xlsx'

    excel_writer = pd.ExcelWriter(report_excel_path)
    excel_cols = ['测试项', '设备返回信息', '测试结果']
    pd.DataFrame(project_config['report_list'], columns=excel_cols).to_excel(excel_writer, sheet_name='Sheet1',
                                                                             index=False)
    excel_writer.sheets['Sheet1'].set_column("A:B", 30)
    excel_writer.sheets['Sheet1'].set_column("B:C", 80)
    excel_writer.sheets['Sheet1'].set_column("C:D", 15)
    excel_writer.save()

    return 0
