# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders.crawl import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
import os
from scrapy.selector import Selector
class WurenjiSpider(CrawlSpider):
    name = 'wurenji'
    # allowed_domains = ['www']
    start_urls = ['http://www.81uav.cn/uav-news/4.html']
    rules = (
        # Rule(LinkExtractor(allow=(r'http://www.81uav.cn/uav-news/4_\d+.html')),follow=True),
        Rule(LinkExtractor(allow=(r'http://www.81uav.cn/uav-news/\d+/\d+/\d+.html'),restrict_css=('div.news-list-box a')), callback="parse_items",follow=False),
    )
    def parse_items(self, response):
        aurl = response.url
        try:
            # 标题
            if response.css('body > div.m.mt15 > div.news_left > h1::text'):
                title=response.css('body > div.m.mt15 > div.news_left > h1::text').extract_first()
            else:
                raise Exception('title is none')
            # 时间
            if response.css('div.info::text').re('\d{4}-\d{2}-\d{2}')[0]:
                time=response.css('div.info::text').re('\d{4}-\d{2}-\d{2}')[0]
            else:
                time=''
            # 来源
            if response.css('div.info::text').re('来源：\w+'):
                form = response.css('div.info::text').re('来源：\w+')[0]
                form = form.replace('来源：', '')
            else:
                form = ''
            if response.css('div.info::text').re('作者：.*'):
                author = response.css('div.info::text').re('作者：.*')[0]
                authors = author.replace('作者：', '')
            else:
                authors = ''
            if response.css('body > div.m.mt15 > div.news_left > div.view > div:nth-child(9) > a::text'):
                biaoqian = response.css(
                    'body > div.m.mt15 > div.news_left > div.view > div:nth-child(9) > a::text').extract_first()
            else:
                biaoqian = ''
            if response.css('#article > p > img::attr(src)'):
                img_url = response.css('#article > p > img::attr(src)').extract()
            else:
                img_url = ''
            sel = Selector(response)
            if sel.xpath('//*[@id="article"]//text()'):
                content = ''.join(sel.xpath('//*[@id="article"]//text()').extract()).strip()
                # print(content)
            else:
                content = ''
            if response.css('body > div.m.mt15 > div.news_left > div.view > div:nth-child(7) > a::text'):
                lianjie = response.css('body > div.m.mt15 > div.news_left > div.view > div:nth-child(7) > a::text').extract_first()
            # 'body > div.m.mt15 > div.news_left > div.view > div:nth-child(7) > a'
            else:
                lianjie = ''
            daodu = sel.xpath('//meta[@name="description"]/@content').extract()
            if len(daodu) == 0:
                daodu = 'kong'
            else:
                daodu = daodu[0]
        except Exception as e:
            if not os.path.exists('log'):
                os.mkdir('log')
            with open('log.text',encoding='utf-8')as f:
                f.write('{0}'+'\n'+'{1}'.format(e,aurl))