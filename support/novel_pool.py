# coding=utf-8
from myutil.config_tool import get_redis_conf
from support.db.mysql_db import DBConnection
from support.redis.redis_helper import RedisHelper

# 数据库连接
novel_conn = DBConnection(dbs_read='novel_read', dbs_write='novel_write')

# redis连接
redis_conn = RedisHelper(get_redis_conf('novel_redis_read'), get_redis_conf('novel_redis_write'))
