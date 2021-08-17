#!/usr/bin/env python
# encoding: utf-8
# 如果觉得不错，可以推荐给你的朋友！http://tool.lu/pyc
'''
Created on 2018\xe5\xb9\xb44\xe6\x9c\x8819\xe6\x97\xa5

@author: mes
'''
import urllib
import urllib2
import os
import requests
import re
import codecs


class FileUtil(object):
    def __init__(self):
        pass

    def getResponseData(self, url):
        res_data = urllib2.urlopen(url)
        res_code = res_data.getcode()
        if res_code == 200:
            return res_data
        return None

    getResponseData = classmethod(getResponseData)

    def getResponse_requests(self, url):
        res = requests.get(url, stream=True)
        if res.status_code == 200:
            return res
        return None

    getResponse_requests = classmethod(getResponse_requests)

    def mkdir(self, path):
        path = path.strip()
        path = path.rstrip('\\')
        isExists = os.path.exists(path)
        if not isExists:
            os.makedirs(path)
            return True
        return None

    mkdir = classmethod(mkdir)

    def strTransToObject(self, strData):
        '''
                \xe5\xb0\x86\xe5\xad\x97\xe7\xac\xa6\xe4\xb8\xb2\xe8\xbd\xac\xe6\x88\x90\xe7\x9b\xb8\xe5\xba\x94\xe7\x9a\x84\xe5\xaf\xb9\xe8\xb1\xa1\xef\xbc\x88\xe5\xa6\x82list\xe3\x80\x81tuple\xe3\x80\x81dict\xe5\x92\x8cstring\xe4\xb9\x8b\xe9\x97\xb4\xe7\x9a\x84\xe8\xbd\xac\xe6\x8d\xa2\xef\xbc\x89
                \xe8\xbf\x99\xe7\xa7\x8d\xe6\x96\xb9\xe6\xb3\x95\xe5\xaf\xb9\xe6\x95\xb0\xe6\x8d\xae\xe8\xa6\x81\xe6\xb1\x82\xe6\xaf\x94\xe8\xbe\x83\xe4\xb8\xa5\xe6\xa0\xbc,\xe5\xbb\xba\xe8\xae\xae\xe4\xbd\xbf\xe7\x94\xa8json.loads
        '''
        return eval(strData)

    strTransToObject = classmethod(strTransToObject)

    def remove_emoji(self, text):
        emoji_pattern = re.compile(
            u'(\xed\xa0\xbd[\xed\xb8\x80-\xed\xb9\x8f])|(\xed\xa0\xbc[\xed\xbc\x80-\xef\xbf\xbf])|(\xed\xa0\xbd[\x00-\xed\xb7\xbf])|(\xed\xa0\xbd[\xed\xba\x80-\xed\xbb\xbf])|(\xed\xa0\xbc[\xed\xb7\xa0-\xed\xb7\xbf])+',
            flags=re.UNICODE)
        return emoji_pattern.sub('', text)

    remove_emoji = classmethod(remove_emoji)

    def open_dict(self, filePath):
        '''
        # \xe6\x89\x93\xe5\xbc\x80\xe8\xaf\x8d\xe5\x85\xb8\xe6\x96\x87\xe4\xbb\xb6\xef\xbc\x8c\xe8\xbf\x94\xe5\x9b\x9e\xe5\x88\x97\xe8\xa1\xa8
        :param filePath:
        '''
        dictionary = open(filePath, 'r')
        wordList = []
        flag = 0
        for word in dictionary:
            if flag == 0:
                if word[:3] == codecs.BOM_UTF8:
                    word = word[3:]
                flag = 1
            word = word.strip('\n')
            wordList.append(word)

        return wordList

    open_dict = classmethod(open_dict)


if __name__ == '__main__':
    print FileUtil.getResponse_requests(
        'http://127.0.0.1:8081/flushStaticData?keys=countrys')
__doc__ = '\nCreated on 2018\xe5\xb9\xb44\xe6\x9c\x8819\xe6\x97\xa5\n\n@author: mes\n'
import urllib
import urllib2
import os
import requests
import re
import codecs


class FileUtil(object):
    def __init__(self):
        pass

    def getResponseData(self, url):
        res_data = urllib2.urlopen(url)
        res_code = res_data.getcode()
        if res_code == 200:
            return res_data
        return None

    getResponseData = classmethod(getResponseData)

    def getResponse_requests(self, url):
        res = requests.get(url, stream=True)
        if res.status_code == 200:
            return res
        return None

    getResponse_requests = classmethod(getResponse_requests)

    def mkdir(self, path):
        path = path.strip()
        path = path.rstrip('\\')
        isExists = os.path.exists(path)
        if not isExists:
            os.makedirs(path)
            return True
        return None

    mkdir = classmethod(mkdir)

    def strTransToObject(self, strData):
        '''
                \xe5\xb0\x86\xe5\xad\x97\xe7\xac\xa6\xe4\xb8\xb2\xe8\xbd\xac\xe6\x88\x90\xe7\x9b\xb8\xe5\xba\x94\xe7\x9a\x84\xe5\xaf\xb9\xe8\xb1\xa1\xef\xbc\x88\xe5\xa6\x82list\xe3\x80\x81tuple\xe3\x80\x81dict\xe5\x92\x8cstring\xe4\xb9\x8b\xe9\x97\xb4\xe7\x9a\x84\xe8\xbd\xac\xe6\x8d\xa2\xef\xbc\x89
                \xe8\xbf\x99\xe7\xa7\x8d\xe6\x96\xb9\xe6\xb3\x95\xe5\xaf\xb9\xe6\x95\xb0\xe6\x8d\xae\xe8\xa6\x81\xe6\xb1\x82\xe6\xaf\x94\xe8\xbe\x83\xe4\xb8\xa5\xe6\xa0\xbc,\xe5\xbb\xba\xe8\xae\xae\xe4\xbd\xbf\xe7\x94\xa8json.loads
        '''
        return eval(strData)

    strTransToObject = classmethod(strTransToObject)

    def remove_emoji(self, text):
        emoji_pattern = re.compile(
            u'(\xed\xa0\xbd[\xed\xb8\x80-\xed\xb9\x8f])|(\xed\xa0\xbc[\xed\xbc\x80-\xef\xbf\xbf])|(\xed\xa0\xbd[\x00-\xed\xb7\xbf])|(\xed\xa0\xbd[\xed\xba\x80-\xed\xbb\xbf])|(\xed\xa0\xbc[\xed\xb7\xa0-\xed\xb7\xbf])+',
            flags=re.UNICODE)
        return emoji_pattern.sub('', text)

    remove_emoji = classmethod(remove_emoji)

    def open_dict(self, filePath):
        '''
        # \xe6\x89\x93\xe5\xbc\x80\xe8\xaf\x8d\xe5\x85\xb8\xe6\x96\x87\xe4\xbb\xb6\xef\xbc\x8c\xe8\xbf\x94\xe5\x9b\x9e\xe5\x88\x97\xe8\xa1\xa8
        :param filePath:
        '''
        dictionary = open(filePath, 'r')
        wordList = []
        flag = 0
        for word in dictionary:
            if flag == 0:
                if word[:3] == codecs.BOM_UTF8:
                    word = word[3:]
                flag = 1
            word = word.strip('\n')
            wordList.append(word)

        return wordList

    open_dict = classmethod(open_dict)


if __name__ == '__main__':
    print FileUtil.getResponse_requests(
        'http://127.0.0.1:8081/flushStaticData?keys=countrys')