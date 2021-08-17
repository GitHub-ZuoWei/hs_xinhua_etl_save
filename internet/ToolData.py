# uncompyle6 version 3.5.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.5 (default, Apr 19 2019, 17:01:24) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: ../src\internet\ToolData.py
# Compiled at: 2018-08-23 15:36:53
u"""
Created on 2018年4月15日

@author: mes
"""
import time
from config import constantConfig as constConfig

class ToolData(object):
    u"""
    互联网数据（工具数据（天气、汇率等））
    格式：Json格式
    """

    def __init__(self):
        pass

    def toolParseJson(self, dataDict):
        u"""
                解析Json
        """
        self.__titleDict = {}
        self.__encoding = dataDict.get('encoding')
        self.__contentForExport = dataDict.get('contentForExport')
        self.__siteCofName = dataDict.get('siteCofName')
        title = dataDict.get('title')
        self.__title = self.__titleDict.setdefault(title)
        self.__url = dataDict.get('url')

    def toolValid(self):
        u"""
                数据验证
        """
        if self.__title is None or self.__title == '':
            return False
        return True

    def insertHsToolsTable(self, *kw):
        u"""
                将写入的数据先转为insert语句
        title做主键，用replace语句
        """
        inTime = time.strftime('%Y-%m-%d %H:%M:%S')
        valueTuple = (self.__title, self.__contentForExport, self.__encoding, self.__siteCofName,
         self.__title, self.__url, constConfig.const_zero, inTime)
        self.sysconfig._cursor.execute(constConfig.hsToolsSql, valueTuple)
        self.sysconfig._conn.commit()


if __name__ == '__main__':
    pass