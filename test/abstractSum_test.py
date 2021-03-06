# uncompyle6 version 3.5.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.5 (default, Apr 19 2019, 17:01:24) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: ../src\test\abstractSum_test.py
# Compiled at: 2019-01-17 14:44:43
import sys, os
from textteaser import TextTeaser
title = '全球热点:第二次“金特会”在望 半岛和平期待新进展'
text = '韩国总统文在寅10日在新年记者会上表示，期待朝美领导人第二次会晤在近期举行。他还说，朝鲜最高领导人金正恩近日访华，对可能的朝美领导人第二次会晤将起到积极作用。\n分析人士认为，朝美之间的谈判如果不能取得突破，韩朝之间诸多工作也难以推进。朝美双方目前仍有保持接触和对话的动力，有关各方必须一道努力，直面下阶段更艰巨、更实质性的难题。\n【新闻事实】\n文在寅当天在青瓦台举行的新年记者会上说，中国在朝鲜半岛无核化进程中发挥了积极而重要的作用。\n他还说，期待朝美领导人第二次会晤在近期举行，同时期待金正恩在朝美领导人会晤后访问首尔。\n文在寅表示，缺乏互信是朝美无核化对话目前面临的关键难题。他呼吁朝美双方在无核化对话中采取相对应的措施。朝方需要进一步做出无核化实际举措，同时也必须考虑相对应的对朝措施，以推动无核化进程。\n金正恩8日在与中国领导人的会谈中表示，去年朝鲜半岛形势出现缓和，中方为此发挥的重要作用有目共睹，朝方高度赞赏并诚挚感谢。朝方将继续坚持无核化立场，通过对话协商解决半岛问题，为朝美领导人第二次会晤取得国际社会欢迎的成果而努力。希望有关方重视并积极回应朝方合理关切，共同推动半岛问题得到全面解决。\n【深度分析】\n复旦大学朝鲜韩国研究中心主任郑继永认为，金正恩访华重要任务之一是与身为半岛问题关键方之一的中方就半岛无核化进程协调立场。\n郑继永说，与首次会晤不同，朝美领导人第二次会晤必须切入更实质性的问题，朝方也将面对“深水区”。除了无核化进程清单内容、如何核验等技术层面难题，双方更大的难点在于构建互信的进程将如何延续、如何保持住对话势头。\n郑继永还说，朝方认为，截至目前美方的善意回应非常少，而美方在短期内解除对朝制裁也不容易，为了落实经济建设之需、解决民生发展之困，朝鲜除了提振内需，还需通过同中国、韩国发展友好关系，推动其经济发展。\n【即时评论】\n春去春又来。朝鲜半岛自去年春天释出暖意，又快走完一个四季轮回。在中朝及有关方共同努力下，半岛问题政治解决进程取得重大进展。\n一年之计在于春。当前，半岛和平对话的大势已经形成，谈下去并谈出成果成为国际社会普遍期待和共识。希望相关各方以诚固信，相向而行，计天下利，不要错失政治解决半岛问题的历史机遇。\n【背景链接】\n朝鲜半岛局势在2018年发生重要的积极变化。朝韩领导人先后三次举行会晤，半岛南北关系实现缓和；2018年6月，美国总统特朗普与金正恩在新加坡举行首次会晤并签署联合声明。\n此后，朝美无核化谈判陷入僵局。美国要求朝鲜先弃核，而朝鲜寻求美国先放松制裁、同意正式结束朝鲜战争。\n金正恩今年1月1日在新年贺词中强调实现半岛完全无核化的坚定意志，并表示随时准备和美国总统再次举行会谈。\n特朗普6日表示，美朝正在就双方领导人第二次会晤地点进行协商。（参与记者：耿学鹏、田明、杜白羽、郭洋；编辑：孙浩）'
stopWordsPath = os.path.dirname(os.path.abspath(__file__)) + '/textteaser/trainer/stopWords.txt'
tt = TextTeaser(stopWordsPath, text)
sentences = tt.summarize(title, text)
for sentence in sentences:
    print sentence