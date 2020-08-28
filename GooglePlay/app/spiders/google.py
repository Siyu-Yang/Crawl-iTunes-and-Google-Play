# -*- coding: utf-8 -*-
import scrapy

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from app.items import GoogleItem


class GoogleSpider(CrawlSpider):
    name = "google"
    allowed_domains = ["play.google.com"]
    start_urls = [
        'http://play.google.com/',
        'https://play.google.com/store/apps/details?id=com.viber.voip'
    ]
    rules = [
        Rule(LinkExtractor(allow=("https://play\.google\.com/store/apps/details", )), callback='parse_app',follow=True),
    ] #  CrawlSpider 会根据 rules 规则爬取页面并调用函数进行处理

    
    def parse_app(self, response):
        # 获取页面的 URL 以及下载数量
        item = GoogleItem()
        item['name'] = response.xpath('//h1[@class = "AHFaub"]/span/text()').get()
        item['description'] = response.xpath('//div[@jsname="sngebd"]/text()').getall()
        item['reviewNumber'] = response.xpath('//span [@class = "AYi5wd TBRnV"]/span[@aria-label]/text()').get()
        item['ratingValue'] = response.xpath('//div[@class="BHMmbe"]/text()').get()
        item['price'] = response.xpath('//meta[@itemprop="price"]/@content').get()
        item['currentVersion'] = response.xpath('//span[@class="htlgb"]/text()').getall()[3]
        item['downloadsNumber'] =  response.xpath('//span[@class="htlgb"]/text()').getall()[2]
        item['author'] = response.xpath('//span[@class="htlgb"]/text()').getall()[-1]
        
        
        yield item 
