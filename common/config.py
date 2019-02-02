# coding=utf-8
from common.constant import *

run_venv = 1
debug_mode = 1 # 正式上线请改为0。1则不会检查sid、签名等信息。

if run_venv == RUN_EVEN_TEST:
    SQL_TRACE_ENABLE = True  # sql调试模式，测试机打开
    LOG_CELERY_PATH = "/home/www/doctor/log/celery.log"
else:
    SQL_TRACE_ENABLE = False
    LOG_CELERY_PATH = "/home/www/doctor/log/celery.log"

DOC_DIR = "docs/"
DOC_TEMPLATE_DIR = "doc_templates/"

# celery 的 redis
CELERY_REDIS_BROKER_URL = "redis://127.0.0.1:6379/0"
CELERY_REDIS_BACKEND_URL = "redis://127.0.0.1:6379/0"

# SID 相关配置
SID_ENCRYPT_KEY = "MEIZIZIA"  # 加密词汇
SID_DES3_KEY = 'YUCHUNDERENLEIYAHAHAHAHA'  # des3 加密解密KEY
SID_ExpiresSeconds = 3600 * 24 * 15  # 过期时间
SID_STATUS_CORRECT = 0  # 0：正常
SID_STATUS_NO_NEED_CHECK = 1  # 1：sid不需要检查
SID_STATUS_NEED_LOGIN = 2  # 2：sid需要登录！！！
SID_STATUS_NOT_EXIST = -1  # -1: sid都没有
SID_STATUS_IRREGULAR = -2  # -2：sid不规则
SID_STATUS_LOST_EFFICACY = -3  # -3：sid失效
SID_INIT_USERID = -1  # 初始化的SID包裹的user_id = -1
SID_ERR_USERID = -2  # SID转INFO失败后，赋值user_id = -2

# 系统配置
APP_BACKEND_VERSION = "1.0"
