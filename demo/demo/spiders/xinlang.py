# -*- coding: utf-8 -*-
import scrapy
import re
import newspaper
class XinlangSpider(scrapy.Spider):
    name = 'xinlang'
    start_urls = ['https://cre.mix.sina.com.cn/api/v3/get?callback=jQuery111206736703070287804_1543493107479&cateid=1z&cre=tianyi&mod=pctech&merge=3&statics=1&length=15&up=0&down=0&tm=1543493107&action=0&top_id=%2CA1u1J%2CA1rkN%2CA1s5b%2CA1mJl%2CA1PbX%2CA1MSP%2CA1fbh%2CA1Rzi%2CA1MWO%2CA1MEd%2C%2C9Eux1%2C%2C&offset=0&ad=%7B%22rotate_count%22%3A100%2C%22platform%22%3A%22pc%22%2C%22channel%22%3A%22tianyi_pctech%22%2C%22page_url%22%3A%22https%3A%2F%2Ftech.sina.com.cn%2F%22%2C%22timestamp%22%3A1543493107663%7D&_=1543493107480']
    def parse(self, response):
        url_all = re.findall('"surl":"(.*?)"',response.text,re.S)
        for url in url_all:
            url = url.replace('\\','')
            yield scrapy.Request(url,self.detail)
    def detail(self,response):
        title = response.xpath("//h1[@class='art_tit_h1']/text()").extract_first()
        new = newspaper.Article(url=response.url,language='zh')
        new.download()
        new.parse()
        b = re.sub('\s|\W', '', new.text)
        img_url = response.xpath("//img[@class='art_img_mini_img j_fullppt_cover finpic']/@src").extract()
        time = re.findall('	<meta property="article:published_time" content="(.*?)" />',response.text,re.S)[0]
        # if len(time)==0:
        time1 = response.xpath("//time[@class='art_time']/text()").extract()
        laiyuan = re.findall('	<meta property="article:author" content="(.*?)"/>',response.text,re.S)[0]
        # time = response.xpath("//time[@class='weibo_time']//text()").extract()[1:]
        # time = time.replace('\t\n')
        print(time1,time,response.url,laiyuan)