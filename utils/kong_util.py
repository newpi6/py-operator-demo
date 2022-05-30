#!/usr/bin/env python
# coding:utf-8

"""
@Time : 2022/5/31 00:09 
@Author : harvey
@File : kong_util.py 
@Software: PyCharm
@Desc: 
@Module
"""
import logging

import requests

logger = logging.getLogger(__name__)


class KongUtil:
    def __init__(self, kong_url="http://kong:8001"):
        self._kong_url = kong_url

    def _request_kong(self, api: str, data: dict = None, method="get"):
        """
        :param api: kong api path, e.g.: /services
        :param data:
        :param method: get/post/delete/update
        :return:
        """
        url = f"{self._kong_url}{api}"
        headers = {"Content-Type": "application/json"}
        if method.lower() == "get":
            resp = requests.get(url=url)
        elif method.lower() == "post":
            resp = requests.post(url, headers=headers, json=data)
        elif method.lower() == "delete":
            resp = requests.delete(url)
        elif method.lower() == 'put':
            resp = requests.put(url)
        elif method.lower() == 'patch':
            resp = requests.patch(url, headers=headers, json=data)
        else:
            resp = None
        logger.debug(data)
        logger.debug(resp.json())
        return resp

    def add_service(self, data: dict):
        api = '/services'
        resp = self._request_kong(api, data, method='post')
        return resp

    def update_service(self, data: dict):
        api = '/services'
        resp = self._request_kong(api, data, method='patch')
        return resp

    def get_service_for_all(self):
        api = '/service'
        resp = self._request_kong(api, method='get')
        return resp

    def get_service_by_name(self, name):
        api = f'/services/{name}'
        resp = self._request_kong(api, method='get')
        return resp

    def delete_service_by_name(self, name):
        api = f'/services/{name}'
        resp = self._request_kong(api, method='delete')
        return resp

    def add_route_to_service(self, data: dict, service_name: str):
        api = f'/services/{service_name}/routes'
        resp = self._request_kong(api, data, method='post')
        return resp

    def update_route_to_service(self, data: dict, service_name: str, route_name:str):
        api = f'/services/{service_name}/routes/{route_name}'
        resp = self._request_kong(api, data, method='patch')
        return resp

    def delete_route_from_service(self, service_name: str, route_name: str):
        api = f'/services/{service_name}/routes/{route_name}'
        resp = self._request_kong(api, method='delete')
        return resp
