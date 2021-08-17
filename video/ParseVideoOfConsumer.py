# uncompyle6 version 3.5.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.5 (default, Apr 19 2019, 17:01:24) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: ../src\video\ParseVideoOfConsumer.py
# Compiled at: 2019-04-10 18:54:19
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

class ParseVideoOfConsumer(VideoJSON):
    u"""
    视频数据解析（消费者）
    格式：
    """

    def __init__(self):
        super(ParseVideoOfConsumer, self).__init__()

    def parseVideoList(self, lock):
        u"""
                解析视频列表(消费者)
        """
        function_name = sys._getframe().f_code.co_name
        self.logger = log.init_log(config.logBasePath + '/' + function_name + '.log')
        self.logger.info('init ' + function_name)
        try:
            self.redis = RedisClient()
            self.redis.redis.ping()
            self.sysconfig = SysConfig()
            while 1:
                try:
                    videoStr = self.redis.fetch(name=constConfig.redis_video_list, timeout=int(config.digitLib_timeout))
                    if videoStr == None:
                        break
                    videoDict = FileUtil.strTransToObject(videoStr)
                    videoId = str(videoDict['id'])
                    pic_path = videoDict['keyframe_images']
                    if pic_path == None:
                        continue
                    file_path = videoDict['hdfs_address']
                    if file_path == None:
                        continue
                    else:
                        file_path = file_path + config.video_postfix_path
                    self.parseVideoInfo(videoDict)
                    localPicPath = self.savePicOrFile(pic_path, config.localBasePath, constConfig.videoPicPath, videoId)
                    valueTuple = self.getHsVideoValueTuple(localPicPath, file_path)
                    self.sysconfig._cursor.execute(constConfig.insertHsVideoSql, valueTuple)
                    self.sysconfig._conn.commit()
                except Exception as e:
                    self.logger.exception(e)

        except redis.exceptions.ConnectionError as e:
            error_message = 'Error 10061 Failed to connect redis server\n'
            self.logger.error(error_message)
        except Exception as e:
            self.logger.exception(e)

        return


if __name__ == '__main__':
    pass