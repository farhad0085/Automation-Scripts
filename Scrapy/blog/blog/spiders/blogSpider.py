# -*- coding: utf-8 -*-
import scrapy
import mysql.connector as mydb
from ..items import BlogItem

class BlogspiderSpider(scrapy.Spider):
    name = 'blogSpider'
    start_urls = ['https://copyblogger.com']
    page_number = 2

    def parse(self, response):
        items = BlogItem()

        html = response.css(".entry")
        for post in html:
            title = post.css(".entry-title-link::text").extract()
            link = post.css("a.entry-title-link::attr(href)").extract()

            items['title'] = title
            items['link'] = link

            yield items

        next_page = "https://copyblogger.com/page/"+str(self.page_number)

        if self.page_number < 331:
            self.page_number += 1
            yield response.follow(next_page, callback=self.parse)