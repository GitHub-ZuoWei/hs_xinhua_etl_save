# uncompyle6 version 3.5.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.5 (default, Apr 19 2019, 17:01:24) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: ../src\txs\ParseTxs.py
# Compiled at: 2019-03-19 11:25:00
u"""
Created on 2018年4月17日

@author: mes
"""
import os, sys
from utils.RedisClient import RedisClient
import xml.etree.ElementTree as ET
from txs.TxsXml import TxsXml
import utils.Mod_logger as log
from utils.CommonUtil import CommonUtil
import pkg_resources, pysolr, requests, redis, config.Config
from sysConfig.SysConfig import SysConfig
from config import constantConfig as constConfig
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

class ParseTxs(TxsXml):
    u"""
        四大通讯社
        格式：
    """

    def __init__(self):
        self.hsNewsDataList = []
        self.hsNewsJorDataList = []
        self.spiderTxsTagsDataList = []
        self.solrLists = []
        self.hsNewsDataNums = 0

    def getIncrementData(self):
        u"""
                获取增量文件
        return:返回解压的文件夹路径
        """
        for root, dirs, files in os.walk(config.txsPath):
            for dir in dirs:
                lists = os.listdir(config.txsPath + '/' + dir)
                for fileXML in lists:
                    if fileXML[-4:] == '.xml':
                        element = self.redis.insert(name=constConfig.redis_txs, value=fileXML, kind='set')
                        if element == 1:
                            txsFileName = config.txsPath + '/' + dir + '/' + fileXML
                            yield txsFileName

    def parseFile(self):
        try:
            for txsFilePath in self.getIncrementData():
                try:
                    tree = ET.parse(txsFilePath)
                    self.parseXML(tree)
                    validResult = self.txsValid()
                    if validResult is False:
                        continue
                    spiderTxsTagsTuple = self.insertSpiderTxsTags()
                    if spiderTxsTagsTuple != None:
                        self.spiderTxsTagsDataList.append(spiderTxsTagsTuple)
                    hsNewsJorValueTuple = self.getHsNewsJorValueTuple()
                    hsNewsValueTuple = self.getHsNewsValueTuple(txsFilePath)
                    solrTuple = self.getSolrValueTuple(hsNewsJorValueTuple)
                    solrDict = self.sysconfig.solrInfoDict(solrTuple)
                    self.hsNewsDataList.append(hsNewsValueTuple)
                    self.hsNewsJorDataList.append(hsNewsJorValueTuple)
                    self.solrLists.append(solrDict)
                    self.hsNewsDataNums = self.hsNewsDataNums + 1
                    if self.hsNewsDataNums >= int(config.txsInsertSqlPers):
                        self.lock.acquire()
                        self.insertSqlProcess()
                        self.lock.release()
                except Exception as e:
                    self.logger.exception(e)

            if self.hsNewsDataNums != 0:
                self.lock.acquire()
                self.insertSqlProcess()
                self.lock.release()
        except Exception as e:
            self.logger.exception(e)

        return

    def insertSqlProcess(self):
        u"""
                批量插入数据
        """
        maxValue = self.sysconfig.getDynamicTable('hs_news_')
        tableCodeDict = {}
        tableCodeDict['tableCode'] = int(maxValue)
        self.sysconfig._cursor.executemany('INSERT INTO hs_news_' + maxValue + constConfig.hsNewsSql, self.hsNewsDataList)
        self.sysconfig._cursor.executemany(constConfig.hsNewsJorSql, [ self.hsNewsJorDataList[i] + (maxValue,) for i in range(self.hsNewsDataNums) ])
        self.sysconfig._conn.commit()
        if config.isIndex == '1':
            self.solr.add([ CommonUtil.merge_two_dicts(self.solrLists[i], tableCodeDict) for i in range(self.hsNewsDataNums) ], commit=True)
        if len(self.spiderTxsTagsDataList) != 0:
            self.sysconfig._cursor.executemany(constConfig.spiderTxsTagsSql, self.spiderTxsTagsDataList)
            self.sysconfig._conn.commit()
            self.spiderTxsTagsDataList = []
        self.hsNewsDataNums = 0
        self.hsNewsDataList = []
        self.hsNewsJorDataList = []
        self.solrLists = []

    def txsProcess(self, lock):
        function_name = sys._getframe().f_code.co_name
        self.logger = log.init_log(config.logBasePath + '/' + function_name + '.log')
        self.logger.info('init ' + function_name)
        try:
            self.lock = lock
            self.redis = RedisClient()
            self.redis.redis.ping()
            self.sysconfig = SysConfig()
            solrCoreAdmin = pysolr.SolrCoreAdmin(self.sysconfig.solrIp)
            solrCoreAdmin.status()
            requests.get(constConfig.nlpUrl)
            self.solr = pysolr.Solr(self.sysconfig.solrIp)
            self.parseFile()
            self.sysconfig.close()
        except requests.exceptions.ConnectionError as e:
            error_message = 'Failed to connect to solr server, are you sure that URL is correct? Checking it in a browser might help!\n                             or failed to connect NLP server!'
            self.logger.error(error_message)
        except redis.exceptions.ConnectionError as e:
            self.logger.error(e)
        except Exception as e:
            self.logger.exception(e)


if __name__ == '__main__':
    pass