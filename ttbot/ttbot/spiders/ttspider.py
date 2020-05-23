# -*- coding: utf-8 -*-
import scrapy
from ..items import TtbotItem

class TtspiderSpider(scrapy.Spider):
    name = 'ttspider'
    allowed_domains = ['tiktok.com']
    start_urls = ['https://www.tiktok.com/@shamimaafrinomi?lang=en/']

    def parse(self, response):

        items = TtbotItem()
        items['it'] = "nothing to yield"

        for href in response.css('a::attr(href)').extract():
            file = open("data.txt", 'a+')
            if href.startswith("https://www.tiktok.com/@"):
                file.write(href+"\n")
                yield response.follow(href, callback=self.parse)
            yield items