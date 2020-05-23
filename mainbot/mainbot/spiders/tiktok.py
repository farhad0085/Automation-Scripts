import scrapy
from ..websiteslinks import linkHelpMan

class EmailbotSpider(scrapy.Spider):
    name = 'tiktok'
    link = linkHelpMan()

    start_urls = link.getFirstLink()

    i = 2

    def parse(self, response):

        for l in range(self.link.linkNumber()):

            url = self.link.readExactLink(self.i)
            self.i += 1

            print(response.xpath("//meta[@name='keywords']/@content").extract())

            yield response.follow(url, callback=self.parse)