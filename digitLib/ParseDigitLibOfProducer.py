# uncompyle6 version 3.5.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.5 (default, Apr 19 2019, 17:01:24) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: ../src\digitLib\ParseDigitLibOfProducer.py
# Compiled at: 2019-04-17 07:22:06
u"""
Created on 2018年4月15日

@author: mes
"""
import sys, os, codecs
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from utils.RedisClient import RedisClient
from sysConfig.SysConfig import SysConfig
import config.Config
from utils.FileUtil import FileUtil
import utils.Mod_logger as log
from DigitLibJSON import DigitLibJSON
from config import constantConfig as constConfig

class ParseDigitLibOfProducer(DigitLibJSON):
    u"""
        数字图书馆数据(生产者)
        格式：
    """

    def __init__(self):
        super(ParseDigitLibOfProducer, self).__init__()

    def getHsLibraryConfigList(self):
        u"""
               更新数据库配置信息
        """
        res_data = FileUtil.getResponseData(config.digitLib_all_DB)
        if res_data != None:
            res_lines = res_data.readlines()
            for i in xrange(len(res_lines)):
                try:
                    if i == 0:
                        if res_lines[i][:3] == codecs.BOM_UTF8:
                            res_lines[i] = res_lines[i][3:]
                    self.parseAllDBInfo(res_lines[i])
                    element = self.redis.insert(name=constConfig.redis_library_config, value=self.getTrsDbId, kind='set')
                    if element == 1:
                        hsLibraryConfigValueTuple = self.getHsLibraryConfigValueTuple()
                        self.sysconfig._cursor.execute(constConfig.hsLibraryConfigSql, hsLibraryConfigValueTuple)
                        self.sysconfig._conn.commit()
                except Exception as e:
                    self.logger.exception(e)

        return

    def putQueue(self):
        u"""
         :param libLists:数字图书馆列表
         :return:
                     将数据库信息以列表形式添加到queue(生产者)
         """
        function_name = sys._getframe().f_code.co_name
        self.logger = log.init_log(config.logBasePath + '/' + function_name + '.log')
        self.logger.info('init ' + function_name)
        try:
            self.redis = RedisClient()
            self.redis.redis.ping()
            self.sysconfig = SysConfig()
            self.getHsLibraryConfigList()
            libConfigLists = self.sysconfig.getHsLibraryConfig()
            for libDict in libConfigLists:
                for rid in range(int(libDict['lastSpiderCount']), int(libDict['dbCount'])):
                    libDict['rid'] = str(rid + 1)
                    self.redis.insert(name=constConfig.redis_library_files, value=libDict, kind='list')

                self.updateHsLibraryConfig(int(libDict['dbCount']), libDict['dbId'])

        except Exception as e:
            self.logger.exception(e)


if __name__ == '__main__':
    pass