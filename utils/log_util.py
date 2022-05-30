#!/usr/bin/env python
# coding:utf-8

"""
@Time : 2022/5/30 21:27 
@Author : harvey
@File : log_util.py 
@Software: PyCharm
@Desc: 
@Module
"""

import logging.config

__all__ = ['set_log']

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "datefmt": "%Y-%m-%d %H:%M:%S%z",
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"
        },
        "main": {
            "datefmt": "%Y-%m-%dT%H:%M:%S%z",
            "format": "[%(asctime)s.%(msecs)d] [%(levelname)s] [%(name)s] [%(module)s:%(lineno)d] [%(processName)s] [%(threadName)s]  %(message)s",
            "style": "%"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "main"
        }
    },
    "loggers": {
        "": {
            "handlers": [
                "console"
            ],
            "propagate": False,
            "level": "DEBUG"
        }
    }
}


def init_log():
    logging.config.dictConfig(LOGGING)


set_log = init_log()
