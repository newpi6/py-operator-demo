#!/usr/bin/env python
# coding:utf-8

"""
@Time : 2022/5/30 20:53 
@Author : harvey
@File : kube_util.py
@Software: PyCharm
@Desc: 
@Module
"""

import logging

import urllib3
from kubernetes import client, config
from kubernetes.config.config_exception import ConfigException

__all__ = ['KubeUtil', 'kube']

logger = logging.getLogger(__name__)


class KubeUtil:
    timeout_seconds = 2

    def __init__(self, host: str = None, token: str = None, verify_ssl=False):
        """
        :param host: apiserver
        :type host: str
        :param token: sa
        :type token: str
        """
        urllib3.disable_warnings()
        self._host = host
        self._token = token
        self._verify_ssl = verify_ssl
        self._api_client = self.__load_client()

    def __call__(self, host: str, token: str):
        self._host = host
        self._token = token
        self.__reload_client()

    def __load_client(self):
        if self._host is None or self._token is None:
            try:
                config.load_kube_config()
                conf = client.Configuration.get_default_copy()
                conf.verify_ssl = self._verify_ssl
            except ConfigException:
                conf = None
        else:
            conf = client.Configuration()
            conf.host = self._host
            conf.verify_ssl = self._verify_ssl
            conf.api_key = {"authorization": f"Bearer {self._token}"}
        return client.ApiClient(configuration=conf)

    def __reload_client(self):
        self._api_client = self.__load_client()

    @property
    def api_client(self):
        return self._api_client

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, value):
        self._token = value
        if self._host and self._token:
            self.__reload_client()

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, value):
        self._host = value
        if self._host and self._token:
            self.__reload_client()

    def list_ns(self):
        api = client.api.CoreV1Api(self._api_client)
        return api.list_namespace()

    def list_deployment(self, namespace=None):
        api = client.api.AppsV1Api(self._api_client)
        if namespace:
            return api.list_namespaced_deployment(namespace=namespace)
        return api.list_deployment_for_all_namespaces()

    def list_cluster_custom_object(self, group: str, version: str, plural: str, **kwargs):
        """
        :param group: k8s api group
        :type group:
        :param version: e.g. v1
        :type version:
        :param plural: kind 小写
        :type plural:
        :return:
        :rtype:
        """
        crd_api = client.api.CustomObjectsApi(self._api_client)
        try:
            return crd_api.list_cluster_custom_object(
                group=group,
                version=version,
                plural=plural,
                timeout_seconds=self.timeout_seconds,
                **kwargs)
        except Exception as e:
            logger.error(exc_info=e, msg="kubernetes访问异常")
            # raise errors.KubeError()

    def list_kong_route_for_all_namespace(self,
                                          group='devops.harvey.io',
                                          version='v1alpha1',
                                          plural='kongroutes',
                                          **kwargs
                                          ):
        return self.list_cluster_custom_object(group=group, version=version, plural=plural, **kwargs)

kube = KubeUtil()
# print(kube.list_ns())
# print(kube.list_deployment())
# print(kube.list_kong_route_for_all_namespace())
