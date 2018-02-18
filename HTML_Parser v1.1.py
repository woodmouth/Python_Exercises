import os
import re

# from bs4 import BeautifulSoup
from lxml import etree

if __name__ == '__main__':
    html = open("C:\\Users\\ThinkPad\\Desktop\\oxford\\accident noun.html", "r", encoding="utf-8")
    page = etree.HTML(html.read())
    SN_GS_list = page.xpath("//span[@class='sn-gs']") # 我想起来这个返回有好几个'sn-gs'. 第一个才是真正的解释。
    regular_definitions = SN_GS_list[0]
    definitions = regular_definitions.xpath("//span[@class='def']")
    sibling = definitions[0].getnext()

    # <span class='x'/>就是例句。
    sampleSentences = sibling.xpath('./span/span[@class = "x"]') # 怎么把class="x-gs"也匹配上了呢？

    # 现在regular_definition[0]只有常规的解释。
    for sample in sampleSentences:
        print("-----------------------------------------------")
        print("etree.tostring: %s" % (etree.tostring(sample)))
        print("sentence : %s" % (sample.xpath('string(.)')))# 很奇怪，为什么第二次迭代还是上次的结果？？？
        # 我觉得下面这样的写法不对，因为如果sample.xpath返回失败，它还是保留以前的值。所以还是需要检查返回值。
        # str1 = sample.xpath('string(//span[@class = "x"])')

        # 新写法：//依旧不对。感觉
        str1 = sample.xpath('string(.)')
        # str1 = sample.xpath('string(//span[@class="x"])') #错误写法。现在试出来了，这个写法不对。前一行的写法才是对的。
        
        formatted_sentence_one = re.sub("\s+", " ", str1)
        # 现在很多例句被一些粗体打断了，text中包括了一些<span/>。但是这些标签代表了显示格式，我现在还想不到该如何处理
        # 我已经通过调试模式看到sentence的所有的属性，发现tail也不对。我觉得是LXML的解析不对。我现在看看text的定义。
        str2 = "Formatted Sentence: %s " % (formatted_sentence_one)
        print(str2)

