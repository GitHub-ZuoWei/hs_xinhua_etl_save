# uncompyle6 version 3.5.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.5 (default, Apr 19 2019, 17:01:24) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: ../src\video\VideoJSON.py
# Compiled at: 2019-04-10 18:27:17
u"""
Created on 2018年4月15日

@author: mes
"""
import uuid, time, os
from utils.TimeUtil import TimeUtil
from utils.FileUtil import FileUtil
from config import constantConfig as constConfig

class VideoJSON(object):
    u"""
    视频JSON数据解析
    """

    def __init__(self):
        pass

    def parseVideoInfo(self, data):
        u"""
                解析Video dict文件
        """
        self.__localImgPath = None
        self.__localFilePath = None
        self.__videoId = str(data['id'])
        self.__info = data['info']
        if self.__info != '' and self.__info != None:
            self.__info = self.__info.encode('utf-8')
        self.__url = data['url']
        self.__title = data['title']
        if self.__title != '' and self.__title != None:
            titleList = self.__title.encode('utf-8').split('、')
            self.__title = titleList[0].strip() if len(titleList) == 1 else titleList[1].strip()
        self.__section = data['section']
        if self.__section != '' and self.__section != None:
            self.__section = self.__section.encode('utf-8')
        self.__tag = data['keypersons']
        if self.__tag != '' and self.__tag != None:
            self.__tag = self.__tag.encode('utf-8')
        self.__upload_time = data['upload_time'][:10] + ' 16:00:00'
        return

    def savePicOrFile(self, webPath, basePath, sTypePath, file_name):
        u"""
                从服务器获取文件并保存到本地
        :return:
        """
        saveLocalPath = None
        res = FileUtil.getResponse_requests(webPath)
        if res is None:
            return saveLocalPath
        else:
            headersDict = eval(str(res.headers))
            if headersDict.has_key('Content-Disposition'):
                fileName = headersDict['Content-Disposition'].split('filename=')[1]
            elif headersDict.has_key('Content-Type'):
                fileName = headersDict['Content-Type'].split('/')[1]
                fileName = file_name + '.' + fileName
            elif headersDict.has_key('Content-type'):
                fileName = headersDict['Content-type'].split('/')[1]
                fileName = file_name + '.' + fileName
            else:
                return saveLocalPath
            str_time = time.strftime('%Y%m%d')
            year_path = os.path.join(basePath, str_time[:4]).replace('\\', '/')
            time_path = os.path.join(year_path, str_time).replace('\\', '/')
            lastPath = os.path.join(time_path, sTypePath).replace('\\', '/')
            FileUtil.mkdir(year_path)
            FileUtil.mkdir(time_path)
            FileUtil.mkdir(lastPath)
            absolutePath = os.path.join(lastPath, fileName).replace('\\', '/')
            saveLocalPath = os.path.join('/temp', str_time[:4], str_time, sTypePath, fileName).replace('\\', '/')
            with open(absolutePath, 'wb') as (db_f):
                for chunk in res.iter_content(chunk_size=512):
                    if chunk:
                        db_f.write(chunk)

            return saveLocalPath

    def getHsVideoValueTuple(self, *kw):
        u"""
        hs_video表值
        """
        img_url = kw[0]
        video_url = kw[1]
        oriTime = self.__upload_time
        inTime = time.strftime('%Y-%m-%d %H:%M:%S')
        videoId = str(uuid.uuid1()).replace('-', '')
        videoType = self.sysconfig.videoTypeDict.get(self.__section)
        valueTuple = (
         videoId, self.__title, videoType, self.__tag,
         self.__info, img_url, video_url, self.__url,
         oriTime, inTime, constConfig.const_zero)
        return valueTuple


if __name__ == '__main__':
    pass