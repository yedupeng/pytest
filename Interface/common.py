"""
@FileName：common.py
@Description：通用参数、通用方法封装
@Author：Huang Junxiong
@Time：2023/7/27 上午9:23
@Department：测试组
"""
import requests

from Utils.logger import LOG


class Common(object):

    token = None

    def __init__(self):
        self.headers = {
            "Content-Type": 'application/json',
            "Authorization": ""
        }

    def get(self, url, headers=None, time_out=10):
        """
        get请求封装
        :param url: 请求完整url
        :param headers: 请求头，默认为类自定的头
        :param time_out: 请求超时时间
        :return:
        """
        if not headers:
            headers = self.headers
        result = requests.get(url=url, headers=headers, timeout=time_out)
        result_json = result.json()
        if result.status_code == 200 and result_json['success'] == True:
            LOG.info('接口：{}请求成功，code：{}，reason：{}，success：{}，message：{}'
                     .format(result.url, result.status_code, result.reason,
                             result_json['success'], result_json['message']))
        else:
            LOG.error('接口：{}请求失败，code：{}，reason：{}，success：{}，message：{}'
                      .format(result.url, result.status_code, result.reason,
                              result_json['success'], result_json['message']))
        return result

    def post(self, url, headers=None, body=None, time_out=10):
        """
        post请求封装
        :param url: 请求完整url
        :param headers: 请求头，默认为类自定的头，部分请求需携带token
        :param body: 请求body
        :param time_out: 请求超时时间
        :return:
        """
        if not headers:
            self.headers['Authorization'] = self.token
            headers = self.headers
        result = requests.post(url=url, headers=headers, json=body, timeout=time_out)
        result_json = result.json()
        if result.status_code == 200 and result_json['success'] == True:
            LOG.info('接口：{}请求成功，code：{}，reason：{}，success：{}，message：{}'
                     .format(result.url, result.status_code, result.reason,
                             result_json['success'], result_json['message']))
        else:
            LOG.error('接口：{}请求失败，code：{}，reason：{}，success：{}，message：{}'
                      .format(result.url, result.status_code, result.reason,
                              result_json['success'], result_json['message']))
        return result
