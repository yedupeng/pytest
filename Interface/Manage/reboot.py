"""
@FileName：reboot.py
@Description：重启接口：
            /api/v1/device/reboot/set
            /api/v1/scheduled/auto/reboot/get
            /api/v1/scheduled/auto/reboot/set
@Author：Huang Junxiong
@Time：2023/7/31 下午2:19
@Department：测试组
"""
from Interface.common import Common


class Reboot(Common):

    def __init__(self, device=None, driver=None):
        super().__init__()
        if not device:
            self.host = 'http://192.168.1.1'
        else:
            self.host = 'http://{}'.format(device['设备IP'])

    def reboot(self, body=None):
        url = "{}/api/v1/device/reboot/set".format(self.host)
        return self.post(url=url, body=body)