# uncompyle6 version 3.5.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.7.3 (default, Mar 27 2019, 17:13:21) [MSC v.1915 64 bit (AMD64)]
# Embedded file name: /usr/local/txs/hs_xinhua_etl/utils/RedisClient.py
# Compiled at: 2019-04-10 16:25:15
import redis, os, sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from config import constantConfig as constConfig
from sysConfig.SysConfig import SysConfig
import config.Config

def bytes_to_str(s, encoding='utf-8'):
    """Returns a str if a bytes object is given."""
    if isinstance(s, bytes):
        return s.decode(encoding)
    return s


class RedisClient(object):

    def __init__(self, **redis_kwargs):
        self.redis = redis.Redis(host=config.redis_ip, port=6379, db=0, password=config.redis_pwd)

    def __new__(cls, *args, **kwargs):
        u"""
                保证单例，减少连接数
        """
        if not hasattr(cls, '__instance'):
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def get_all_keys(self, match=None, cursor=0):
        u"""
                遍历队列，获取所有keys，用cursor在keys量大时不会堵塞redis
        """
        result_list = []
        while True:
            iter_result = self.redis.scan(match=match, cursor=cursor)
            cursor = iter_result[0]
            result_list.extend(iter_result[1])
            if cursor == 0:
                return map(bytes_to_str, result_list)

    def get_len(self, args):
        u"""
                获取队列长度，兼容不同类型的获取长度，同时可以批量检测
        """
        len_dict = dict()
        val = None
        if not isinstance(args, str):
            for key in args:
                kind = self.get_kind(key)
                if kind == 'hash':
                    val = self.redis.hlen(key)
                elif kind == 'zset':
                    val = self.redis.zcard(key)
                elif kind == 'list':
                    val = self.redis.llen(key)
                elif kind == 'set':
                    val = self.redis.scard(key)
                len_dict[key] = val

            return len_dict
        dict_len = self.get_len([args])
        return dict_len[args]
        return

    def get_kind(self, args):
        u"""
                获取队列类型，同时兼容批量检测类型
        """
        if isinstance(args, str):
            return bytes_to_str(self.redis.type(args))
        else:
            kind_dict = dict()
            for item in args:
                kind_dict[item] = bytes_to_str(self.redis.type(item))

            return kind_dict

    def batch_fetch(self, name, kind=None, count=1):
        u"""
                批量取，因为保证进程安全，采取迭代弹出，如果是单进程可以批量查然后批量删
        """
        if not kind:
            kind = self.get_kind(name)
        pipe = self.redis.pipeline()
        if kind == 'set':
            while True:
                [ pipe.spop(name=name) for i in range(count) ]
                result = pipe.execute()
                clean_result = set(result) - set([None])
                if clean_result:
                    yield clean_result
                else:
                    break

        elif kind == 'list':
            while True:
                [ pipe.lpop(name=name) for i in range(count) ]
                result = pipe.execute()
                clean_result = set(result) - set([None])
                if clean_result:
                    yield clean_result
                else:
                    break

        return

    def fetch(self, name, kind=None, block=True, timeout=None):
        u"""
                获取
        """
        if not kind:
            kind = self.get_kind(name)
        if kind == 'set':
            return self.redis.spop(name)
        if kind == 'list':
            if block:
                item = self.redis.blpop(name, timeout=timeout)
            else:
                item = self.redis.lpop(name)
            if item:
                item = item[1]
            return item
        if kind == 'string':
            return self.redis.get(name)

    def batch_find(self, name, count=None, kind=None, match=None, cursor=0):
        u"""
                批量查找
        """
        if not kind:
            kind = self.get_kind(name)
        if kind == 'set':
            self.redis.sscan('set1')
            cursor, result = self.redis.sscan(name=name, count=count, cursor=cursor, match=None)
            print result
        return

    def batch_delete(self, name, value, kind=None, count=None):
        u"""
                批量删除
        """
        if not kind:
            kind = self.get_kind(name)
        if kind == 'set':
            self.redis.srem(name, *value)
        elif kind == 'list':
            self.redis.ltrim(name=name, start=count, end=-1)

    def insert(self, name, value, kind=None):
        u"""
                插入
        """
        if not kind:
            kind = self.get_kind(name)
        insert_num = 0
        if kind == 'set':
            insert_num = self.redis.sadd(name, value)
        elif kind == 'list':
            insert_num = self.redis.rpush(name, value)
        elif kind == 'string':
            insert_num = self.redis.set(name, value)
        return insert_num

    def test(self, name, count=None, kind=None, match=None, cursor=0):
        print '================'
        if not kind:
            kind = self.get_kind(name)
        if kind == 'set':
            print 'yes'
            cursor, result = self.redis.sscan(name=name, count=count, cursor=cursor, match=None)
            print cursor
            print result
        return


def xhsTest():
    redisClient = RedisClient()
    xhs_hqbz_name = 'string:xhs_hqbz_title'
    insertFlag = redisClient.insert(xhs_hqbz_name, '西藏军区派出直升机为山体滑坡灾区开辟空中救援通道', kind='string')
    if insertFlag is True:
        print xhs_hqbz_name
        print 'insert success'
    hqbz_title = redisClient.fetch(name=xhs_hqbz_name)
    print 'fetch hqbz_title:'
    print hqbz_title
    xhs_wqzb_name = 'string:xhs_wqzb_title'
    insertFlag = redisClient.insert(xhs_wqzb_name, '美战机巡弋中国南沙岛礁', kind='string')
    if insertFlag is True:
        print xhs_wqzb_name
        print 'insert success'
    wqzb_title = redisClient.fetch(name=xhs_wqzb_name)
    print 'fetch wqzb_title:'
    print wqzb_title


def insertInternetSiteDateTimeTest():
    redisClient = RedisClient()
    internetSiteDateTime = 'string:internet_siteDateTime'
    insertFlag = redisClient.insert(internetSiteDateTime, '2018-10-8 11:30:06', kind='string')
    if insertFlag is True:
        print 'insert success'


if __name__ == '__main__':
    try:
        redisC = RedisClient()
        print redisC.redis.ping()
        result = redisC.redis.sscan(name='queue:zyfw_dbId', cursor=0, count=100000)
        import re
        pattern1 = '(.[a-zA-z\\s]*)book(.[a-zA-z\\s]*)'
        for v in result[1]:
            s = re.search(pattern1, v)
            print s
            if s != None:
                print v
                redisC.redis.srem('queue:zyfw_dbId', v)

    except Exception as e:
        print e