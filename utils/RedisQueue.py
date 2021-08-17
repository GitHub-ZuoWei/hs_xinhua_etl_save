# uncompyle6 version 3.5.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.7.3 (default, Mar 27 2019, 17:13:21) [MSC v.1915 64 bit (AMD64)]
# Embedded file name: ../src\utils\RedisQueue.py
# Compiled at: 2018-07-13 11:32:09
u"""
Created on 2018年4月17日

@author: mes
"""
import os, sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import redis, config.Config

class RedisQueue(object):
    """Simple Queue with Redis Backend"""

    def __init__(self, name, namespace='queue', **redis_kwargs):
        """The default connection parameters are: host='localhost', port=6379, db=0"""
        self.db = redis.Redis(host=config.redis_ip, port=6379, db=0, password=config.redis_pwd)
        self.mylist = '%s:%s' % (namespace, name)

    def qsize(self):
        """Return the approximate size of the queue."""
        return self.db.llen(self.mylist)

    def empty(self):
        """Return True if the queue is empty, False otherwise."""
        return self.qsize() == 0

    def put(self, item):
        """Put item into the queue."""
        self.db.rpush(self.mylist, item)

    def setExpire(self, key, time):
        """Put item into the queue."""
        self.db.expire(key, time)

    def get(self, block=True, timeout=None):
        """Remove and return an item from the queue.

        If optional args block is true and timeout is None (the default), block
        if necessary until an item is available."""
        if block:
            item = self.db.blpop(self.mylist, timeout=timeout)
        else:
            item = self.db.lpop(self.mylist)
        if item:
            item = item[1]
        return item

    def get_nowait(self):
        """Equivalent to get(False)."""
        return self.get(False)

    def setAdd(self, item):
        """add item into the set."""
        return self.db.sadd(self.mylist, item)

    def set_ismember(self, item):
        u"""
                判断成员元素是否是集合的成员
                返回值:
                如果member元素是集合的成员，返回1。
                如果member元素不是集合的成员，或key不存在，返回0。
        """
        return self.db.sismember(self.mylist, item)

    def string_set(self, item):
        u"""设置给定 key 的值"""
        return self.db.set(self.mylist, item)

    def string_get(self):
        u"""获取指定 key 的值"""
        return self.db.get(self.mylist)


if __name__ == '__main__':
    siteDateTime_q = RedisQueue('internet_siteDateTime', namespace='string')
    siteDateTime_q.string_set('2018-06-13 15:01:01')
    siteDateTime = siteDateTime_q.string_get()
    print siteDateTime
    library_dbRid_content = RedisQueue('jsfw_zip')
    element = library_dbRid_content.set_ismember('jdw2018_20180428.zip')
    print element