# -*- coding: utf-8 -*-
"""
@Time    : 2021-08-19 22:28
@Author  : Lijintao
@FileName: urls.py
@Software: PyCharm
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.runoob),
]
