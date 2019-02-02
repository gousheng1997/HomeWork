# coding=utf-8
import hashlib
import logging
import time
from datetime import date, datetime


def str_to_int(value, default=0):
    """
    强制类型转换 str -> int
    :param value:
    :param default:
    :return:
    """
    try:
        value = int(value)
    except TypeError, ex:
        value = default
    return value


def getCurrentTimestamp(bit_type=13):
    """
    :param bit_type: bit_type=10. 10位时间戳，bit_type=13，13位时间戳
    返回时间戳，python是10位.3位，这里为了和终端保持一致统一13位
    :return: -1 表示错误
    """
    if bit_type == 13:
        return int(round(time.time() * 1000))
    elif bit_type == 10:
        return int(round(time.time()))
    return -1


def getTimestrFromTimestamp(timestamp, fmt="%Y-%m-%d %H:%M:%S", bit_type=13):
    """
    时间戳 -> 时间字符串
    若bit_type==13, 先变成10位时间戳，再转...
    :param timestamp:
    :param fmt:
    :return: '' 表示错误
    """
    if bit_type == 13:
        x = time.localtime(timestamp / 1000)
        return time.strftime(fmt, x)
    elif bit_type == 10:
        x = time.localtime(timestamp)
        return time.strftime(fmt, x)
    return ''


def getDeltaSeconds(datetime1, datetime2):
    """
    获取两个datetime之间的时间间隔seconds
    :param datetime1:
    :param datetime2:
    :return:
    """
    a = datetime2 - datetime1
    return abs(a.days * 24 * 60 * 60 + a.seconds)


def datetime2timestamp(obj, format="%Y-%m-%d %H:%M:%S", bit_type=13):
    '''
    :param obj: 类似'2016-09-01 09:57:54'
    :param format:类似"%Y-%m-%d %H:%M:%S"
    :param bit_type: bit_type=10. 10位时间戳，bit_type=13，13位时间戳
    :return:返回13位的时间戳, -1 表示失败
    '''
    if isinstance(obj, str):
        _datetime = datetime.strptime(obj, format)
        ts = time.mktime(_datetime.timetuple())
        if bit_type == 13:
            return int(ts * 1000)
        elif bit_type == 10:
            return int(ts)
    elif isinstance(obj, datetime):
        ts = time.mktime(obj.timetuple())
        if bit_type == 13:
            return int(ts * 1000)
        elif bit_type == 10:
            return int(ts)
    return -1


def timestamp2datetime(timestamp, format="%Y-%m-%d %H:%M:%S", bit_type=13):
    '''
    根据时间戳返回时间, 和客户端约定13ms
    localtime(seconds) .. 传入的要是秒...
    '''
    if bit_type == 13:
        ltime = time.localtime(timestamp / 1000)
        timeStr = time.strftime(format, ltime)
        return timeStr, ltime
    elif bit_type == 10:
        ltime = time.localtime(timestamp)
        timeStr = time.strftime(format, ltime)
        return timeStr, ltime


def str2datetime(time_str, format="%Y-%m-%d %H:%M:%S"):
    """
    time_str = "2017-10-11 12:01:00"
    :param time_str:
    :return:
    """
    t = time.strptime(time_str, format)
    dt = datetime(*t[:6])
    return dt


def getTimeOClockOfToday(timestamp, bit_type=13):
    """
    获取某个时间戳的0点的时间戳
    :param timestamp:
    :param bit_type:
    :return:
    """
    import time
    if bit_type == 13:
        t = time.localtime(timestamp / 1000)
        time1 = time.mktime(time.strptime(time.strftime('%Y-%m-%d 00:00:00', t), '%Y-%m-%d %H:%M:%S'))
        return long(time1)
    elif bit_type == 10:
        t = time.localtime(timestamp)
        time1 = time.mktime(time.strptime(time.strftime('%Y-%m-%d 00:00:00', t), '%Y-%m-%d %H:%M:%S'))
        return long(time1)
    return -1


def phone_check(s):
    """
    不检查前缀了....鬼知道运营商加了什么字段
    :param s:
    :return:
    """
    # 号码前缀，如果运营商启用新的号段，只需要在此列表将新的号段加上即可。
    phoneprefix = ['130', '131', '132', '133', '134', '135', '136', '137', '138', '139', \
                   '150', '151', '152', '153', '155', '156', '158', '159', '170', '183', '182', \
                   '185', '186', '188', '189']
    # 检测号码是否长度是否合法。
    if len(s) != 11:
        logging.info("The length of phone num is 11.")
        return False
    else:
        # 检测输入的号码是否全部是数字。
        if s.isdigit():
            return True
            # 检测前缀是否是正确。
            # if s[:3] in phoneprefix:
            #     return True
            # else:
            #     logging.info("The phone num is invalid.")
            #     return False
        else:
            logging.info("The phone num is made up of digits.")
            return False


def get_md5(s):
    """
    get md5 of s
    :param s:
    :return:
    """
    m = hashlib.md5()
    m.update(s)
    return m.hexdigest()


def get_today():
    today = date.today()
    return today.strftime("%Y-%m-%d")
