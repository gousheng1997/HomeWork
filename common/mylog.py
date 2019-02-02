# coding=utf-8
import logging
import os

from logging.config import fileConfig

# 导入配置
cur_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
logger_conf_path = os.path.join(cur_dir, './conf/logger.conf')
fileConfig(logger_conf_path)

# 全局logger
logger = logging.getLogger("novelLogger")
