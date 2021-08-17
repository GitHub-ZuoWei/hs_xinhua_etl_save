# uncompyle6 version 3.5.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.7.3 (default, Mar 27 2019, 17:13:21) [MSC v.1915 64 bit (AMD64)]
# Embedded file name: ../src\utils\CommonUtil.py
# Compiled at: 2019-01-20 17:11:04
u"""
Created on 2019年1月20日

@author: 薛清晨
"""

class CommonUtil(object):
    u"""
        公共类工具
    """

    def __init__(self, params):
        """
        Constructor
        """
        pass

    @classmethod
    def merge_two_dicts(self, x, y):
        """
        Given two dicts, merge them into a new dict as a shallow copy.
        """
        z = x.copy()
        z.update(y)
        return z