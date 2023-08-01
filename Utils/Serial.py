"""
@FileName：Serial.py
@Description：串口工具类
@Author：Huang Junxiong
@Time：2023/7/17 下午3:27
@Department：测试组
"""
import atexit
import logging
import signal
import threading

import serial

from Common.read_config import CONFIG
from Config.conf import CM
from Utils.logger import LOG
from Utils.times import dt_strftime, sleep
from logging.handlers import TimedRotatingFileHandler

serial_list = []


@atexit.register
def stop_all_serial():
    """
    退出后，发送停止信号给串口日志线程
    @return:
    """
    # LOG.info('串口日志线程清理，对象数：{}'.format(len(serial_list)))
    for serial_obj in serial_list:
        if isinstance(serial_obj, Serial):
            if serial_obj.thread_keep_running:
                # LOG.info('串口日志线程清理，存在线程：{}，已设置停止位'.format(serial_obj.note))
                serial_obj.thread_keep_running = False
                sleep(3)
            else:
                pass
                # LOG.info('串口日志线程清理，线程：{}，未运行'.format(serial_obj.note))


def get_serial_logger(file_name):
    """
    根据提供的串口文件名，生成一个 logging 的 Handler，并返回该 logger，供串口记录使用
    当前日志持续写入 file_name 指定的主文件中
    :param file_name: 记录串口数据的文件名（全路径）
    :return: serial_logger Logger 对象
    """
    serial_logger = logging.getLogger(name="serial")
    serial_logger.setLevel(level=logging.INFO)
    fh = logging.FileHandler(file_name, encoding='utf-8')
    fh.setLevel(logging.INFO)
    serial_logger.addHandler(fh)
    return serial_logger


class Serial(object):

    def __init__(self, location=None):
        global serial_list
        self.location = location
        self.serial = None
        self.thread = None
        self.thread_keep_running = None
        self.write_count = 10000000000
        self.note = None
        serial_list.append(self)

    def get_and_write_to_file(self):
        """
        将串口的输出写入到文件中，文件根据规则生成，格式为：2023-07-17_194309_note.log，note为：测试用例
        该函数将运行在线程环境中
        :return:
        """
        file_name = "{}/{}_{}.log".format(CM.SERIAL_PATH, dt_strftime().replace(' ', '_'), self.note)
        serial_logger = get_serial_logger(file_name)
        if not isinstance(self.serial, serial.Serial):
            LOG.error("[串口日志线程：{}]串口对象类型异常：{}".format(self.note, type(self.serial)))
        write_count_start = 10000000000
        self.write_count = write_count_start
        LOG.info("[串口日志线程：{}]串口日志写入开始，文件{}".format(self.note, file_name))
        serial_logger.info('[串口日志线程：{}]串口日志抓取开始，时间：{}'.format(self.note, dt_strftime()))
        while self.thread_keep_running:
            output = self.serial.readline()
            if output:
                try:
                    output = output.decode()
                except UnicodeDecodeError:
                    continue
                self.write_count += 1
                file_line = '[{}][{}] {}'.format(dt_strftime(), self.write_count, output.strip())
                serial_logger.info(file_line)
            sleep(0.001)
        serial_logger.info('[串口日志线程：{}]串口日志抓取结束，时间：{}'.format(self.note, dt_strftime()))
        LOG.warning('[串口日志线程：{}]串口日志写入结束，文件关闭，写入行数：{}'.format(self.note,
                                                                                    self.write_count - write_count_start))

    def start(self, note, serial_port=None):
        """
        启动一个线程，运行串口输出写入文件的逻辑
        :param note: 串口输出文件的文件名内容，用于提示串口文件的记录原因
        :param serial_port: 串口端口号，不填默认为config.ini中的serial_port
        :return:
        """
        if not note:
            note = '未知'
        self.note = note
        if not serial_port:
            serial_port = CONFIG.get('system', 'serial_port')
        try:
            self.serial = serial.Serial(port=serial_port, baudrate=115200, timeout=10,
                                        bytesize=8, parity='N', stopbits=1)
        except Exception as e:
            if 'PermissionError' in str(e) or '拒绝访问' in str(e):
                raise KeyError(msg='打开串口，获取串口对象失败，串口拒绝访问（一般是串口被其他工具打开了，请先退出）。异常：{}' \
                               .format(e), go=False)
            raise KeyError(msg='打开串口，获取串口对象失败，异常：{}'.format(e), go=False)
        self.thread_keep_running = True
        signal.signal(signal.SIGINT, quit)
        signal.signal(signal.SIGTERM, quit)
        self.thread = threading.Thread(target=self.get_and_write_to_file)
        self.thread.setDaemon(True)
        self.thread.start()
        LOG.info('[串口日志线程：{}]串口日志线程已启动'.format(self.note))

    def stop(self):
        """
        终止串口输出写入文件的线程，通过设置一个公开的变量 thread_keep_running，控制线程中的 while 循环的退出
        :return:
        """
        if not self.thread:
            LOG.warning('[串口日志线程：{}]停止串口日志错误，串口日志未启动'.format(self.note))
            return
        LOG.info('[串口日志线程：{}]停止串口日志记录，停止中，线程存活：{}'.format(self.note, self.thread.is_alive()))
        self.thread_keep_running = False
        for i in range(5):
            if not self.thread.is_alive():
                break
            sleep(5)
        self.serial.close()
        LOG.info('[串口日志线程：{}]停止串口日志记录，完成'.format(self.note))
        sleep(2)


SERIAL = Serial()

if __name__ == '__main__':
    capture = Serial()
    capture.start(note='测试')
    sleep(5)
    capture.stop()
