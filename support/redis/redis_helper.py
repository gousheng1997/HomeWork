# coding: utf8
import redis

from common.mylog import logger

CONN_CHECK_INTERVAL = 60  # 连接检测间隔(秒)


class RedisHelper(object):
    rcfg_2_pool = {}

    def __init__(self, r_cfg=None, w_cfg=None):
        self.read_cfg = r_cfg
        self.write_cfg = w_cfg
        self.r = redis.StrictRedis(connection_pool=self._get_pool(self.read_cfg))
        self.w = redis.StrictRedis(connection_pool=self._get_pool(self.write_cfg))
        self.is_r_working = False
        self.is_w_working = False
        self.validate_conn()  # 判断其实连接状态

    def _get_pool(self, redis_cfg):
        conn_key = "%s:%s#%s" % (redis_cfg.get('host'), redis_cfg.get('port'), redis_cfg.get('db', 0))
        print ">>>>> redis get pool, conn_key", conn_key
        cur_pool = self.__class__.rcfg_2_pool.get(conn_key, None)
        if cur_pool:
            logger.info("got redis connection_pool by %s!", conn_key)
            return cur_pool

        cur_pool = redis.ConnectionPool(host=redis_cfg.get('host'), port=redis_cfg.get('port'),
                                        db=redis_cfg.get('db', 0))
        self.__class__.rcfg_2_pool[conn_key] = cur_pool
        logger.info("create redis connection_pool for %s.", conn_key)
        print ">>>>> create redis connection_pool for", conn_key
        return cur_pool

    def readable(self):
        return self.is_r_working

    def writeable(self):
        return self.is_w_working

    def validate_conn(self):
        try:
            r_connecting = self.r.ping()
            self.is_r_working = r_connecting
        except Exception, ex:
            self.is_r_working = False
            logger.error("redis r connect error:%s", str(ex))
        try:
            w_connecting = self.w.ping()
            self.is_w_working = w_connecting
        except Exception, ex:
            self.is_w_working = False
            logger.error("redis w connect error:%s", str(ex))
        logger.info("redis read conn:%s, redis write conn:%s", self.is_r_working, self.is_w_working)

    def check_r_conn(self):
        try:
            r_connecting = self.r.ping()
            self.is_r_working = r_connecting
        except Exception, ex:
            self.is_r_working = False
            logger.error("redis r connect error:%s", str(ex))

    def expire(self, name, t):
        try:
            return self.w.expire(name, t)
        except Exception, ex:
            self.is_w_working = False
            logger.error("redis w connect error:%s", str(ex))

    def get(self, key):
        try:
            ret_v = self.r.get(key)
            return ret_v
        except Exception, ex:
            self.is_r_working = False
            logger.error("redis r connect error:%s", str(ex))

    def set(self, key, value, ex=None, px=None, nx=False, xx=False):
        try:
            return self.w.set(key, value, ex, px, nx, xx)
        except Exception, ex:
            self.is_w_working = False
            logger.error("redis w connect error:%s", str(ex))

    def scan_iter(self, match=None, count=None):
        try:
            return self.r.scan_iter(match, count)
        except Exception, ex:
            self.is_r_working = False
            logger.error("redis r connect error:%s", str(ex))
            return None

    def exists(self, name):
        try:
            return self.r.exists(name)
        except Exception, ex:
            logger.error(ex, exc_info=1)
            self.is_w_working = False
            return None

    def keys(self, pattern='*'):
        try:
            return self.r.keys(pattern)
        except Exception, ex:
            logger.error(ex, exc_info=1)
            self.is_w_working = False
            return None

    def setex(self, key, timeout_secs, value):
        try:
            self.w.setex(key, timeout_secs, value)
        except Exception, ex:
            self.is_w_working = False
            logger.error("redis w connect error:%s", str(ex))

    def hexists(self, name, key):
        "Returns a boolean indicating if ``key`` exists within hash ``name``"
        try:
            return self.r.hexists(name, key)
        except Exception, ex:
            logger.error(ex, exc_info=1)
            self.is_w_working = False
            return None

    def hget(self, key, fd):
        try:
            return self.r.hget(key, fd)
        except Exception, ex:
            self.is_r_working = False
            logger.error("redis r connect error:%s", str(ex))

    def hgetall(self, key):
        try:
            return self.r.hgetall(key)
        except Exception, ex:
            self.is_r_working = False
            logger.error("redis r connect error:%s", str(ex))

    def hset(self, key, fd, v):
        try:
            return self.w.hset(key, fd, v)
        except Exception, ex:
            self.is_w_working = False
            logger.error("redis w connect error:%s", str(ex))

    def hincrby(self, key, fd, v):
        try:
            return self.w.hincrby(key, fd, v)
        except Exception, ex:
            self.is_w_working = False
            logger.error("redis w connect error:%s", str(ex))

    def hmset(self, key, data_dict):
        try:
            return self.w.hmset(key, data_dict)
        except Exception, ex:
            self.is_w_working = False
            logger.error("redis w connect error:%s", str(ex))

    def pttl(self, key):
        try:
            return self.r.pttl(key)
        except Exception, ex:
            self.is_r_working = False
            logger.error("redis r connect error:%s", str(ex))

    def incr(self, key):
        try:
            return self.w.incr(key)
        except Exception, ex:
            self.is_w_working = False
            logger.error("redis w connect error:%s", str(ex))

    def delete(self, key):
        try:
            return self.w.delete(key)
        except Exception, ex:
            self.is_w_working = False
            logger.error("redis w connect error:%s", str(ex))

    def lpush(self, lst_key, v):
        try:
            return self.w.lpush(lst_key, v)
        except Exception, ex:
            self.is_w_working = False
            logger.error("redis w connect error:%s", str(ex))

    def lpop(self, lst_key):
        try:
            return self.w.lpop(lst_key)
        except Exception, ex:
            self.is_w_working = False
            logger.error("redis w connect error:%s", str(ex))

    def rpush(self, lst_key, v):
        try:
            return self.w.rpush(lst_key, v)
        except Exception, ex:
            self.is_w_working = False
            logger.error("redis w connect error:%s", str(ex))

    def rpop(self, lst_key):
        try:
            return self.w.rpop(lst_key)
        except Exception, ex:
            self.is_w_working = False
            logger.error("redis w connect error:%s", str(ex))
