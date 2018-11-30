# -*- coding: utf-8 -*-
import scrapy
import newspaper
from scrapy.spiders import Rule,CrawlSpider
from scrapy.selector import Selector
import re
# from scrapy.http import HtmlResponse
from scrapy.linkextractors import LinkExtractor
class DayinhuSpider(CrawlSpider):
    name = 'dayinhu'
    # allowed_domains = ['www.']
    start_urls = ['http://www.dayinhu.com/news/category/科技前沿']
    rules = (
        # "//div[@class='na_detail clearfix ']/div[@class='news_title']/h3/a/@href"
        Rule(LinkExtractor(allow='http://www.dayinhu.com/news/category/%E7%A7%91%E6%8A%80%E5%89%8D%E6%B2%BF/page/2', ),follow=True),
        Rule(LinkExtractor(allow='http://www.dayinhu.com/news/\d{6}.html',restrict_css=("h1.entry-title a")),callback='parse_item', follow=False),
#sel.css("div.n_detail.clear h3 a::attr(href)")
    )
    def parse_item(self, response):
        sel = Selector(response)

        try:
            #正文
            new = newspaper.Article(url=response.url, language='zh')
            new.download()
            new.parse()
            content = re.sub('\s|\W', '', new.text)
            print(content)
            # 标题
            if sel.xpath("//h1[@class='entry-title']/text()").extract_first():
                title = sel.xpath("//h1[@class='entry-title']/text()").extract_first()
                # print(title)
            else:
                pass
            #时间
            if sel.xpath("//a[1]/time[@class='entry-date']").extract_first():
                time = sel.xpath("//a[1]/time[@class='entry-date']//text()").extract_first()
                # print(time)
            else:
                pass
            #img图片url
            if sel.xpath("//img[@class='aligncenter size-full wp-image-1142']/@src").extract_first():
                img_url = sel.xpath("//img[@class='aligncenter size-full wp-image-1142']/@src").extract()
                for url in img_url:
                    print(url)
            else:
                pass
            #来源
            if sel.xpath("//div[@class='entry-content']/p/text()").extract():
                #内容来源一起
                content = sel.xpath("//div[@class='entry-content']/p/text()").extract()
                if '来源' in content[-1]:
                    print(content[-1])
                    # print(content,response.url)
                else:
                    pass
            else:
                pass
            print(response.url)

        except:
            pass