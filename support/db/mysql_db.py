# coding=utf-8
import pymysql

from common import config
from common import constant
from common import mylog
from myutil import config_tool

logger = mylog.logger


class DBConnection(object):
    def __init__(self, dbs_read, dbs_write=None):
        print "will create db instance, callstack:>>>>>>>>>", dbs_read, dbs_write

        self.db_source_read = dbs_read
        self.db_source_write = dbs_write
        self.cf_read = config_tool.get_db_conf(self.db_source_read)
        self.cf_write = config_tool.get_db_conf(self.db_source_write)

        try:  # 读连接
            self.conn_read = pymysql.connect(host=self.cf_read['host'],
                                             user=self.cf_read['user'],
                                             password=self.cf_read['password'],
                                             db=self.cf_read["db"],
                                             charset=self.cf_read['charset'],
                                             cursorclass=pymysql.cursors.DictCursor,
                                             autocommit=True
                                             )
        except pymysql.DataError, ex:
            logger.error(ex, exc_info=1)
            self.conn_read = None
            logger.error("connect db conn_read(%s) Error %d: %s", str(self.cf_read), ex.args[0], ex.args[1])
            raise Exception("DBConnection init failed because of read conn.")

        try:  # 同步写连接
            self.conn_write = pymysql.connect(host=self.cf_write['host'],
                                              user=self.cf_write['user'],
                                              password=self.cf_write['password'],
                                              db=self.cf_write["db"],
                                              charset=self.cf_write['charset'],
                                              cursorclass=pymysql.cursors.DictCursor,
                                              autocommit=True
                                              )

        except pymysql.DataError, ex:
            logger.error(ex, exc_info=1)
            self.conn_write = None
            if self.conn_read:  # 注意释放读连接
                self.conn_read.close()
            logger.error("connect db conn_write(%s) Error %d: %s", str(self.cf_write), ex.args[0], ex.args[1])
            raise Exception("DBConnection init failed  because of write conn.")

        print "create db instance ok....."

    def __del__(self):
        if self.conn_read is not None:
            self.conn_read.close()
            self.conn_read = None
        if self.conn_write is not None:
            self.conn_write.close()
            self.conn_write = None

    def reconnect_db(self, _type):
        """
        重新连接db
        :param _type:
        :return:
        """
        if _type != constant.CONN_READ and _type != constant.CONN_WRITE:
            return False
        if _type == constant.CONN_READ:
            try:
                if self.conn_read is not None:
                    self.conn_read.close()
                self.conn_read = pymysql.connect(host=self.cf_read['host'],
                                                 user=self.cf_read['user'],
                                                 password=self.cf_read['password'],
                                                 db=self.cf_read["db"],
                                                 charset=self.cf_read['charset'],
                                                 cursorclass=pymysql.cursors.DictCursor,
                                                 autocommit=True
                                                 )
            except pymysql.DataError, e:
                logger.error("reconnect db conn_read(%s) Error %d: %s", str(self.cf_read), e.args[0], e.args[1])
                self.conn_read = None
            return self.conn_read is not None
        elif _type == constant.CONN_WRITE:
            try:
                if self.conn_write is not None:
                    self.conn_write.close()
                self.conn_write = pymysql.connect(host=self.cf_write['host'],
                                                  user=self.cf_write['user'],
                                                  password=self.cf_write['password'],
                                                  db=self.cf_write["db"],
                                                  charset=self.cf_write['charset'],
                                                  cursorclass=pymysql.cursors.DictCursor,
                                                  autocommit=True
                                                  )
            except pymysql.DataError, e:
                logger.error("reconnect db conn_write(%s) Error %d: %s", str(self.cf_write), e.args[0], e.args[1])
                self.conn_write = None
            return self.conn_write is not None

    def is_connect_living(self, _type):
        """
        判断连接是否存活...
        :param _type:
        :return:
        """
        try:
            if _type == constant.CONN_READ:
                self.conn_read.ping(True)
                return True
            elif _type == constant.CONN_WRITE:
                self.conn_write.ping(True)
                return True
            else:
                return False
        except Exception, ex:
            logger.error(ex, exc_info=1)
            logger.error("is_connect_living judge failed. _type:%s" % _type)
            return False

    def fetchone(self, sql, *args):
        """
        只返回一个数据item

        遇到异常：
            我们先抓住异常后，关掉游标和释放锁，然后再raise，最终不hold住异常
        :param sql:
        :param args:
        :return:
        """
        if sql.split()[0].upper() not in ("SELECT", "SHOW", "EXPLAIN", "DESC"):
            logger.error(
                'only <select> can be called function query(), statement <update> need call function exec_sql()')
            raise Exception(
                'only <select> can be called function query(), statement <update> need call function exec_sql()')

        cursor = None
        try:
            conn_available = True
            sql_result = None
            if not self.is_connect_living(constant.CONN_READ):
                logger.error("[db_source_read:%s] connect gone away, try to reconnect.", self.db_source_read)
                conn_available = self.reconnect_db(constant.CONN_READ)
            if conn_available:
                if config.SQL_TRACE_ENABLE:
                    logger.debug(sql)

                cursor = self.conn_read.cursor()
                cursor.execute(sql, args)
                items = cursor.fetchall()
                if items:
                    sql_result = items[0]
            return sql_result
        except Exception, e:
            logger.error("[db_source_read:%s] query sql(%s) error:%s", self.db_source_read, str(sql), str(e))
            raise e
        finally:
            if cursor:
                cursor.close()

    def fetchall(self, sql, *args):
        """
        返回一个列表

        遇到异常：
            我们先抓住异常，关掉游标和释放锁，然后再raise，最终不hold住异常
        :param sql:
        :param args:
        :return:
        """
        if sql.split()[0].upper() not in ("SELECT", "SHOW", "EXPLAIN", "DESC"):
            logger.error(
                'only <select> can be called function query(), statement <update> need call function exec_sql()')
            raise Exception(
                'only <select> can be called function query(), statement <update> need call function exec_sql()')

        cursor = None
        try:
            sql_result = []
            conn_available = True
            if not self.is_connect_living(constant.CONN_READ):
                logger.error("[db_source_read:%s] connect gone away, try to reconnect.", self.db_source_read)
                conn_available = self.reconnect_db(constant.CONN_READ)
            if conn_available:
                if config.SQL_TRACE_ENABLE:
                    logger.debug(sql)

                cursor = self.conn_read.cursor()
                cursor.execute(sql, args)
                sql_result = cursor.fetchall()
                sql_result = list(sql_result)
            return sql_result
        except Exception, e:
            logger.error("[db_source_read:%s] query sql(%s) error:%s", self.db_source_read, str(sql), str(e))
            raise e
        finally:
            if cursor:
                cursor.close()

    def execute_sql(self, sql):
        """
        执行一条sql： insert、update、delete
        :param sql:
        :return:
        """
        cursor = None
        result = None
        conn_available = True
        try:
            if not self.is_connect_living(constant.CONN_WRITE):
                logger.error("[db_source_write:%s] connect gone away, try to reconnect", self.db_source_write)
                conn_available = self.reconnect_db(constant.CONN_WRITE)
            if conn_available:
                if config.SQL_TRACE_ENABLE:
                    logger.debug(sql)

                cursor = self.conn_write.cursor()
                cursor.execute(sql)

                if 'update' in sql or 'delete' in sql:  # 如果是单条update，则获取影响的行数
                    result = cursor.rowcount
                elif "insert" in sql:  # 否则，获取最后一次插入的id
                    sql_last_id = "select last_insert_id() as id"
                    cursor.execute(sql_last_id)
                    last_id_result = cursor.fetchall()
                    if len(last_id_result) > 0:
                        result = last_id_result[0]['id']
        except Exception, ex:
            logger.error("sql=%s" % sql)
            logger.error("[db_source_write:%s] exectue error: %s !" % (self.db_source_write, ex), exc_info=1)
            raise
        finally:
            if cursor is not None:
                cursor.close()
        return result

    def raw_execute_sql(self, sql):
        """
        执行一条sql： insert、update、delete
        :param sql:
        :return:
        """
        cursor = None
        result = None
        conn_available = True
        try:
            if not self.is_connect_living(constant.CONN_WRITE):
                logger.error("[db_source_write:%s] connect gone away, try to reconnect", self.db_source_write)
                conn_available = self.reconnect_db(constant.CONN_WRITE)
            if conn_available:
                if config.SQL_TRACE_ENABLE:
                    logger.debug(sql)

                cursor = self.conn_write.cursor()
                res = cursor.execute(sql)
                return res
        except Exception, ex:
            logger.error("sql=%s" % sql)
            logger.error("[db_source_write:%s] exectue error: %s !" % (self.db_source_write, ex), exc_info=1)
            raise
        finally:
            if cursor is not None:
                cursor.close()
        return result
