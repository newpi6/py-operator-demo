#!/usr/bin/env python
# coding:utf-8

"""
@Time : 2022/5/31 01:25 
@Author : harvey
@File : kong_api_test.py.py 
@Software: PyCharm
@Desc: 
@Module
"""

from utils.kong_util import KongUtil


kong_util = KongUtil(kong_url='http://localhost:30001')


# kong_util.delete_service_by_name('nginx-example1')
kong_util.delete_route_from_service(service_name='nginx-example1',route_name='nginx-example1')

