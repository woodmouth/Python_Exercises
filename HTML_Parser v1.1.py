import os
import re

# from bs4 import BeautifulSoup
from lxml import etree

# 我在程序的开头记录一下目前看到的一些很奇怪的bug。
# 原网页：
# https://www.oxfordlearnersdictionaries.com/us/definition/english/accident?q=accident
# 现在正在尝试提取第一个解释和解释下的例句。发现一些很奇怪的bugs。有些例句被跳过了。具体是第二到第四个例句。
# 要研究HTML的源代码。
# 的确是这样，比如第二个解释，前两个例句也被跳过了。不清楚为什么会这样。
# 对于第一个解释，sampleSentences的期望长度应该是11，因为有11个例句.
# 现在知道原因了，当前节点是<span class="x-gs"/>
# 有些例句是<span class="x-gs"><span class="x-g"><span class="x">...
# 但是有些是<span class="x-gs"><span class="x-g"><span class="rx-g"><span class="x">...
# 所以层级不一样。所以还是调整xpath的语句。

'''
class SampleSentence:
    def __init__(self, samples):
        self.samples = samples

class Definition:
    def __init__(self, definitions):
        self.definitions = definitions

class HeadWord:
    def __init__(self, definitions, samples):
        if not isinstance(definitions, Definition):
            raise TypeError('It is not class Definition')
        if not isinstance(samples, SampleSentence)
            raise TypeError
        self.definition = defitions
        self.samples = samples
        self.isOxford3000 = False
'''


if __name__ == '__main__':

    html = open("C:\\Users\\ThinkPad\\Desktop\\oxford\\accident noun.html", "r", encoding="utf-8")

    samples = []
    definition_section = {}  # 用一个简单的数据结构表示词条就足够了。
    headWord = []  # headword是definition_section的列表。
    page = etree.HTML(html.read())

    # 问题的根源在于下面entryContent的赋值，这里的SN-GS没选择好，应该按照这样的路径选择出来：oald/entry/h-g/sn-gs/sn-g/x-gs/x-g
    # 详细的原因在evernote.com里边有写了。2月19日的笔记。我现在研究透网页的标签结构，这个程序就不是这么写了。
    # 可以做到直接选择到所需要的标签节点，不需要遍历了。
    # entryContent = page.xpath("//div[@id='entryContent']")
    page_sn_gs_xpath_string = "//div[@id='entryContent']//ol[@class='h-g']/span[@class='sn-gs']"

    page_SN_GS_list = page.xpath(page_sn_gs_xpath_string)  # 我想起来这个返回有好几个'sn-gs'. 第一个才是真正的解释。
    # page_regular_definitions = page_SN_GS_list[0]

    # 很无语，为什么这里的definition还是6个。明明是2个而已。。。或者我重新构建一个HTML tree。
    # 现在重新构建HTML树就对了。现在是只有两个解释了。那如果这样的话，我就转变思路去build tree了。
    page_regular_definitions = etree.HTML(etree.tostring(page_SN_GS_list[0]))

    page_definition_sections = page_regular_definitions.xpath("//li[@class='sn-g']")
    for page_section in page_definition_sections:
        page_section_etree = etree.HTML(etree.tostring(page_section))
        page_definition = page_section_etree.xpath("//span[@class='def']")
        str0 = page_definition[0].xpath('string(.)')
        print("definition: %s" % (str0))
        # sibling = definition.getnext() # 我期望这个getnext()语句就是返回下一个节点。

        # <span class='x'/>就是例句。
        # sampleSentences = sibling.xpath('./span/span[@class = "x"]') # 怎么把class="x-gs"也匹配上了呢？#这个匹配会遗漏例句
        # sampleSentences = sibling.xpath('//span[@class = "x"]') #直接匹配到例句的节点。这个好点。
        page_sampleSentences = page_section_etree.xpath("//span[@class='x-g']")

        # 现在regular_definitions只有常规的解释。
        samples.clear()
        for page_sample in page_sampleSentences:
            print("-----------------------------------------------")
            print("sentence : %s" % (page_sample.xpath('string(.)')))  # 很奇怪，为什么第二次迭代还是上次的结果？？？
            # 我觉得下面这样的写法不对，因为如果sample.xpath返回失败，它还是保留以前的值。所以还是需要检查返回值。
            # str1 = sample.xpath('string(//span[@class = "x"])')

            # 新写法:
            str1 = page_sample.xpath('string(.)')
            # str1 = sample.xpath('string(//span[@class="x"])') #错误写法。现在试出来了，这个写法不对。前一行的写法才是对的。

            formatted_sentence = re.sub("\s+", " ", str1)
            # 现在很多例句被一些粗体打断了，text中包括了一些<span/>。但是这些标签代表了显示格式，我现在还想不到该如何处理
            # 我已经通过调试模式看到sentence的所有的属性，发现tail也不对。我觉得是LXML的解析不对。我现在看看text的定义。
            str2 = "Formatted Sentence: %s " % (formatted_sentence)
            print(str2)
            samples.append(formatted_sentence)

        # 这里应该用深复制，给列表新增加元素。
        # 下面这样就可以增加字典的元素。
        definition_section['definition'] = str0
        definition_section['samples'] = samples.copy()

        headWord.append(definition_section)

print(headWord)
