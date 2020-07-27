# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 11:35:57 2020

@author: user
"""


import scrapy,time
from scrapy.crawler import CrawlerProcess

class HousePriceSpider(scrapy.Spider):
    name='houseprice'
    pno=30
    def start_requests(self):
        
        url="https://www.99acres.com/rent-property-in-bangalore-ffid-page-1"
        yield scrapy.Request(url=url,callback=self.parse)
        
    def parse(self,response):
        
        for href in response.css('.srpTuple__tupleDetails a::attr(href)').extract():
           url = response.urljoin(href)
           print(url)
           req = scrapy.Request(url, callback=self.parse2)
           time.sleep(5)
           yield req
            
    def parse2(self,response):
        for sel in response.css('html').extract():
            house_prices= {}
            house_prices['Address']=response.xpath('//*[@id="FactTableComponent"]/li[4]/div[2]/text()[2]').extract()
            house_prices['Prices']=response.css('#pdPrice2::text').extract()
            house_prices['Bedrooms']=response.css('#bedRoomNum::text').extract()
            house_prices['SqFt']=response.css('#builtupArea_span::text').extract()
            house_prices['Furnishing']=response.css('#furnishingLabel::text').extract()
        yield house_prices
        
        
        nextpage="https://www.99acres.com/rent-property-in-bangalore-ffid-page-"+str(HousePriceSpider.pno)
    
    
        if HousePriceSpider.pno <=300:
            HousePriceSpider.pno += 1
            yield response.follow(nextpage, callback = self.parse)
        
        
    
    
    
process=CrawlerProcess(settings={"FEEDS":{"House_price.csv":{"format":"csv"},},})
process.crawl(HousePriceSpider) 
process.start()      
