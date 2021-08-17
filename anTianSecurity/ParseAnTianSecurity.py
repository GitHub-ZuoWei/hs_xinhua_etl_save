# uncompyle6 version 3.5.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.5 (default, Apr 19 2019, 17:01:24) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: ../src\anTianSecurity\ParseAnTianSecurity.py
# Compiled at: 2019-03-19 11:22:47
u"""
Created on 2018年4月17日

@author: mes
"""
import sys, os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from sysConfig.SysConfig import SysConfig
import utils.Mod_logger as log
from utils.ZipUtil import ZipUtil
from utils.CommonUtil import CommonUtil
import config.Config
from config import constantConfig as constConfig
from anTianSecurity.AnTianSecurityJSON import AnTianSecurityJSON
import shutil, pysolr, requests, redis, traceback
from utils.RedisClient import RedisClient

class ParseAnTianSecurity(AnTianSecurityJSON):
    u"""
          处理安天网络安全数据类
    """

    def __init__(self, db=None):
        self.hsNewsDataList = []
        self.hsNewsJorDataList = []
        self.solrLists = []
        self.hsNewsDataNums = 0

    def getIncrementData(self):
        u"""
        return:获取增量文件列表，数据包数据量统计字典
        """
        filenames = os.listdir(config.anTianSecurityPath)
        extractToFileList = []
        fileDict = {}
        for filename in filenames:
            if constConfig.AnTianSecurityReges in filename:
                element = self.redis.insert(name=constConfig.redis_anTianSecurity_zip, value=filename, kind='set')
                if element == 1:
                    extractFilePath = config.anTianSecurityPath + '/' + filename
                    extractToFilePath = config.anTianSecurityExtractFilePath + '/' + filename[:-4]
                    extractToFileList.append(extractToFilePath)
                    uipath = unicode(extractFilePath, 'utf-8')
                    zipUtil = ZipUtil(uipath)
                    zipUtil.extract_to(extractToFilePath)
                    zipUtil.close()
                    count = 0
                    for root, dirs, files in os.walk(extractToFilePath):
                        for anTianFile in files:
                            fileNamePath = (root + '/' + anTianFile).replace('\\', '/')
                            self.redis.insert(name=constConfig.redis_anTianSecurity_files, value=fileNamePath, kind='list')
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
                if self.redis.get_len(constConfig.redis_anTianSecurity_files) != None:
                    fileName = self.redis.fetch(name=constConfig.redis_anTianSecurity_files)
                    with open(unicode(fileName, 'utf-8'), 'r') as (f):
                        lists = eval(f.read())
                        for data_dict in lists:
                            try:
                                self.parseJson(data_dict)
                                validResult = self.dataValid()
                                if validResult is False:
                                    continue
                                hsNewsValueTuple = self.getHsNewsValueTuple(fileName)
                                hsNewsJorValueTuple = self.getHsNewsJorValueTuple()
                                solrTuple = self.getSolrValueTuple(hsNewsJorValueTuple)
                                solrDict = self.sysconfig.solrInfoDict(solrTuple)
                                self.hsNewsDataList.append(hsNewsValueTuple)
                                self.hsNewsJorDataList.append(hsNewsJorValueTuple)
                                self.solrLists.append(solrDict)
                                self.hsNewsDataNums = self.hsNewsDataNums + 1
                                if self.hsNewsDataNums >= int(config.anTianSecurityInsertSqlPers):
                                    self.lock.acquire()
                                    self.insertSqlProcess()
                                    self.lock.release()
                            except ValueError:
                                self.logger.error(traceback.format_exc())
                            except Exception:
                                self.logger.exception(traceback.format_exc())

                elif self.hsNewsDataNums != 0:
                    self.lock.acquire()
                    self.insertSqlProcess()
                    self.lock.release()
                else:
                    break

            except SyntaxError as e:
                self.logger.error(e)
                self.logger.error(traceback.format_exc())
            except Exception as e:
                self.logger.error(e)
                self.logger.exception(traceback.format_exc())

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
        self.hsNewsDataNums = 0
        self.hsNewsDataList = []
        self.hsNewsJorDataList = []
        self.solrLists = []

    def anTianSecurityProcess(self, lock):
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