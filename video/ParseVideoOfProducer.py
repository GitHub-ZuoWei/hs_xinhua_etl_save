# uncompyle6 version 3.5.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.5 (default, Apr 19 2019, 17:01:24) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: ../src\video\ParseVideoOfProducer.py
# Compiled at: 2019-04-10 17:16:08
u"""
Created on 2018年4月15日

@author: mes
"""
import sys, os, time
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from utils.RedisClient import RedisClient
from sysConfig.SysConfig import SysConfig
from config import constantConfig as constConfig
import config.Config
from utils.FileUtil import FileUtil
from utils.TimeUtil import TimeUtil
from VideoJSON import VideoJSON
import utils.Mod_logger as log, datetime, redis, json

class ParseVideoOfProducer(VideoJSON):
    u"""
    视频数据解析（生产者）
    格式：
    """

    def __init__(self):
        self.HsLibraryConfigDataNums = 0
        self.HsLibraryConfigDataList = []

    def getVideoList(self):
        u"""
               获取视频列表信息
        """
        function_name = sys._getframe().f_code.co_name
        self.logger = log.init_log(config.logBasePath + '/' + function_name + '.log')
        self.logger.info('init ' + function_name)
        try:
            self.redis = RedisClient()
            self.redis.redis.ping()
            sysconfig = SysConfig()
            startDatatime = datetime.datetime.strptime(config.video_spider_start_time, '%Y-%m-%d')
            while 1:
                nowDataTime = datetime.datetime.now()
                if startDatatime >= nowDataTime:
                    break
                nextDataTime = TimeUtil.calDataTime(startDatatime, 1)
                element = self.redis.insert(name=constConfig.redis_video_list_set, value=startDatatime, kind='set')
                if element == 1:
                    video_list_path = config.video_list_path % (startDatatime.strftime('%Y-%m-%d'), nextDataTime.strftime('%Y-%m-%d'))
                    res_data = FileUtil.getResponse_requests(video_list_path)
                    if res_data != None:
                        try:
                            video_lists = json.loads(res_data.content)
                            for video_list in video_lists:
                                if video_list['section'].encode('utf-8') in sysconfig.videoTypeDict:
                                    self.redis.insert(name=constConfig.redis_video_list, value=video_list, kind='list')

                        except Exception as e:
                            self.logger.exception(e)

                startDatatime = nextDataTime

        except redis.exceptions.ConnectionError as e:
            error_message = 'Error 10061 Failed to connect redis server\n'
            self.logger.error(error_message)
        except Exception as e:
            self.logger.exception(e)

        return


if __name__ == '__main__':
    pass