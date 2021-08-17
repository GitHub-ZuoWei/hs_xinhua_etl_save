# uncompyle6 version 3.5.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.5 (default, Apr 19 2019, 17:01:24) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: ../src\parseMain\parseMain.py
# Compiled at: 2019-03-05 10:19:12
u"""
Created on 2018年5月31日

@author: mes
"""
import sys, os, traceback
from multiprocessing import Pool, Manager
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from utils.MysqlHelper import MysqlDataBase
import config.Config
from utils.FileUtil import FileUtil
import utils.Mod_logger as log
from digitLib.ParseDigitLibOfConsumer import ParseDigitLibOfConsumer
from digitLib.ParseDigitLibOfProducer import ParseDigitLibOfProducer
from jsfw.ParseJsfw import ParseJsfw
from video.ParseVideoOfConsumer import ParseVideoOfConsumer
from video.ParseVideoOfProducer import ParseVideoOfProducer
from zyfw.ParseZyfw import ParseZyfw
from internet.ParseInternet import ParseInternet
from anTianSecurity.ParseAnTianSecurity import ParseAnTianSecurity
from xhs.ParseXhs import ParseXhs
from txs.ParseTxs import ParseTxs

def parsePerHsLibrary(cls, lock):
    cls.parsePerHsLibrary(lock)


def putQueueQ(cls):
    cls.putQueue()


def parseJsfwData(cls, lock):
    cls.jsfwProcess(lock)


def parseInternetData(cls, lock):
    cls.internetProcess(lock)


def parseXhsData(cls, lock):
    cls.xhsProcess(lock)


def parseTxsData(cls, lock):
    cls.txsProcess(lock)


def getVideoList(cls):
    cls.getVideoList()


def parseVideoList(cls, lock):
    cls.parseVideoList(lock)


def parseZyfwData(cls, lock):
    cls.ZyfwProcess(lock)


def parseAnTianSecurityData(cls, lock):
    cls.anTianSecurityProcess(lock)


if __name__ == '__main__':
    logger = log.init_log(config.logBasePath + '/hs_parse.log')
    logger.info('start parse........')
    try:
        fileUtil = FileUtil()
        mysqlDB = MysqlDataBase()
        manager = Manager()
        lock = manager.Lock()
        p = Pool()
        if config.jsfwSpider == '1':
            parseJsfw = ParseJsfw()
            p.apply_async(parseJsfwData, args=(parseJsfw, lock))
        if config.internetSpider == '1':
            parseInternet = ParseInternet()
            p.apply_async(parseInternetData, args=(parseInternet, lock))
        if config.xhsSpider == '1':
            parseXhs = ParseXhs()
            p.apply_async(parseXhsData, args=(parseXhs, lock))
        if config.txsSpider == '1':
            parseTxs = ParseTxs()
            p.apply_async(parseTxsData, args=(parseTxs, lock))
        if config.videoSpider == '1':
            parseVideoOfProducer = ParseVideoOfProducer()
            parseVideoOfConsumer = ParseVideoOfConsumer()
            p.apply_async(getVideoList, args=(parseVideoOfProducer,))
            p.apply_async(parseVideoList, args=(parseVideoOfConsumer, lock))
        if config.zyfwSpider == '1':
            parseZyfw = ParseZyfw()
            p.apply_async(parseZyfwData, args=(parseZyfw, lock))
        if config.anTianSecuritySpider == '1':
            parseAnTianSecurity = ParseAnTianSecurity()
            p.apply_async(parseAnTianSecurityData, args=(parseAnTianSecurity, lock))
        if config.digitLibSpider == '1':
            parseDigitLibOfProducer = ParseDigitLibOfProducer()
            parseDigitLibOfConsumer = ParseDigitLibOfConsumer()
            p.apply_async(putQueueQ, args=(parseDigitLibOfProducer,))
            p.apply_async(parsePerHsLibrary, args=(parseDigitLibOfConsumer, lock))
        p.close()
        p.join()
        mysqlDB.close()
    except Exception as e:
        traceback.print_exc()
        logger.exception(e)