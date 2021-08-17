# uncompyle6 version 3.5.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.5 (default, Apr 19 2019, 17:01:24) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: ../src\internet\ParseInternet.py
# Compiled at: 2019-03-19 11:23:59
u"""
Created on 2018年4月17日

@author: mes
"""
import sys, os
from sysConfig.SysConfig import SysConfig
import utils.Mod_logger as log
from utils.ZipUtil import ZipUtil
from utils.CommonUtil import CommonUtil
import config.Config
from ToolData import ToolData
from InterNetDataRelation import InterNetDataRelation
from config import constantConfig as constConfig
from InterNetJSON import InterNetJSON
import shutil, pysolr, requests, redis
from utils.RedisClient import RedisClient
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

class ParseInternet(InterNetJSON, InterNetDataRelation, ToolData):
    u"""
          处理互联网数据类
    """

    def __init__(self, db=None):
        self.hsNewsDataList = []
        self.hsNewsJorDataList = []
        self.hsJoseonDataList = []
        self.solrLists = []
        self.hsNewsDataNums = 0

    def getIncrementData(self):
        u"""
        return:获取增量文件列表，数据包数据量统计字典
        """
        filenames = os.listdir(config.internetPath)
        extractToFileList = []
        fileDict = {}
        for filename in filenames:
            if constConfig.internetReg in filename:
                element = self.redis.insert(name=constConfig.redis_internet_zip, value=filename, kind='set')
                if element == 1:
                    extractFilePath = config.internetPath + '/' + filename
                    extractToFilePath = config.extractFilePath + '/' + filename[:-4]
                    extractToFileList.append(extractToFilePath)
                    uipath = unicode(extractFilePath, 'utf-8')
                    zipUtil = ZipUtil(uipath)
                    zipUtil.extract_to(extractToFilePath)
                    zipUtil.close()
                    count = 0
                    for root, dirs, files in os.walk(extractToFilePath):
                        for internetFile in files:
                            fileNamePath = (root + '/' + internetFile).replace('\\', '/')
                            self.redis.insert(name=constConfig.redis_internet_files, value=fileNamePath, kind='list')
                            count += 1

                    fileDict[filename] = count

        return (
         extractToFileList, fileDict)

    def parseFile(self):
        u"""
                解析每个文件
        """
        while 1:
            try:
                if self.redis.get_len(constConfig.redis_internet_files) != None:
                    fileName = self.redis.fetch(name=constConfig.redis_internet_files)
                    if fileName.split('/')[(-1)] == constConfig.internetFile:
                        with open(unicode(fileName, 'utf-8'), 'r') as (f):
                            dict_name = eval(f.read())
                            if dict_name.get('taskDataId') != constConfig.toolDataId:
                                try:
                                    self.parseJson(fileName, dict_name)
                                    validResult = self.internetValid()
                                    if validResult is False:
                                        continue
                                    hsNewsJorValueTuple = self.getHsNewsJorValueTuple()
                                    hsNewsValueTuple = self.getHsNewsValueTuple(fileName)
                                    solrTuple = self.getSolrValueTuple(hsNewsJorValueTuple)
                                    solrDict = self.sysconfig.solrInfoDict(solrTuple)
                                    self.hsNewsDataList.append(hsNewsValueTuple)
                                    self.hsNewsJorDataList.append(hsNewsJorValueTuple)
                                    self.solrLists.append(solrDict)
                                    self.hsNewsDataNums = self.hsNewsDataNums + 1
                                    if dict_name.get('siteCofName') in constConfig.Korea_sourceDict:
                                        hsJoseonValueTuple = self.getHsJoseonValueTuple(dict_name.get('siteCofName'))
                                        self.hsJoseonDataList.append(hsJoseonValueTuple)
                                except Exception as e:
                                    self.logger.exception(e)

                            else:
                                try:
                                    self.toolParseJson(dict_name)
                                    validResult = self.toolValid()
                                    if validResult is False:
                                        continue
                                    self.lock.acquire()
                                    self.insertHsToolsTable()
                                    self.lock.release()
                                except Exception as e:
                                    self.logger.exception(e)

                    elif constConfig.internetRelationFile in fileName.split('/')[(-1)]:
                        validResult, fileNameDateTime = self.internetRelationValid(fileName)
                        if validResult is False:
                            continue
                        self.sysconfig.init_sysconfig()
                        with open(unicode(fileName, 'utf-8'), 'r') as (f):
                            list_name = eval(f.read())
                            for dict_name in list_name:
                                try:
                                    self.ParseInterNetRelationJson(dict_name)
                                    if self.getGuid == constConfig.toolGuid or self.getPid == constConfig.toolGuid:
                                        continue
                                    if self.sysconfig.countryNumByCountryEnDict.get(self.getRegion) == None:
                                        try:
                                            if self.getRegion_cn == None:
                                                continue
                                            else:
                                                self.insertCountryTable()
                                                self.sysconfig.countryNumByCountryEnDict = self.sysconfig.getCountryNumByCountryEnDict()
                                                self.sysconfig.countryNumByCountryDict = self.sysconfig.getCountryNumByCountryDict()
                                        except Exception as e:
                                            self.logger.exception(e)

                                    if dict_name.get('verifyStatus') == '1':
                                        try:
                                            if dict_name.get('pId') == '-1':
                                                self.updateHsMediaTable()
                                            else:
                                                self.updateHsMediaSectionTable(fileNameDateTime)
                                        except Exception as e:
                                            self.logger.exception(e)

                                except Exception as e:
                                    self.logger.exception(e)

                            self.sysconfig._conn.commit()
                        self.delMediaAndMediaSec()
                        self.sysconfig.init_sysconfig()
                    if self.hsNewsDataNums >= int(config.insertSqlPers):
                        self.lock.acquire()
                        self.insertSqlProcess()
                        self.lock.release()
                elif self.hsNewsDataNums != 0:
                    self.lock.acquire()
                    self.insertSqlProcess()
                    self.lock.release()
                else:
                    break

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
        self.sysconfig._cursor.executemany(constConfig.hsJoseonSql, self.hsJoseonDataList)
        self.sysconfig._conn.commit()
        if config.isIndex == '1':
            self.solr.add([ CommonUtil.merge_two_dicts(self.solrLists[i], tableCodeDict) for i in range(self.hsNewsDataNums) ], commit=True)
        self.hsNewsDataNums = 0
        self.hsNewsDataList = []
        self.hsNewsJorDataList = []
        self.hsJoseonDataList = []
        self.solrLists = []

    def internetProcess(self, lock):
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
            extractToFileList, fileDict = self.getIncrementData()
            self.parseFile()
            self.DataStatistics(fileDict)
            for extractToFilePath in extractToFileList:
                shutil.rmtree(extractToFilePath)

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