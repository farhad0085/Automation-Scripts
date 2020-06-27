# -*- coding: utf-8 -*-
import scrapy


class BookSpider(scrapy.Spider):
    name = 'book'
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        pass
