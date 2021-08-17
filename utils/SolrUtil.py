# uncompyle6 version 3.5.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.7.3 (default, Mar 27 2019, 17:13:21) [MSC v.1915 64 bit (AMD64)]
# Embedded file name: ../src\utils\SolrUtil.py
# Compiled at: 2019-03-18 17:45:20
u"""
Created on 2019年1月24日

@author: mes
"""
import pysolr

class SolrUtil(object):
    u"""
    solr工具类
    """

    def __init__(self, solrIp):
        """
        Constructor
        """
        self.solrIp = solrIp
        self.solr = pysolr.Solr(self.solrIp)
        solrCoreAdmin = pysolr.SolrCoreAdmin(self.solrIp)
        print solrCoreAdmin.status()

    def add(self, dataLists):
        u"""
        :param dataLists:list列表，列表元素是dict字典
        example：
        solr.add([
            {
                "id": "doc_1",
                'tableCode': 1000,
            },
            {
                "id": "doc_2",
                'tableCode': 1000,
            },
        ])        
        """
        self.solr.add(dataLists)

    def optimize(self):
        u"""
        You can optimize the index when it gets fragmented, for better speed.
                优化索引，加快索引速度
        """
        self.solr.optimize()

    def search(self, keyword):
        u"""
                关键词搜索
        """
        results = self.solr.search('bananas')
        print ('Saw {0} result(s).').format(len(results))
        for result in results:
            print ("The title is '{0}'.").format(result['title'])

        results = self.solr.search('bananas', **{})
        similar = self.solr.more_like_this(q='id:doc_2', mltfl='text')
        self.solr.delete(id='doc_1')
        self.solr.delete(q='*:*')


if __name__ == '__main__':
    import time
    print 'start search'
    start = time.clock()
    content = '新华社日内瓦４月１３日电财经观察：中国经济结构改革利好全球贸易\n\u3000\u3000新华社记者凌馨\n\u3000\u3000世界贸易组织日前大幅上调今年全球贸易增长预期，并指出中国经济结构改革长期来看将对全球贸易增长提供支撑。贸易专家对此表示，中国经济转型有助于全球经济实现稳定、可持续增长。\n\u3000\u3000世贸组织１２日发布《全球贸易数据与展望》报告，将今年全球贸易增长预期由此前的３．２％上调至４．４％。报告预测，中国从投资驱动向消费拉动转型的经济再平衡，从长期来看有益于实现更强劲的可持续经济增长，并将支持贸易增长。\n\u3000\u3000世贸组织数据显示，从２０１３年到２０１７年，投资对中国国内生产总值增长的贡献率已经从５５％下降到３２％，而消费的比重则大幅提高。\n\u3000\u3000报告撰写人之一、世贸组织经济学家科尔曼·尼强调，中国的经济再平衡是个逐步推进的过程，因此并未引起全球经济震荡或产生干扰。从投资向消费倾斜一方面可以减少和消除对一些需求不足行业的过度投资，另一方面则将进一步提高中国消费者的生活水平。更平衡的发展模式可以避免经济遭受各种冲击，从而支撑稳定的经济增长。\n\u3000\u3000联合国贸易和发展会议经济事务官员梁国勇表示，消费相对于投资在经济增长中作用的增强，意味着经济增长更强的可持续性和包容性，也意味着进口需求的不断扩张。作为世界第二大经济体，中国消费和进口规模的持续扩大将为世界贸易提供源源不断的增长动力。\n\u3000\u3000世贸组织的这份报告显示，２０１７年，全球贸易增速达４．７％，为２０１１年以来最大增幅。同期，中国成为全球第二大进口国和第一大出口国，进出口额分别占全球进出口贸易总额的１０．２％和１２．８％。\n\u3000\u3000尼表示，１９８０年中国进出口只占全球总量的１％，如今中国的经济体量和全球经济参与度均大幅提升，拓宽了全球商品和服务市场，推动了地区和全球贸易需求，让诸多贸易伙伴由此受益。\n\u3000\u3000尼认为，中国对全球经济稳定增长的贡献明显体现在２００８年国际金融危机爆发之后。金融危机首先在发达国家爆发，并重创其经济。而中国在这段时期保持了自身经济的强劲增长，成为对其他国家产品需求的重要来源，这在一定程度上缩小了全球经济萎缩幅度。\n\u3000\u3000尼说，２０１７年是金融危机以来全球经济出现全面复苏的一年，各地区经济普遍向好，传递了非常积极的信号。因此，世贸组织将今年全球贸易增长预期大幅上调，并预测２０１９年全球贸易增速为４．０％。但他同时警告，贸易保护主义可能会让国际贸易付出代价。\n\u3000\u3000世贸组织在报告中也指出，部分经济体间贸易摩擦可能升级，将增加贸易前景的不确定性。\n\u3000\u3000梁国勇表示，改革开放４０年来，中国以贸易和投资为两翼，不断融入世界经济和国际分工体系，成为推进全球化进程的主要力量之一。２００１年，中国加入世贸组织，成为世界贸易和经济发展史上的里程碑事件，极大地推动了全球贸易的高速增长。\n\u3000\u3000梁国勇说，引进外资和扩大出口曾是中国外向型经济发展模式的主要特征，现在中国实施的则是内外平衡、更加均衡的开放。这意味着对外投资和进口在中国经济中的重要性不断提升，也意味着中国在推动全球化、反对逆全球化中的作用不断加强。\n\u3000\u3000梁国勇认为，中国仍是“世界工厂”，并且重要性还在提升，同时，随着消费和进口高速增长，中国也正在成为“世界市场”。（完）'
    keyword = '特征'
    if keyword in content:
        print 'yes'
    end = time.clock()
    print 'Running time: %s Seconds' % (end - start)
    solrUtil = SolrUtil('http://192.168.7.1:8090/solr/new_core')
    solrUtil.add([{}, {}])