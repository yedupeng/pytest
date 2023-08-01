"""
@FileName：logger.py
@Description：记录日志操作工具类
@Author：Huang Junxiong
@Time：2023/6/29 上午10:45
@Department：测试组
"""
import logging
import uuid

from Config.conf import CM


class Log:

    def __init__(self):
        self.logger = logging.getLogger(str(uuid.uuid4()))
        if not self.logger.handlers:
            self.logger.setLevel(logging.DEBUG)

            # 创建一个handle写入文件
            fh = logging.FileHandler(CM.LOG_FILE, encoding='utf-8')
            fh.setLevel(logging.INFO)

            # 创建一个handle输出到控制台
            ch = logging.StreamHandler()
            ch.setLevel(logging.INFO)

            # 定义输出格式
            formatter = logging.Formatter(self.fmt)
            fh.setFormatter(formatter)
            ch.setFormatter(formatter)

            # 添加到handle
            self.logger.addHandler(fh)
            self.logger.addHandler(ch)

    @property
    def fmt(self):
        """
        日志格式化
        @return:
        """
        return '[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)d] %(message)s'


LOG = Log().logger

if __name__ == '__main__':
    print(LOG)
    LOG.info("输入文本：{}".format("text"))
