"""
@FileName：capture.py
@Description：
@Author：Huang Junxiong
@Time：2023/7/13 下午5:50
@Department：测试组
"""
import logging

import dpkt.pcap
from scapy.error import Scapy_Exception
from scapy.layers.inet import IP, TCP
from scapy.sendrecv import sniff
from scapy.utils import wrpcap
import subprocess
import xml.etree.ElementTree as ET

from Common.read_config import CONFIG
from Config.conf import CM
from Utils.logger import LOG
from Utils.times import sleep, dt_strftime


class Capture(object):

    def __init__(self):
        self.process_run = None
        self.note = None
        self.start_time = None
        self.pcap_file = None

    def start(self, note='', iface='', wait_time=3):
        """
        启动抓包
        :param note: 抓包的备注信息，用于抓包文件的命名，报文命名格式：2023-07-17_105304_note.pcap
        :param iface: 需要抓包的网卡，默认为空，如果为空，则使用config.ini中配置的网卡
        :param wait_time: 抓包启动后额外的等待时间，以便抓取inform前的一些交互
        :return: 返回抓包进程对象
        """
        if self.process_run:
            LOG.warning("启动抓包，存在未清理的抓包进程，将强制终止，抓包进程信息：{}，启动时间：{}" \
                        .format(self.note, self.start_time))
            self.stop()
        if not iface:
            iface = CONFIG.get('system', 'iface')

        self.note = note
        self.start_time = dt_strftime()
        self.pcap_file = "{}/{}_{}.pcap".format(CM.CAPTURE_PATH, self.start_time.replace(' ', '_'), self.note)

        cmd = "echo {} |sudo -S  tcpdump -i {} -vv -w {}" \
            .format(CONFIG.get('system', 'sudo_password'), iface, self.pcap_file)
        self.process_run = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        LOG.info("启动抓包，接口：{}，报文：{}".format(iface, self.pcap_file))

        if wait_time:
            LOG.info("启动抓包成功，等待{}秒".format(wait_time))
            sleep(wait_time)
        return self.process_run

    def stop(self):
        """
        停止抓包进程
        :return: 如果不存在抓包进程，返回False，停止成功返回True
        """
        if not self.process_run:
            LOG.warning("停止抓包异常，不存在抓包进程")
            return False

        self.process_run.kill()
        LOG.info("停止抓包，报文：{}".format(self.pcap_file))
        return True

    def get_tcp_streams(self, packets=None):
        """
        将报文中的ack进行去重并保留原有顺序，并提取data数据存入tcp_stream中
        :param packets: 需要分析的报文，不填默认打开抓包生成的报文文件
        :return: tcp_streams字典，内容为[ack，data]
        """
        # 打开报文
        try:
            if not packets:
                packets = sniff(offline=self.pcap_file)
        except Scapy_Exception:
            LOG.error("读取报文失败，报文中不存在tcp报文，报文：{}".format(self.pcap_file))
            packets = []
            pass

        # 将报文中的ack进行去重并保留原有顺序，并提取data数据存入tcp_stream中
        # tcp_stream为字典，内容为[ack，data]
        tcp_streams = {}
        for packet in packets:
            try:
                if packet.haslayer(IP):
                    if packet.payload.haslayer(TCP):
                        # 提取ack和data
                        ack = packet.payload.payload.ack
                        data = packet.payload.payload.load.decode()
                        # 去重
                        if ack not in list(tcp_streams.keys()):
                            tcp_streams[ack] = []
                        # data存入tcp_stream[ack]中，此时data为列表形式
                        tcp_streams[ack].append(data)
            except:
                pass
        return tcp_streams

    def get_soap_msgs(self):
        """
        获取报文中的soap消息
        :return: soap消息列表
        """
        tcp_streams = self.get_tcp_streams()
        # 提取data中的soap信息，存入soap_msgs中
        # soap_msgs为列表形式
        soap_msgs = []
        for key, value in tcp_streams.items():
            # 将data转为string
            if len(value) > 0:
                value = ''.join(value)
                tcp_streams[key] = value
            # 提取soap消息，存入soap_msg中
            if '<SOAP-ENV:' in value:
                soap_msgs.append(str(value).split("\r\n\r\n")[1])
        return soap_msgs

    def get_xml_msgs(self):
        """
        从报文中提取xml消息，返回报文中所有的xml消息列表，并保持原本顺序
        :return: xml消息列表，列表中每一个元素为每条soap报文中提取出的xml信息，xml消息以字典形式存储{节点，值}
        """
        # 提取的xml消息列表，列表中一个元素对应一条soap报文中的xml信息
        xml_msgs = []

        # 获取报文中的soap信息，同样为列表，一个元素对应一条报文
        soap_msgs = self.get_soap_msgs()

        # 循环遍历每条报文
        for soap_msg in soap_msgs:
            # 获取整个xml节点
            root = ET.fromstring(soap_msg)
            # 每条报文的xml消息
            xml_msg = {}
            # 提取xml消息
            for child in root:
                for childrens in child:
                    if 'cwmp' in childrens.tag:
                        if childrens.attrib:
                            xml_msg['cwmpID'] = childrens.text
                        else:
                            xml_msg['cwmp'] = childrens.tag.split('}')[1]
                    for children in childrens:
                        xml_msg[children.tag] = children.text
                        for chi in children:
                            if 'ParameterValueStruct' in chi.tag:
                                xml_msg[chi[0].text] = chi[1].text
                            elif 'EventStruct' in chi.tag:
                                for ch in chi:
                                    if ch.tag in xml_msg.keys():
                                        xml_msg[ch.tag] = str(xml_msg[ch.tag]) + ',' + str(ch.text)
                                    else:
                                        xml_msg[ch.tag] = ch.text
                            else:
                                xml_msg[chi.tag] = chi.text
            xml_msgs.append(xml_msg)
        return xml_msgs


CAPTURE = Capture()

if __name__ == '__main__':
    CAPTURE.start("测试报文")
    sleep(5)
    CAPTURE.stop()
    print(CAPTURE.get_xml_msgs())
