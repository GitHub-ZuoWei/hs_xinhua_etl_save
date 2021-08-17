# uncompyle6 version 3.5.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.5 (default, Apr 19 2019, 17:01:24) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: ../src\zyfw\ParseZyfw.py
# Compiled at: 2019-03-19 11:25:55
u"""
Created on 2018年4月15日

@author: mes
"""
import sys, os, pysolr
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from sysConfig.SysConfig import SysConfig
from utils.CommonUtil import CommonUtil
import config.Config
from utils.FileUtil import FileUtil
from ZyfwJSON import ZyfwJSON
from utils.SqlServerHelper import SqlServerDataBase
import utils.Mod_logger as log
from utils.RedisClient import RedisClient
from config import constantConfig as constConfig

class ParseZyfw(ZyfwJSON):
    u"""
        知远防务数据
       修改记录：
    20180531-1003：   
       将hs_zyfw_config dbId字段长度设大点为128
    """

    def __init__(self):
        self.hsLibraryDataList = []
        self.hsNewsJorDataList = []
        self.solrLists = []
        self.hsNewsDataNums = 0

    def parseZyfwDB(self):
        u"""
                解析知远防务数据库
        """
        try:
            for zyfwConfigDict in self.zyfwConfigLists:
                try:
                    dbId = zyfwConfigDict.get('dbId')
                    lastCrawTime = zyfwConfigDict['lastCrawTime']
                    self.getZyfwLibLists(dbId, lastCrawTime)
                    for zyfwDict in self.zyfwLists:
                        try:
                            zyfw_element = str(dbId) + str(zyfwDict['Id'])
                            element = self.redis.insert(name=constConfig.redis_zyfw_dbId, value=zyfw_element, kind='set')
                            if element == 1:
                                self.parseLibInfo(zyfwConfigDict, zyfwDict)
                                hsLibraryValueTuple = self.getHsLibraryValueTuple()
                                hsNewsJorValueTuple = self.getHsNewsJorValueTuple()
                                solrTuple = self.getSolrValueTuple(hsNewsJorValueTuple)
                                solrDict = self.sysconfig.solrInfoDict(solrTuple)
                                self.hsLibraryDataList.append(hsLibraryValueTuple)
                                self.hsNewsJorDataList.append(hsNewsJorValueTuple)
                                self.solrLists.append(solrDict)
                                self.hsNewsDataNums = self.hsNewsDataNums + 1
                                if self.hsNewsDataNums >= int(config.zyfwInsertSqlPers):
                                    self.lock.acquire()
                                    self.insertSqlProcess()
                                    self.lock.release()
                        except Exception as e:
                            self.logger.exception(e)

                    self.updateZyfwCrawTime(dbId)
                except Exception as e:
                    self.logger.exception(e)

            if self.hsNewsDataNums != 0:
                self.lock.acquire()
                self.insertSqlProcess()
                self.lock.release()
        except Exception as e:
            self.logger.exception(e)

    def insertSqlProcess(self):
        u"""
                批量插入数据
        """
        maxValue = self.sysconfig.getDynamicTable(constConfig.prefixNameOfLibraryTable)
        tableCodeDict = {}
        tableCodeDict['tableCode'] = int(maxValue)
        self.sysconfig._cursor.executemany('INSERT INTO ' + constConfig.prefixNameOfLibraryTable + maxValue + constConfig.hsLibrarySql, self.hsLibraryDataList)
        self.sysconfig._cursor.executemany(constConfig.hsNewsJorSql, [ self.hsNewsJorDataList[i] + (maxValue,) for i in range(self.hsNewsDataNums) ])
        self.sysconfig._conn.commit()
        if config.isIndex == '1':
            self.solr.add([ CommonUtil.merge_two_dicts(self.solrLists[i], tableCodeDict) for i in range(self.hsNewsDataNums) ], commit=True)
        self.hsNewsDataNums = 0
        self.hsLibraryDataList = []
        self.hsNewsJorDataList = []
        self.solrLists = []

    def ZyfwProcess(self, lock):
        function_name = sys._getframe().f_code.co_name
        self.logger = log.init_log(config.logBasePath + '/' + function_name + '.log')
        self.logger.info('init ' + function_name)
        try:
            self.lock = lock
            self.sqlServerDB = SqlServerDataBase()
            self.sysconfig = SysConfig()
            solrCoreAdmin = pysolr.SolrCoreAdmin(self.sysconfig.solrIp)
            solrCoreAdmin.status()
            self.solr = pysolr.Solr(self.sysconfig.solrIp)
            self.redis = RedisClient()
            self.redis.redis.ping()
            self.zyfwConfigLists = self.sysconfig.getHsZyfwConfig()
            self.parseZyfwDB()
        except Exception as e:
            self.logger.exception(e)


if __name__ == '__main__':
    fileUtil = FileUtil()
    sqlServerDB = SqlServerDataBase()
    parseZyfw = ParseZyfw()
    parseZyfw.init_process()