# -*- coding: utf-8 -*-
"""
@Time    : 2021-08-23 23:28
@Author  : Lijintao
@FileName: zhuge.py
@Software: PyCharm
"""
import re

import requests

from lib.errors import ParseNoneResultException


class Zhuge:
    def __init__(self):
        self.search_url = 'https://bj.xinfang.zhuge.com/v_{}_/'
        self.detail_url_regex = '<ul class="list_ul">.*?<a class="ellipsis house_title" href="(.*?)".*?</a>.*?ul>'
        self.detail_image_regex = '<ul class="list_ul">.*?<img class="loupan_img lazy".*?data-src="(.*?)".*?</ul>'
        self.detail_data_regex = '<div class="detail_modular">.*?"modular_name">{}</p.*?<ul class="modular_ul clearfix">(.*?)</ul.*?/div>'
        self.li_info_regex = '<li class="modular_li.*?li_name">(.*?)：</i>.*?li_text ellipsis">(.*?)<.*?/li>'
        self.marching_info_regex = '<i class="fl li_name">(.*?)：</i>.*?li_text">(.*?)</div.*?/li>'
        self.introduce_info_regex = '<div class="detail_modular">.*?class="modular_name">楼盘项目介绍<.*?class="project">(.*?)</div>'
        self.detail_name_regex = '<b class="fl">(.*?)</b>'
        self.search_html = ''

    def get_cookie(self, arg1):
        arg1 = arg1
        _0x20a7bf = 0
        _0x4b082b = [15, 35, 29, 24, 33, 16, 1, 38, 10, 9, 19, 31, 40, 27, 22, 23, 25, 13, 6, 11, 39, 18, 20, 8, 14, 21,
                     32,
                     26, 2, 30, 7, 4, 17, 5, 3, 28, 34, 37, 12, 36]
        _0x4da0dc = ['', '', '', '', '', '', '4', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                     '',
                     '', '', '', '', 'A', '', '', '', '', '', '', 'F', '', '', '', '', '', '']
        _0x12605e = ""
        while _0x20a7bf < len(arg1):

            _0x385ee3 = arg1[_0x20a7bf]
            _0x217721 = 0
            while _0x217721 < len(_0x4b082b):
                if _0x4b082b[_0x217721] == _0x20a7bf + 1:
                    _0x4da0dc[_0x217721] = _0x385ee3
                _0x217721 += 1
            _0x20a7bf += 1

        _0x12605e = "".join(_0x4da0dc)
        _0x23a392 = _0x12605e
        _0x4e08d8 = "3000176000856006061501533003690027800375"
        _0x5a5d3b = ""
        _0xe89588 = 0
        while _0xe89588 < len(_0x23a392) and _0xe89588 < len(_0x4e08d8):
            _0x401af1 = int(_0x23a392[_0xe89588:_0xe89588 + 2], 16)
            _0x105f59 = int(_0x4e08d8[_0xe89588:_0xe89588 + 2], 16)
            _0x189e2c = hex((_0x401af1 ^ _0x105f59))
            if len(_0x189e2c) == 3:
                _0x189e2c = "0" + _0x189e2c
            _0x5a5d3b += _0x189e2c
            _0xe89588 += 2
        return _0x5a5d3b.replace('0x', '')

    def get_html(self, url):
        # time.sleep(random.randint(1, 2))
        request = requests.Session()
        resp = request.get(url).text
        arg1 = re.findall('arg1\s*?=\s*?[\"\'](\S*?)[\"\']', resp)[0]
        headers = {
            'cookie': 'acw_sc__v2=' + self.get_cookie(arg1) + ';',
            'Host': 'bj.xinfang.zhuge.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
        }
        html = request.get(url, headers=headers).text
        return html

    def parse_html(self, regex, html):
        pattern = re.compile(regex, re.S)
        result = pattern.findall(html)
        if not len(result):
            raise ParseNoneResultException('Find no result with :{}'.format(regex))
        else:
            return result

    def get_detail_url(self, url):
        html = self.get_html(url)
        self.search_html = html
        search_result = self.parse_html(self.detail_url_regex, html)
        print(search_result)
        if not len(search_result):
            return False
        else:
            return 'https:{}{}/'.format(search_result[0], 'loupanxiangqing')

    def get_li_info(self, detail_html, info):
        info_data = self.parse_html(
            self.detail_data_regex.format(info),
            detail_html
        )
        li_list = self.parse_html(self.li_info_regex, info_data[0])
        return li_list

    def parse_detail_data(self, detail_html):
        basic_list = self.get_li_info(detail_html, '楼盘基本信息')
        sales_list = self.get_li_info(detail_html, '楼盘销售信息')
        plan_list = self.get_li_info(detail_html, '楼盘小区规划')
        marching_info = self.parse_html(
            self.detail_data_regex.format('楼盘周边配套'),
            detail_html
        )
        introduce_info = self.parse_html(self.introduce_info_regex, detail_html)
        name = self.parse_html(self.detail_name_regex, detail_html)
        image_url = self.parse_html(self.detail_image_regex, self.search_html)
        marching_list = self.parse_html(self.marching_info_regex, marching_info[0])
        assert self.search_html != ''
        result = {
            'basic_list': dict(basic_list),
            'sales_list': dict(sales_list),
            'plan_list': dict(plan_list),
            'marching_list': dict(marching_list),
            'introduce_info': introduce_info[0],
            'image_url': image_url[0],
            'name': name[0]
        }
        self.search_html = ''
        return result

    def get_detail(self, name):
        search_url = self.search_url.format(requests.utils.quote(name))
        detail_url = self.get_detail_url(search_url)
        detail_html = self.get_html(detail_url)
        return self.parse_detail_data(detail_html)
