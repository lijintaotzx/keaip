# Create your views here.
from django.shortcuts import render

from lib.common import merge_detail
from spider.zhuge import Zhuge


def runoob(request):
    if request.GET.get('search1') and request.GET.get('search2'):
        zhuge = Zhuge()
        detail1 = zhuge.get_detail(request.GET.get('search1'))
        detail2 = zhuge.get_detail(request.GET.get('search2'))
        context = {
            'index': False,
            'basic_data': merge_detail(detail1['basic_list'], detail2['basic_list']),
            'sales_data': merge_detail(detail1['sales_list'], detail2['sales_list']),
            'plan_data': merge_detail(detail1['plan_list'], detail2['plan_list']),
            'marching_data': merge_detail(detail1['marching_list'], detail2['marching_list']),
            'image_data': {'info1': detail1['image_url'], 'info2': detail2['image_url']},
            'introduce_data': {'info1': detail1['introduce_info'], 'info2': detail2['introduce_info']},
            'name': {'info1': detail1['name'], 'info2': detail2['name']},
        }
    else:
        context = {
            'index': True
        }
    return render(request, 'compare.html', context)
