"""
@FileName：read_devices.py
@Description：读取设备信息列表文件，获取设备信息
@Author：Huang Junxiong
@Time：2023/7/21 下午3:53
@Department：测试组
"""
import configparser

import pandas as pd

from Config.conf import CM
from Utils.logger import LOG


class Devices(object):

    def __init__(self, sheet_name='Sheet1'):
        """
        读取设备列表文件，将所有设备信息保存在data中，文件路径 Data/devices.xlsx
        :param sheet_name: excel的sheet名称，默认为Sheet1
        """
        self.df = pd.read_excel(CM.DEVICES_FILE, sheet_name=sheet_name, keep_default_na=False)
        self.data = self.df.to_dict('records')

    def get(self, locator, attribute=None):
        """
        从data中过滤出指定的设备信息
        :param locator: 设备信息定位条件，提供两种方式定位：
                        1、通过设备在设备列表中顺序定位，如locator=1，则匹配设备列表中的第一台设备
                        2、通过设备信息定位，如locator='mtk'，则匹配设备列表中值包含mtk的设备
        :param attribute: 设备信息的属性值，默认为None，为None时将返回设备的所有信息；
                        如果为某个属性，如attribute='SN'，则只返回设备的SN
        :return: 返回过滤出的设备信息，默认为字典类型{attribute, value}
                如果过滤出的结果包含多台设备，则返回字典列表[{attribute, value}]
        """
        result = []
        try:
            return self.data[locator - 1][attribute]
        except KeyError:
            if attribute is None:
                return self.data[locator - 1]
            else:
                LOG.error("查询设备信息参数错误，设备参数不包含：{}".format(attribute))
                raise
        except IndexError:
            LOG.error("查询设备信息参数错误，设备列表中不存在第{}台设备".format(locator))
            raise
        except TypeError:
            for row in self.data:
                if locator in list(row.values()):
                    try:
                        result.append(row[attribute])
                    except KeyError:
                        if attribute is None:
                            result.append(row)
                        else:
                            LOG.error("查询设备信息参数错误，设备参数不包含：{}".format(attribute))
                            raise
            if len(result) == 1:
                return result[0]
            else:
                return result


DEVICES = Devices()

if __name__ == '__main__':
    a = DEVICES.get('CIOT00059680', 'SN')
    print(a)

