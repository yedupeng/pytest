"""
@FileName：wan.py
@Description：/api/v1/network/wan接口相关操作：
                /api/v1/network/wan/add
                /api/v1/network/wan/mod
                /api/v1/network/wan/del
                /api/v1/network/wan/list/get
@Author：Huang Junxiong
@Time：2023/7/26 下午3:11
@Department：测试组
"""
import json

import requests

from Common.read_devices import DEVICES
from Interface.common import Common
from Utils.logger import LOG
from conftest import driver


class Wan(Common):

    def __init__(self, device=None, driver=None):
        super().__init__()
        if not device:
            self.host = 'http://192.168.1.1'
        else:
            self.host = 'http://{}'.format(device['设备IP'])

    def get_wan_list(self):
        url = "{}/api/v1/network/wan/list/get".format(self.host)
        return self.get(url=url)

    def add_wan(self, body=None):
        url = "{}/api/v1/network/wan/add".format(self.host)
        return self.post(url=url, body=body)


if __name__ == '__main__':
    WAN = Wan(DEVICES.get('CIOT00059680'))
    print(WAN.get_wan_list())
