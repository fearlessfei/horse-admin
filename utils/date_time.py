# *-* coding: utf-8 *-*
import time
import datetime


def time10():
    """
    当前时间戳
    :return:
    """
    return int(time.time())


def time13():
    """
    当前13位时间戳
    :return:
    """
    return time10() * 1000


def day_start():
    """
    当天0点时间戳
    :return:
    """
    now = datetime.datetime.now()
    return int(time.mktime((now.year, now.month, now.day, 0, 0, 0, 0, 0, 0)))