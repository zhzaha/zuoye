# -*- coding: utf-8 -*-
import scrapy
from lxml import etree
import time
import json
import re
# from ..items import JingdongItem

class JingSpider(scrapy.Spider):
    name = 'jing'
    # allowed_domains = ['https://search.jd.com/Search?keyword=%E5%A4%A7%E5%9C%B0%E7%93%9C&enc=utf-8&wq=%E5%A4%A7%E5%9C%B0%E7%93%9C&pvid=49c811574e0848b38b835ad2d5d68245']
    # start_urls = ['https://search.jd.com/Search?keyword=%E5%A4%A7%E5%9C%B0%E7%93%9C&enc=utf-8&wq=%E5%A4%A7%E5%9C%B0%E7%93%9C&pvid=49c811574e0848b38b835ad2d5d68245']
    global goods
    goods = input('输入收索内容')
    start_urls = ['https://search.jd.com/Search?keyword='+goods+'&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq='+goods+'&page=' + str(2*n-1) + '&s='+ str(60*(n-2)+55)+'&click=0'for n in range(2,40000)]

    def parse(self, response):
        soup = response.xpath('//li[contains(@class,"gl-item")]')
        for i in soup:
            # 商品价格
            price = i.xpath('div[@class="gl-i-wrap"]/div[@class="p-price"]/strong/i/text()').extract_first()
            # 商品名称
            tatle = ''.join(''.join(
                i.xpath("string(.//div[@class='gl-i-wrap']/div[@class='p-name p-name-type-2']/a)").extract()).split())
            goods_id = i.xpath('@data-sku').extract_first()
            html = 'https://item.jd.com/' + goods_id + '.html'
            yield scrapy.Request(html, self.detail, meta={'goods_id': goods_id, 'price': price, 'tatle': tatle})
        # 动态的30个加入头
        headers = {
            'referer': 'https://search.jd.com/Search?keyword='+goods+'&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq='+goods+'&stock=1&page=5&s=116&click=0'}
        for t in range(2,50):
        # 时间戳
            a = time.time()
        # 固定格式小数点后5个
            b = '%.5f' % a
        # 动态接口
        #       'https://search.jd.com/s_new.php?keyword=%E5%A4%A7%E5%9C%B0%E7%93%9C&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E5%A4%A7%E5%9C%B0%E7%93%9C&stock=1&page=2&s=30&scrolling=y&log_id=' 6 145  4 85  8 205  85+60(n-1)
            url = 'https://search.jd.com/s_new.php?keyword='+goods+'&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq='+goods+'&stock=1&page='+ str(2*t) +'&s='+ str(85 + 60 * (t-1))+'&scrolling=y&log_id='+str(b)

        # url = 'https://search.jd.com/s_new.php?keyword=%E5%A4%A7%E5%9C%B0%E7%93%9C&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E5%A4%A7%E5%9C%B0%E7%93%9C&stock=1&page=2&s=29&scrolling=y&log_id=' + str(b)
        # 传递
            yield scrapy.Request(url, self.parse1, headers=headers)

    def parse1(self, response):
        base_all = response.xpath('//li[contains(@class,"gl-item")]/@data-sku').extract()
        soup = response.xpath('//li[contains(@class,"gl-item")]')
        for i in soup:
            # 商品价格
            price = i.xpath('div[@class="gl-i-wrap"]/div[@class="p-price"]/strong/i/text()').extract_first()
            # 商品名称
            tatle = ''.join(''.join(i.xpath(
                "string(.//div[@class='gl-i-wrap']/div[@class='p-name p-name-type-2']/a)").extract()).split())
            # 商品id
            goods_id = i.xpath('@data-sku').extract_first()
            html = 'https://item.jd.com/' + goods_id + '.html'

            yield scrapy.Request(html, self.detail, meta={'goods_id': goods_id, 'price': price, 'tatle': tatle})

    def detail(self, response):

        tatle = response.meta['tatle']
        goods_id = response.meta['goods_id']
        price = response.meta['price']
        #  name = re.compile('<div class="item ellipsis" title="(.*?)">')        soup = response.xpath("//ul[@class='parameter2 p-parameter-list']/li//text()").extract()

        # tatle = name.findall(response.text)[0]
        # pingpai = response.xpath("//ul[@id='parameter-brand']/li/a/text()").extract_first()
        # print(pingpai)
        # 图片连接
        img_url = response.xpath("//li[@class='img-hover']/img/@src").extract_first()
        soup = response.xpath("//ul[@class='parameter2 p-parameter-list']")

        html = 'https://sclub.jd.com/comment/productPageComments.action?&productId=' + str(goods_id) + '&score=0&sortType=5&page=1&pageSize=10'
        # 评论的链接拼接而成
        for i in soup:
            # 全部的信息
            all_tatle = ''.join(i.xpath("li//text()").extract()).split(',')[0]
            yield scrapy.Request(html, self.comment,meta={"goods_id":goods_id,'price': price, 'tatle': tatle,'img_url':img_url,'all_tatle':all_tatle})
    def comment(self, response):

        all_tatle = response.meta['all_tatle']
        img_url = response.meta['img_url']
        goods_id = response.meta['goods_id']
        price = response.meta['price']
        tatle = response.meta['tatle']
        comment_content_num = re.findall('"commentCountStr":"(.*?)"', response.text, re.S)[0]

        if '万+' in comment_content_num:
            a = comment_content_num[:-2]
            comment_number = int(10000 * float(a)) // 10
            for i in range(comment_number):
                goods_id = response.meta['goods_id']
                comment_html = 'https://sclub.jd.com/comment/productPageComments.action?&productId=' + str(goods_id) + '&score=0&sortType=5&page='+str(i)+'&pageSize=10'
                yield scrapy.Request(comment_html, self.comment_html,meta={'price': price, 'tatle': tatle,'img_url':img_url,'all_tatle':all_tatle})
        elif '+' in comment_content_num:
            a = comment_content_num[:-1]
            comment_number = int(a)//10
            for i in range(comment_number):
                goods_id = response.meta['goods_id']
                comment_html = 'https://sclub.jd.com/comment/productPageComments.action?&productId=' + str(goods_id) + '&score=0&sortType=5&page='+str(i)+'&pageSize=10'
                yield scrapy.Request(comment_html, self.comment_html, meta={'price': price, 'tatle': tatle, 'img_url': img_url,'all_tatle':all_tatle})
    #
        else:
            num = int(comment_content_num)
            if num>9:
                num1 = num//10 +2
                for i in range(num1):
                    goods_id = response.meta['goods_id']
                    comment_html = 'https://sclub.jd.com/comment/productPageComments.action?&productId=' + str(goods_id) + '&score=0&sortType=5&page='+str(i)+'&pageSize=10'
                    yield scrapy.Request(comment_html, self.comment_html,meta={'price': price, 'tatle': tatle, 'img_url': img_url,'all_tatle':all_tatle})
            else:
                goods_id = response.meta['goods_id']
                comment_html = 'https://sclub.jd.com/comment/productPageComments.action?&productId=' + str(goods_id) + '&score=0&sortType=5&page=1&pageSize=10'
                yield scrapy.Request(comment_html, self.comment_html,meta={'price': price, 'tatle': tatle, 'img_url': img_url,'all_tatle':all_tatle})
                # comment_html = 'https://sclub.jd.com/comment/productPageComments.action?&productId=' + str(goods_id) + '&score=0&sortType=5&page='+str(i)+'&pageSize=10'
                # yield scrapy.Request(comment_html, self.comment,meta={'price': price, 'tatle': tatle,'img_url':img_url,'all_tatle':all_tatle})

    def comment_html(self,response):
        all_tatle = response.meta['all_tatle']
        img_url = response.meta['img_url']
        price = response.meta['price']
        tatle = response.meta['tatle']
        # item = JingdongItem()
        comment_all = re.findall(r'"content":"(.*?)"', response.text)
        # for comment in comment_all:
        pinglun = str(comment_all)
        print(pinglun)
        # item['pinglun'] = pinglun
        # item['all_tatle'] = all_tatle
        # item['tatle'] = tatle
        # item['price'] = price
        # item['img_url'] = img_url
        # yield item