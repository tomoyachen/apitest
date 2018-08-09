#!/usr/bin/python
# -*- coding: UTF-8 -*-

import configparser
import core.log as log
import importlib,sys
importlib.reload(sys)

config = configparser.ConfigParser()
logging = log.get_logger()
# config.read("IpConfig.ini")


def get_config(filename):
    """
    获取文件配置
    :param filename: 配置文件名
    :return: None
    """
    global config
    try:
        config.read(filename, encoding="utf-8")
        return True
    except Exception as e:
        logging.error("读取配置失败 %s" % e)


def get_data(title, key):
    """
    参数配置
    :param title: 配置文件的头信息
    :param key: 配置文件的key值
    :return: 配置文件的value
    """
    try:
        value = config.get(title, key)
        return value
    except Exception as e:
        logging.error("获取参数失败 %s" % e)


def get_title_list():
    """
    获取所有title
    :return: title list
    """
    try:
        title = config.sections()
        return str(title).encode("unicode-escape")
        # return '\n'.join(title)
    except Exception as e:
        logging.error("获取title信息失败 %s", e)


