"""
@FileName：telnet.py
@Description：telnet工具类
@Author：Huang Junxiong
@Time：2023/7/13 下午3:44
@Department：测试组
"""
import telnetlib

from Common.read_config import CONFIG
from Common.read_devices import DEVICES
from Utils.logger import LOG


class Telnet(object):

    def __init__(self):
        self.ip = None
        self.port = None
        self.user = None
        self.pwd = None
        self.chip_type = None
        self.telnet_con = telnetlib.Telnet()

    def is_connect(self, ip, port):
        """
        telnet连接
        :param ip: telnet连接的ip
        :param port: telnet连接的端口
        :return: 失败返回False，成功返回True
        """
        try:
            self.telnet_con.open(ip, port)
            LOG.info("Telnet连接成功！ip:{}, port:{}".format(ip, port))
        except:
            LOG.error("Telnet连接失败！ip:{}, port:{}".format(ip, port))
            return False
        return True

    def read_until(self, match, timeout=10):
        """
        重写read_until方法，增加结果校验
        :param match: 需要match到的字符，bytes类型
        :param timeout: 搜索超时时间
        :return: 命令执行结果，string类型
        """
        if '# ' in match.decode() or '/ #' in match.decode():
            result = self.telnet_con.read_until(match, timeout=timeout).decode('ascii')
            if result == '\r\n# ':
                result = self.telnet_con.read_until(match, timeout=timeout).decode('ascii')
        else:
            result = self.telnet_con.read_until(match, timeout=timeout).decode('ascii') \
                .replace('\r\n# ', '')
        if match.decode() not in result:
            LOG.error("Telnet执行错误，预期：{}不在实际结果：{}中".format(match.decode(), result))
            raise Exception("Telnet执行错误，预期：{}不在实际结果：{}中".format(match.decode(), result))
        elif not result:
            LOG.error("Telnet执行错误，Telnet未输出任何回显".format(match.decode(), result))
            raise Exception("Telnet执行错误，Telnet未输出任何回显".format(match.decode(), result))

        return result

    def login(self, device):
        """
        封装telnet_login，直接传入设备信息即可telnet登录
        :param device: 设备信息，字典类型
        :return: 失败返回False，成功返回True
        """
        self.ip = device['设备IP']
        self.port = device['TELNET端口']
        self.user = device['TELNET用户名']
        self.pwd = device['TELNET密码']
        self.chip_type = device['芯片方案']
        return self.telnet_login()

    def telnet_login(self, ip=None, port=None, user=None, pwd=None, chip_type=None,
                     login_show=b"Login", pwd_show=b"Password", time_out=10):
        """
        telnet登录，登录到su模式
        :param ip: telnet连接的ip
        :param port: telnet连接的端口
        :param user: telnet连接的用户名
        :param pwd: telnet连接的密码
        :param chip_type: 芯片方案
        :param login_show: 登录时用户名提示的字符串，默认为“Login”
        :param pwd_show: 登录时密码提示的字符串，默认为“Password”
        :param time_out:telnet登录超时时间
        :return:失败返回False，成功返回True
        """
        if ip and port and user and pwd and chip_type:
            self.ip = ip
            self.port = port
            self.user = user
            self.pwd = pwd
            self.chip_type = chip_type

        if self.is_connect(self.ip, self.port):
            self.read_until(login_show, timeout=time_out)
            self.telnet_con.write(self.user.encode('ascii') + b'\n')
            self.read_until(pwd_show, timeout=time_out)
            self.telnet_con.write(self.pwd.encode('ascii') + b'\n')
            if self.chip_type == "mtk":
                self.read_until(b' > ', timeout=time_out)
                self.telnet_con.write('sh'.encode('ascii') + b'\n')
                self.read_until(b'# ', timeout=time_out)
                LOG.info("Telnet登录成功！")
                return True
            elif self.chip_type == "zxic":
                a = self.read_until(b'~ $', timeout=time_out)
                self.telnet_con.write('su'.encode('ascii') + b'\n')
                a = self.read_until(pwd_show, timeout=time_out)
                self.telnet_con.write(CONFIG.get('Telnet', 'root_password').encode('ascii') + b'\n')
                a = self.read_until(b'/ #', timeout=time_out)
                LOG.info("Telnet登录成功！")
                return True
            else:
                LOG.info("Telnet登录失败，未识别的芯片方案：{}".format(self.chip_type))
                return False
        else:
            return False

    def exec_cmd(self, command, match='', time_out=10):
        """
        执行 telnet命令
        :param match: 回显中包含的字符串
        :param command: 执行的命令
        :param time_out: 执行超时时间
        :return: 命令执行结果
        """
        if not match:
            if self.chip_type == "mtk":
                match = '# '
            elif self.chip_type == "zxic":
                match = '/ #'
        self.telnet_con.write(f'{command}\n'.encode('ascii') + b'\n')
        result = self.read_until(match.encode(), timeout=time_out).replace(f'{command}\r\n', '').replace('\r\n# ', '')
        LOG.info("执行Telnet命令：{}".format(command))
        LOG.info("Telnet命令执行结果：\n{}".format(result))
        return result

    def close(self):
        """
        关闭Telnet连接
        :return:
        """
        self.telnet_con.write(b"exit\n")
        self.telnet_con.close()


TELNET = Telnet()

if __name__ == '__main__':
    TELNET.login(DEVICES.get('CIOT00059680'))
    TELNET.exec_cmd("tcapi show VoIPAdvanced")
    TELNET.exec_cmd("tcapi get VoIPAdvanced_Common Starnet_callGetMode")
    TELNET.close()
