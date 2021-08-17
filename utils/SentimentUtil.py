# uncompyle6 version 3.5.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.7.3 (default, Mar 27 2019, 17:13:21) [MSC v.1915 64 bit (AMD64)]
# Embedded file name: ../src\utils\SentimentUtil.py
# Compiled at: 2019-02-26 14:30:57
u"""
Created on 2019年2月26日

@author: mes
"""
import jieba, numpy as np
from FileUtil import FileUtil
import config.Config, sys
reload(sys)
sys.setdefaultencoding('utf8')

class SentimentUtil(object):

    def __init__(self):
        self.deny_word = FileUtil.open_dict(config.denyWordFilePath)
        self.posdict = FileUtil.open_dict(config.posWordFilePath)
        self.negdict = FileUtil.open_dict(config.negWordFilePath)
        self.degree_word = FileUtil.open_dict(config.degreeWordFilePath)
        self.mostdict = self.degree_word[self.degree_word.index('extreme') + 1:self.degree_word.index('very')]
        self.verydict = self.degree_word[self.degree_word.index('very') + 1:self.degree_word.index('more')]
        self.moredict = self.degree_word[self.degree_word.index('more') + 1:self.degree_word.index('ish')]
        self.ishdict = self.degree_word[self.degree_word.index('ish') + 1:self.degree_word.index('last')]

    def sentiment_score_list(self, data):
        count1 = []
        segtmp = jieba.lcut(data.replace(' ', '，'), cut_all=False)
        i = 0
        a = 0
        poscount = 0
        poscount2 = 0
        poscount3 = 0
        negcount = 0
        negcount2 = 0
        negcount3 = 0
        for word in segtmp:
            if word in self.posdict:
                poscount += 1
                c = 0
                for w in segtmp[a:i]:
                    if w in self.mostdict:
                        poscount *= 4.0
                    elif w in self.verydict:
                        poscount *= 3.0
                    elif w in self.moredict:
                        poscount *= 2.0
                    elif w in self.ishdict:
                        poscount *= 0.5
                    elif w in self.deny_word:
                        c += 1

                if self.judgeodd(c) == 'odd':
                    poscount *= -1.0
                    poscount2 += poscount
                    poscount = 0
                    poscount3 = poscount + poscount2 + poscount3
                    poscount2 = 0
                else:
                    poscount3 = poscount + poscount2 + poscount3
                    poscount = 0
                a = i + 1
            elif word in self.negdict:
                negcount += 1
                d = 0
                for w in segtmp[a:i]:
                    if w in self.mostdict:
                        negcount *= 4.0
                    elif w in self.verydict:
                        negcount *= 3.0
                    elif w in self.moredict:
                        negcount *= 2.0
                    elif w in self.ishdict:
                        negcount *= 0.5
                    elif w in self.degree_word:
                        d += 1

                if self.judgeodd(d) == 'odd':
                    negcount *= -1.0
                    negcount2 += negcount
                    negcount = 0
                    negcount3 = negcount + negcount2 + negcount3
                    negcount2 = 0
                else:
                    negcount3 = negcount + negcount2 + negcount3
                    negcount = 0
                a = i + 1
            elif word == '！' or word == '!':
                for w2 in segtmp[::-1]:
                    if w2 in self.posdict:
                        poscount3 += 2
                    elif w2 in self.negdict:
                        negcount3 += 2
                    else:
                        poscount3 += 0
                        negcount3 += 0

            else:
                poscount3 = 0
                negcount3 = 0
            i += 1
            pos_count = 0
            neg_count = 0
            if poscount3 < 0 and negcount3 > 0:
                neg_count += negcount3 - poscount3
                pos_count = 0
            elif negcount3 < 0 and poscount3 > 0:
                pos_count = poscount3 - negcount3
                neg_count = 0
            elif poscount3 < 0 and negcount3 < 0:
                neg_count = -pos_count
                pos_count = -neg_count
            else:
                pos_count = poscount3
                neg_count = negcount3
            count1.append([pos_count, neg_count])

        return count1

    def sentiment_score(self, senti_score_list):
        score_array = np.array(senti_score_list)
        Pos = np.sum(score_array[:, 0])
        Neg = np.sum(score_array[:, 1])
        res = Pos - Neg
        if res > 0:
            return 1
        else:
            if res < 0:
                return -1
            return 0

    def judgeodd(self, num):
        if num % 2 == 0:
            return 'even'
        else:
            return 'odd'


if __name__ == '__main__':
    sentimentUtil = SentimentUtil()
    print sentimentUtil.sentiment_score(sentimentUtil.sentiment_score_list('中国以毒品走私判处加拿大人死刑'))