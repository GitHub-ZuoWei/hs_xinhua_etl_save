# uncompyle6 version 3.5.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.7.3 (default, Mar 27 2019, 17:13:21) [MSC v.1915 64 bit (AMD64)]
# Embedded file name: ../src\utils\ZipUtil.py
# Compiled at: 2018-07-13 09:21:42
u"""
Created on 2018年4月19日

@author: mes
"""
import urllib, os, os.path, zipfile
from zipfile import *
import sys

class ZipUtil(object):
    u"""
    Zip文件处理类
    """

    def __init__(self, filename, mode='r', basedir=''):
        self.filename = filename
        self.mode = mode
        if self.mode in ('w', 'a'):
            self.zfile = zipfile.ZipFile(filename, self.mode, compression=zipfile.ZIP_DEFLATED)
        else:
            self.zfile = zipfile.ZipFile(filename, self.mode)
        self.basedir = basedir
        if not self.basedir:
            self.basedir = os.path.dirname(filename)

    def addfile(self, path, arcName=None):
        u"""
        path为需要压缩的文件
        arcName为压缩后的文件名，可以为空
        """
        self.zfile.write(path, arcName)

    def addfiles(self, paths):
        for path in paths:
            if isinstance(path, tuple):
                self.addfile(*path)
            else:
                self.addfile(path)

    def close(self):
        self.zfile.close()

    def extract_to(self, path):
        u"""
                解析zip文件到指定文件夹
        """
        for p in self.zfile.namelist():
            try:
                self.extract(p, path)
            except Exception as e:
                pass

    def extract(self, filename, path):
        if not filename.endswith('/'):
            f = path + '/' + filename.replace('\\', '/')
            dir = os.path.dirname(f)
            if not os.path.exists(dir):
                os.makedirs(dir)
            file(f, 'wb').write(self.zfile.read(filename))


if __name__ == '__main__':
    pass