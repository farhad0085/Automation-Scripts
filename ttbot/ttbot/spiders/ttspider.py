import scrapy
from ..items import TtbotItem
from ..websitelinks import linkHelpMan

class TtspiderSpider(scrapy.Spider):
    name = 'ttspider'
    allowed_domains = ['tiktok.com']

    link = linkHelpMan()

    total = link.linkNumber()

    su = []

    for i in range(total):
        su.append(link.readExactLink(i+1))

    start_urls = ["https://www.tiktok.com/@talliastorm"]

    print(start_urls)

    i = 2

    def parse(self, response):

        items = TtbotItem()
        items['it'] = "nothing to yield"

        for href in response.css('a::attr(href)').extract():
            file = open("data.txt", 'a+')
            if href.startswith("https://www.tiktok.com/@"):
                file.write(href+"\n")
                #yield response.follow(href, callback=self.parse)
            yield items