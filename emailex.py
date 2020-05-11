import scrapy
import re

class EmailbotSpider(scrapy.Spider):
    name = 'emailbot'
    start_urls = ['http://localhost/']

    def parse(self, response):
        reobj = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,6}\b", re.IGNORECASE)
        emailList = re.findall(reobj, response.css("html")[0].extract())