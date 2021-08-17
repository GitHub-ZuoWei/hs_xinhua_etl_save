# uncompyle6 version 3.5.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.5 (default, Apr 19 2019, 17:01:24) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: ../src\digitLib\ParseDigitLibOfConsumer.py
# Compiled at: 2019-04-17 11:38:06
u"""
Created on 2018年4月15日

@author: mes
"""
import sys, os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import pysolr
from utils.RedisClient import RedisClient
from utils.CommonUtil import CommonUtil
from sysConfig.SysConfig import SysConfig
import config.Config, utils.Mod_logger as log
from DigitLibJSON import DigitLibJSON
from config import constantConfig as constConfig
from config import Config as config

class ParseDigitLibOfConsumer(DigitLibJSON):
    u"""
        数字图书馆数据(消费者)
        格式：
    """

    def __init__(self):
        super(ParseDigitLibOfConsumer, self).__init__()
        self.hsLibraryDataList = []
        self.hsNewsJorDataList = []
        self.solrLists = []
        self.hsLibraryDataNums = 0

    def parsePerHsLibrary(self, lock):
        u"""
                解析数据库
        """
        self.sysconfig = SysConfig()
        function_name = sys._getframe().f_code.co_name
        self.logger = log.init_log(config.logBasePath + '/' + function_name + '.log')
        self.logger.info('init ' + function_name)
        self.lock = lock
        self.redis = RedisClient()
        self.redis.redis.ping()
        solrCoreAdmin = pysolr.SolrCoreAdmin(self.sysconfig.solrIp)
        solrCoreAdmin.status()
        self.solr = pysolr.Solr(self.sysconfig.solrIp)
        while 1:
            if self.redis.get_len(constConfig.redis_library_files) != None:
                try:
                    self.lock.acquire()
                    libDict = self.redis.fetch(name=constConfig.redis_library_files, timeout=int(config.digitLib_timeout))
                    self.parseLibInfo(libDict)
                    lock.release()
                    if self.getTitle is None or self.getTitle == '':
                        continue
                    pic_path = config.digitLib_db_pic + 'db=' + str(self.getDbId) + '&rid=' + str(self.getRid)
                    file_path = config.digitLib_db_file + 'db=' + str(self.getDbId) + '&rid=' + str(self.getRid)
                    try:
                        self.localPicPath = self.savePicOrFile(pic_path, config.localBasePath, constConfig.libPicPath['1'])
                    except Exception as e:
                        self.localPicPath = None
                        self.logger.exception(e)

                    self.localFilePath = file_path
                    hsLibraryValueTuple = self.getHsLibraryValueTuple()
                    hsNewsJorValueTuple = self.getHsNewsJorValueTuple()
                    solrTuple = self.getSolrValueTuple(hsNewsJorValueTuple)
                    solrDict = self.sysconfig.solrInfoDict(solrTuple)
                    self.hsLibraryDataList.append(hsLibraryValueTuple)
                    self.hsNewsJorDataList.append(hsNewsJorValueTuple)
                    self.solrLists.append(solrDict)
                    self.hsLibraryDataNums = self.hsLibraryDataNums + 1
                    if self.hsLibraryDataNums >= int(config.digitLibInsertSqlPers):
                        self.lock.acquire()
                        self.insertSqlProcess()
                        self.lock.release()
                except Exception as e:
                    self.logger.exception(e)

            else:
                try:
                    if self.hsLibraryDataNums != 0:
                        self.lock.acquire()
                        self.insertSqlProcess()
                        self.lock.release()
                    break
                except Exception as e:
                    self.logger.exception(e)
                    break

        return

    def insertSqlProcess(self):
        u"""
                批量插入数据
        """
        maxValue = self.sysconfig.getDynamicTable(constConfig.prefixNameOfLibraryTable)
        tableCodeDict = {}
        tableCodeDict['tableCode'] = int(maxValue)
        self.sysconfig._cursor.executemany('INSERT INTO ' + constConfig.prefixNameOfLibraryTable + maxValue + constConfig.hsLibrarySql, self.hsLibraryDataList)
        self.sysconfig._cursor.executemany(constConfig.hsNewsJorSql, [ self.hsNewsJorDataList[i] + (maxValue,) for i in range(self.hsLibraryDataNums) ])
        self.sysconfig._conn.commit()
        if config.isIndex == '1':
            self.solr.add([ CommonUtil.merge_two_dicts(self.solrLists[i], tableCodeDict) for i in range(self.hsLibraryDataNums) ], commit=True)
        self.hsLibraryDataNums = 0
        self.hsLibraryDataList = []
        self.hsNewsJorDataList = []
        self.solrLists = []


if __name__ == '__main__':
    pass