# -*- coding: utf-8 -*-
"""
@Time    : 2021-08-22 22:28
@Author  : Lijintao
@FileName: common.py
@Software: PyCharm
"""


def merge_keys(d1, d2):
    res = list(d1.keys())
    res.extend(list(d2.keys()))
    return set(res)


def merge_detail(d1, d2):
    keys = merge_keys(d1, d2)
    result = []
    for key in keys:
        key = key.replace('&nbsp;', '')
        if key == '咨询电话':
            continue
        else:
            result.append({
                'title': key,
                'info1': d1.get(key, '暂无数据'),
                'info2': d2.get(key, '暂无数据')
            })

    return result
