# *-* coding: utf-8 *-*
import time


def now_timestamp10():
    """
    当前时间戳
    :return:
    """
    return int(time.time())


def now_timestamp13():
    """
    当前13位时间戳
    :return:
    """
    return now_timestamp10() * 1000