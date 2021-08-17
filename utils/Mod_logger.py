# uncompyle6 version 3.5.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.7.3 (default, Mar 27 2019, 17:13:21) [MSC v.1915 64 bit (AMD64)]
# Embedded file name: ../src\utils\Mod_logger.py
# Compiled at: 2018-07-13 09:21:42
u"""
Created on 2018年4月15日

@author: mes
"""
import config.Config, logging, sys
from logging import getLogger, INFO, Formatter, WARN
from concurrent_log_handler import ConcurrentRotatingFileHandler

def init_log(logpath):
    u"""
        日志分5个等级：critical:50 error:40 warning:30 info:20 debug:10 notset:0
    maxBytes:每个日志文件的大小
    backupcount：保留日志文件份数
    """
    format = config.format.replace('@', '%')
    level = int(config.level)
    backupcount = int(config.backupcount)
    maxbytes = int(config.maxbytes)
    log = getLogger()
    rotate_handler = ConcurrentRotatingFileHandler(logpath, mode='a', maxBytes=maxbytes, backupCount=backupcount, encoding='utf-8')
    formatter = Formatter(format)
    rotate_handler.setFormatter(formatter)
    log.addHandler(rotate_handler)
    log.setLevel(level)
    return log


def setLogger(logpath):
    logger = logging.getLogger('hs_parse')
    formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)-8s: %(message)s')
    file_handler = logging.FileHandler(logpath)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.formatter = formatter
    console_handler.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger


if __name__ == '__main__':
    print 'mod_logger'