# uncompyle6 version 3.5.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.7.3 (default, Mar 27 2019, 17:13:21) [MSC v.1915 64 bit (AMD64)]
# Embedded file name: ../src\utils\TimeUtil.py
# Compiled at: 2019-08-06 19:50:34
u"""
Created on 2018年5月31日

@author: 薛清晨
"""
import datetime, time

class TimeUtil(object):

    def __init__(self):
        pass

    @classmethod
    def calDataTime(self, calData, diffDays):
        u"""
                日期相加减(按天)
        """
        if isinstance(calData, datetime.datetime):
            return calData + datetime.timedelta(days=diffDays)
        raise TypeError('calData is not type datetime.datetime\n')

    @classmethod
    def ISOString2Time(self, s):
        u"""
        convert a ISO format time to second 
        from:2006-04-12 16:46:40 to:23123123 
                把一个时间转化为秒 
        """
        d = datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
        return time.mktime(d.timetuple())

    @classmethod
    def Time2ISOString(self, s):
        u"""
        convert second to a ISO format time 
        from: 23123123 to: 2006-04-12 16:46:40 
                把给定的秒转化为定义的格式 
        """
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(s)))

    @classmethod
    def isVaildDate(self, date):
        u"""
                校验时间规则，多加一个长度判断，因为solr中对于date日期严格。
                例如："2019-08-4 16:58:00" ，solr识别出不是date格式
        """
        try:
            if ':' in date:
                time.strptime(date, '%Y-%m-%d %H:%M:%S')
                if len(date) != 19:
                    return False
            else:
                time.strptime(date, '%Y-%m-%d')
                if len(date) != 10:
                    return False
            return True
        except:
            return False


if __name__ == '__main__':
    newsTimeOfDateTime = datetime.datetime.strptime('2018-10-05 00:00:00', '%Y-%m-%d %H:%M:%S')
    date_text = '2019-08-04   16:58:00'
    print TimeUtil.isVaildDate(date_text)