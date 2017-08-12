# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Spider
from amazoncrawler.items import AmazoncrawlerItem
from scrapy.selector import Selector
from scrapy.http import Request
import re

class BookSelector(Selector):
    global link
    def link(self,path):
        link = (
            self.xpath(path + '/@href')
            .extract_first()
            .strip()
            )
        return link

    global price
    def price(self,path):
        currency = (
            self.xpath(path + '/span/@class')
            .extract_first(default='')[-3:]
            )
        value = (
            self.xpath(path + '/text()')
            .extract_first(default='NA')
            )
        return currency + value
        
    global text
    def text(self,path):
        text = (
                self.xpath(path + '//text()')
                .extract_first(default='NA')
                .strip()
            )
        return text

    global rating
    def rating(self,path):
         return text(self,path)[:3]

    def extract_tag(self,method,path):
        path = './/' + path
        return method(self,path)

class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    allowed_domains = ['amazon.in', 'amazon.com']
    start_urls = []

    def __init__(self,country='',*args,**kwargs):
        super(AmazonSpider, self).__init__(*args, **kwargs)
        domain = 'com' if country.lower()=='us' else 'in'
        self.start_urls = [
            'http://www.amazon.%s/gp/bestsellers/books/' % domain,
            ]
        print self.start_urls[0]

    def parse(self,response):
        sel = BookSelector(response)
        for category in sel.xpath('//ul[@id="zg_browseRoot"]/ul//a'):
            cat_link = category.xpath('./@href').extract_first()
            cat_name = category.extract_tag(text,'.')
            for page in xrange(1,6):
                url = '%s/?&pg=%s&ajax=1' % (cat_link,page)
                request = Request(url, callback=self.parse_page)
                request.meta['category'] = cat_name
                yield request

    def parse_page(self,response):
        cel = BookSelector(response)
        domain = self.start_urls[0]
        for book in cel.xpath('//div[@class="zg_itemImmersion"]'):
            test_string = "Test String"
            lnk = book.extract_tag(link,'a')
            lnk = re.sub('/gp.*','',domain) + lnk[:lnk.find('?')]
            item = {
                'category' : response.meta['category'],
                'author' : book.extract_tag(text,'div[@class="a-row a-size-small"]'),
                'reviews_count' : book.extract_tag(text,'a[@class="a-size-small a-link-normal"]'),
                'price' : book.extract_tag(price,'span[@class="p13n-sc-price"]'),
                'link' : lnk,
                'title' : book.extract_tag(text, 'div[@aria-hidden="true"]'),
                'rating' : book.extract_tag(rating, 'a//span'),
                    }
            yield item
