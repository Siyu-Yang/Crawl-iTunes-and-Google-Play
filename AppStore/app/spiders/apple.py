# -*- coding: utf-8 -*-
import scrapy

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from app.items import AppleItem

def crawl_rules():
    # Extract links matching '/genre/ios-***' (but not matching 'letter=')
    # and follow links from them (since no callback means follow=True by default).

    allow_urls = (f"/genre/ios-")

    # please use (1) or (2)

    # (1) this is to check only popular apps on category top page for testing
    app_links = LinkExtractor(allow=('/app/',), deny=('ct=footer',))

    # (2) this is to check category top page plus all sub pages for each letter
    genre_links = LinkExtractor(allow=allow_urls)

    # Extract links matching '/app/' and parse them with the spider's method parse_item
    # also there is a link to Apple Store App in footer which should be skipped

    return (
        Rule(genre_links),
        Rule(app_links, callback='parse_app', follow=False),
    )
    
    
    
    
class AppleSpider(CrawlSpider):
    name = "apple"
    allowed_domains = ["apps.apple.com"]
    start_urls = ['https://apps.apple.com/us/genre/ios-entertainment/id6016','https://apps.apple.com/us/genre/ios-finance/id6015',
    'https://apps.apple.com/us/genre/ios-news/id6009','https://apps.apple.com/us/genre/ios-health-fitness/id6013',
    'https://apps.apple.com/us/genre/ios-productivity/id6007','https://apps.apple.com/us/genre/ios-travel/id6003',
    'https://apps.apple.com/us/genre/ios-medical/id6020','https://apps.apple.com/us/genre/ios-shopping/id6024',
    'https://apps.apple.com/us/genre/ios-business/id6000', 'https://apps.apple.com/us/genre/ios-stickers/id6025',
    'https://apps.apple.com/us/genre/ios-food-drink/id6023','https://apps.apple.com/us/genre/ios-lifestyle/id6012',
    'https://apps.apple.com/us/genre/ios-magazines-newspapers/id6021','https://apps.apple.com/us/genre/ios-games/id6014',
    'https://apps.apple.com/us/genre/ios-navigation/id6010','https://apps.apple.com/us/genre/ios-photo-video/id6008',
    'https://apps.apple.com/us/genre/ios-reference/id6006','https://apps.apple.com/us/genre/ios-social-networking/id6005',
    'https://apps.apple.com/us/genre/ios-sports/id6004','https://apps.apple.com/us/genre/ios-utilities/id6002',
    'https://apps.apple.com/us/genre/ios-weather/id6001', 'https://apps.apple.com/us/genre/ios-catalogues/id6022',
    'https://apps.apple.com/us/genre/ios-developer-tools/id6026', 'https://apps.apple.com/us/genre/ios-education/id6017',
    'https://apps.apple.com/us/genre/ios-music/id6011', 'https://apps.apple.com/us/genre/ios-graphics-design/id6027',
    ] 
    rules = crawl_rules()
    
    def parse_app(self, response):
        # 获取页面的 URL 以及下载数量
        item = AppleItem()
        
        item['name'] = response.xpath('//h1[@class="product-header__title app-header__title"]/text()').extract_first().strip()        
        

        rows = response.xpath('//div[@class="information-list__item l-row"]')

        info_dict = {}

        for row in rows:
            try:
                key = row.xpath('./dt/text()').extract_first().strip()
            except:
                continue

            try:
                value = row.xpath('./dd/text()').extract_first().strip()
            except:
                continue
                
            info_dict[key] = value

        section = response.xpath('//div[@class="section__description"]')
         
        item['description'] = section.xpath('//p[@data-test-bidi=""]/text()').getall()

        item['reviewNumber'] = response.xpath('//p[@class="we-customer-ratings__count medium-hide"]/text()').get()

        try:
            item['reviewNumber'] = item['reviewNumber'].split()[0]
        except:
            pass
        
        item['ratingValue'] = response.xpath('//span[@class="we-customer-ratings__averages__display"]/text()').get()
        
        item['price'] = info_dict["Price"]
        
        item['currentVersion'] = response.xpath('//p[@class = "l-column small-6 medium-12 whats-new__latest__version"]/text()').get()

        try:
            item['currentVersion'] =item['currentVersion'].split()[1]
        except:
            pass


        item['author'] = info_dict["Seller"]
        
        
        yield item 
