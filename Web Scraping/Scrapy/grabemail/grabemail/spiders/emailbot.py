import scrapy
import re
from ..items import GrabemailItem
from ..websitelinks import linkHelpMan

class EmailbotSpider(scrapy.Spider):
    name = 'emailbot'
    link = linkHelpMan()

    start_urls = link.getFirstLink()

    i = 2

    def parse(self, response):

        items = GrabemailItem()

        reobj = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,6}\b", re.IGNORECASE)
        emailList = re.findall(reobj, response.css("html")[0].extract())

        items['emailList'] = emailList

        for l in range(self.link.linkNumber()):

            url = self.link.readExactLink(self.i)
            self.i += 1

            yield response.follow(url, callback=self.parse)

        yield items