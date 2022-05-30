#!/usr/bin/env python
# coding:utf-8

"""
@Time : 2022/5/30 21:08 
@Author : harvey
@File : main.py
@Software: PyCharm
@Desc: 
@Module
"""

import logging

from kubernetes import client, watch

from utils.kube_util import KubeUtil
from utils.kong_util import KongUtil

logger = logging.getLogger(__name__)


def main_controller():
    logger.debug("controller start")
    kube_client = KubeUtil()
    kong_util = KongUtil(kong_url='http://localhost:30001')
    crd_api = client.CustomObjectsApi(kube_client.api_client)
    w = watch.Watch()
    for event in w.stream(crd_api.list_cluster_custom_object, group='devops.harvey.io',
                          version='v1alpha1',
                          plural='kongroutes', ):
        logger.debug(event)
        logger.debug(event['type'])
        event_type = event['type']
        route_lsit = event['object']['spec']['routeList']
        if event_type == 'ADDED':
            for data in route_lsit:
                service_name = data['serviceName']
                service_host = data['serviceHost']
                service_port = data['servicePort']
                del data['serviceName']
                del data['serviceHost']
                del data['servicePort']
                kong_util.add_service({"name":service_name,"host":service_host,"port":service_port})
                kong_util.add_route_to_service(data,service_name=service_name)
        elif event_type == 'DELETED':
            for data in route_lsit:
                service_name = data['serviceName']
                del data['serviceName']
                del data['serviceHost']
                del data['servicePort']
                kong_util.delete_route_from_service(service_name=service_name,route_name=data['name'])
        elif event_type == 'MODIFIED':
            for data in route_lsit:
                service_name = data['serviceName']
                del data['serviceName']
                del data['serviceHost']
                del data['servicePort']
                kong_util.update_route_to_service(data,service_name=service_name,route_name=data['name'])

main_controller()
