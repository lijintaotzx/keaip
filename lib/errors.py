# -*- coding: utf-8 -*-
"""
@Time    : 2021-08-23 23:28
@Author  : Lijintao
@FileName: errors.py
@Software: PyCharm
"""


class ParseNoneResultException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg
