# uncompyle6 version 3.5.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.5 (default, Apr 19 2019, 17:01:24) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: ../src\internet\InterNetDataRelation.py
# Compiled at: 2018-11-16 17:42:16
u"""
Created on 2018年4月15日

@author: mes
"""
import uuid, time
from datetime import datetime
from pypinyin import lazy_pinyin, Style
from config import constantConfig as constConfig

class InterNetDataRelation(object):
    u"""
    互联网数据（新闻关系）
    格式：Json格式
    """

    def __init__(self, db=None, sysconfig=None):
        pass

    def ParseInterNetRelationJson(self, dataDict):
        u"""
                解析Json
        """
        self.__guid = dataDict.get('guid')
        self.__pId = dataDict.get('pId')
        self.__land = dataDict.get('land')
        self.__languages = dataDict.get('languages')
        self.__name = dataDict.get('name')
        self.__region = dataDict.get('region')
        self.__region_cn = dataDict.get('region_cn')
        self.__tags = dataDict.get('tags')
        self.__ishotsopt = dataDict.get('ishotsopt')

    @property
    def getGuid(self):
        return self.__guid

    @property
    def getPid(self):
        return self.__pId

    @property
    def getRegion(self):
        return self.__region

    @property
    def getRegion_cn(self):
        return self.__region_cn

    def internetRelationValid(self, *kw):
        u"""
                验证：小于当前媒体数据的时间，不更新媒体表
        """
        fileName = kw[0]
        fileNameDateTime = datetime.strptime(fileName.split('/')[(-3)][:19].replace('_', ':'), '%Y-%m-%d %H:%M:%S')
        siteDateTime = self.redis.fetch(name=constConfig.redis_internet_siteDateTime)
        siteDateTimeOfMediaSection = datetime.strptime(siteDateTime, '%Y-%m-%d %H:%M:%S')
        if fileNameDateTime <= siteDateTimeOfMediaSection:
            return (False, fileNameDateTime)
        else:
            self.redis.insert(constConfig.redis_internet_siteDateTime, fileNameDateTime)
            return (
             True, fileNameDateTime)

    def insertCountryTable(self, *kw):
        u"""
                互联网数据有新的国家，则插入国家表
        """
        countryList = sorted(self.sysconfig.countryNumByCountryEnDict.items(), key=lambda d: d[1], reverse=True)
        newCountryNum = int(countryList[0][1]) + 1
        regionCode = self.sysconfig.regionByCountryDict.get(self.__region_cn)
        spellFull = lazy_pinyin(unicode(self.__region_cn, 'utf-8'), strict=False)
        spellFirst = lazy_pinyin(unicode(self.__region_cn, 'utf-8'), style=Style.INITIALS, strict=False)
        initials = spellFirst[0].upper()
        countryId = str(uuid.uuid1()).replace('-', '')
        valueTuple = (countryId, newCountryNum, self.__region_cn, self.__region_cn,
         self.__region_cn, self.__region, regionCode, initials,
         ('').join(spellFull), ('').join(spellFirst), constConfig.const_zero)
        self.sysconfig._cursor.execute(constConfig.hsCountrySql, valueTuple)
        self.sysconfig._conn.commit()

    def updateHsMediaTable(self, *kw):
        u"""
                更新互联网媒体表：hs_media
                因为华茹给的媒体表会定期更新，并且华茹那边媒体主键guid会变（当华茹删了某个媒体，后来又添加了这个媒体），媒体名称name也会变，
                所以更新策略为：
                当该媒体Id不在当前的mediaId表中,也不在当前的媒体名称表，直接插入；
                当该媒体Id不在当前的mediaId表中,在当前的媒体名称表，不做更新；
                当该媒体Id在当前的mediaId表中,不在当前的媒体名称表，更新该媒体信息；
                当该媒体Id在当前的mediaId表中,在当前的媒体名称表，更新该媒体信息；
        """
        mediaId = str(uuid.uuid5(uuid.NAMESPACE_DNS, self.__guid)).replace('-', '')
        countryNum = self.sysconfig.countryNumByCountryDict.get(self.__region_cn)
        inTime = time.strftime('%Y-%m-%d %H:%M:%S')
        if countryNum == None:
            countryNum = self.sysconfig.countryNumByCountryEnDict.get(self.__region)
        insertValueTuple = (
         mediaId, self.__name, countryNum, constConfig.const_zero,
         inTime)
        updateValueTuple = (self.__name, countryNum, inTime, mediaId)
        if mediaId not in self.sysconfig.mediaDict:
            if self.__name.decode('utf-8') not in self.sysconfig.mediaNameDict:
                if countryNum != None:
                    self.sysconfig._cursor.execute(constConfig.hsMediaSql, insertValueTuple)
            else:
                oldMediaId = self.sysconfig.mediaIdByNameDict.get(self.__name.decode('utf-8'))
                self.sysconfig.mediaDict[oldMediaId] = '0'
        else:
            self.sysconfig.mediaDict[mediaId] = '0'
            self.sysconfig._cursor.execute(constConfig.updateMediaSql, updateValueTuple)
        return

    def updateHsMediaSectionTable(self, *kw):
        u"""
                更新互联网媒体版块表：hs_media_section
                因为华茹给的媒体板块表会定期更新，并且华茹那边媒体板块主键guid会变（当华茹删了某个媒体板块，后来又添加了这个媒体板块），媒体板块名称name也会变，
                所以更新策略为：
                当该媒体板块Id不在当前的mediaId表中,也不在当前的媒体板块名称表，直接插入；
                当该媒体板块Id不在当前的mediaId表中,在当前的媒体板块名称表，不做更新；
                当该媒体板块Id在当前的mediaId表中,不在当前的媒体板块名称表，更新该媒体板块信息；
                当该媒体板块Id在当前的mediaId表中,在当前的媒体板块名称表，更新该媒体板块信息；
        """
        fileNameDateTime = kw[0]
        mediaId = str(uuid.uuid5(uuid.NAMESPACE_DNS, self.__pId)).replace('-', '')
        mediaSectionId = str(uuid.uuid5(uuid.NAMESPACE_DNS, self.__guid)).replace('-', '')
        countryNum = self.sysconfig.countryNumByCountryDict.get(self.__region_cn)
        if countryNum == None:
            countryNum = self.sysconfig.countryNumByCountryEnDict.get(self.__region)
        regionCode = self.sysconfig.regionByCountryDict.get(self.__region_cn)
        land = self.sysconfig.regionDict.get(regionCode)
        languageNum = self.sysconfig.numByLanguageDict.get(self.__languages)
        operateTime = time.strftime('%Y-%m-%d %H:%M:%S')
        if self.__ishotsopt == '' or self.__ishotsopt is None:
            self.__ishotsopt = '0'
        updateValueTuple = (self.__tags, self.__languages, languageNum, self.__region_cn,
         self.__region, countryNum, land, regionCode,
         self.__ishotsopt, constConfig.const_zero, operateTime, fileNameDateTime,
         self.__name, mediaSectionId)
        InsertValueTuple = (
         mediaSectionId, mediaId, self.__name, self.__tags,
         self.__languages, languageNum, self.__region_cn, self.__region,
         countryNum, land, regionCode, self.__ishotsopt,
         constConfig.const_zero, operateTime, fileNameDateTime)
        if mediaSectionId not in self.sysconfig.mediaSectionDict:
            if self.__name.decode('utf-8') not in self.sysconfig.mediaSectionNameDict:
                self.sysconfig._cursor.execute(constConfig.hsMediaSectionInsertSql, InsertValueTuple)
            else:
                oldMediaSectionId = self.sysconfig.mediaSectionIdByNameDict.get(self.__name.decode('utf-8'))
                self.sysconfig.mediaSectionDict[oldMediaSectionId] = '0'
        else:
            self.sysconfig.mediaSectionDict[mediaSectionId] = '0'
            self.sysconfig._cursor.execute(constConfig.hsMediaSectionUpdateSql, updateValueTuple)
        return

    def delMediaAndMediaSec(self, *kw):
        u"""
                删除不在当前的媒体和媒体板块字段
        """
        if len(self.sysconfig.mediaDict) != 0:
            deleteMediaList = []
            for mediaId, v in self.sysconfig.mediaDict.iteritems():
                if v == '1':
                    deleteMediaList.append(mediaId)

            self.sysconfig._cursor.executemany(constConfig.deleteMediaIdSql, deleteMediaList)
            self.sysconfig._conn.commit()
        if len(self.sysconfig.mediaSectionDict) != 0:
            deleteMediaSectionList = []
            for mediaSectionId, v in self.sysconfig.mediaSectionDict.iteritems():
                if v == '1':
                    deleteMediaSectionList.append(mediaSectionId)

            self.sysconfig._cursor.executemany(constConfig.deleteMediaSectionSql, deleteMediaSectionList)
            self.sysconfig._conn.commit()


if __name__ == '__main__':
    pass