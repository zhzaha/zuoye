# -*- coding: utf-8 -*-
import scrapy
import re
import newspaper

class Xinwen(scrapy.Spider):
    name = 'xinwen'
    # allowed_domains = ['http://tech.163.com/special/00097UHL/tech_datalist_02.js?callback=data_callback']
    start_urls = ['http://tech.163.com/special/00097UHL/tech_datalist_0'+str(i)+'.js?callback=data_callback' for i in range(2,4)]

    def parse(self, response):
        url_all = re.findall(r'"docurl":"(.*?)"', response.text, re.S)
        for url in url_all:
            if 'photoview' not in url:
                yield scrapy.Request(url,self.detaile)
            else:
                pass
    def detaile(self,response):
        #标题
        if re.findall('<title>(.*?)</title>',response.text,re.S)[0]:
            title = re.findall('<title>(.*?)</title>',response.text,re.S)[0]
            print(title)
        else:
            pass
        # 来源
        form = response.xpath("//a[@id='ne_article_source']/text()").extract_first()
        # 时间  2018-11-28T19:31:51+08:00
        time = re.findall('<meta property="article:published_time" content="(.*?)">',response.text,re.S)[0]
        time = time.replace('T',' ').split('+')[0]
        #作者
        author = response.xpath("//span[@class='ep-editor']/text()").extract_first()
        # print(author)
        #图片
        img = response.xpath("//div[@id='endText']/p[@class='f_center']/img/@src").extract()
        if img is not []:
            for i in img:
                print(i)
        else:
            pass
        #内容xpath 和正则两种
        content = response.xpath("//div[@class='post_body']/div[@id='endText']/p/text()")
        new = newspaper.Article(url=response.url, language='zh')
        new.download()
        new.parse()
        a = re.sub('\s|\W', '', new.text)
        # print(content)
        # print(a)
        # 关键字
        key_word = re.findall('<meta name="keywords" content="(.*?)"/>',response.text,re.S)[0]
        print(key_word)
        #导读
        daodu = re.findall('<meta name="description" content="(.*?)"/>',response.text,re.S)[0]
        print(daodu)

# 单py
# from lxml import etree
# import re
# import requests
# import newspaper,re
# from newspaper import Article
# import time
# # for i in range
# print('haole' )
# url = 'http://tech.163.com/special/00097UHL/tech_datalist_02.js?callback=data_callback'
# response = requests.get(url).text
# # print(response)
# #标题
# title = re.findall(r'"title":"(.*?)"',response,re.S)
# #详情页url
# url = re.findall(r'"docurl":"(.*?)"',response,re.S)
# #关键字
# key_word = re.findall(r'"keyname":"(.*?)"',response,re.S)
# for i in url:
#     if 'photoview' in i:
#         pass
#     else:
#         response = requests.get(i)
#         soup = etree.HTML(response.text)
#         #来源
#         form = soup.xpath("//a[@id='ne_article_source']/text()")[0]
#         # 时间  2018-11-28T19:31:51+08:00
#         time = re.findall('<meta property="article:published_time" content="(.*?)">',response.text,re.S)[0]
#         time = time.replace('T',' ').split('+')[0]
#         #作者
#         author = soup.xpath("//span[@class='ep-editor']/text()")[0]
#         print(form)
#         #图片
#         img = soup.xpath("//div[@id='endText']/p[@class='f_center']/img/@src")
#         if img is not []:
#             for i in img:
#                 print(i)
#         else:
#             pass
#         #内容xpath 和正则两种
#         content = soup.xpath("//div[@class='post_body']/div[@id='endText']/p/text()")
#         new = newspaper.Article(url=i, language='zh')
#         new.download()
#         new.parse()
#         a = re.sub('\s|\W', '', new.text)
#         # print(content)
#         # print(a)
#         # 关键字
#         key_word = re.findall('<meta name="keywords" content="(.*?)"/>',response.text,re.S)[0]
#         #